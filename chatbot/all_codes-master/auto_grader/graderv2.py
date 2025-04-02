import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, render_template, request, jsonify, send_file, session
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import uuid
import atexit
import tempfile
import glob

# Create a dedicated temp directory for your application
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'auto_grader_temp')
os.makedirs(TEMP_DIR, exist_ok=True)

# Function to clean up all temporary files on application exit
def cleanup_temp_files():
    """Remove all temporary files created by the application"""
    try:
        # Delete all temporary files
        for file_pattern in ['assessment_template_*.xlsx', 'temp_responses_*.xlsx', 'results_*.csv']:
            for file_path in glob.glob(os.path.join(TEMP_DIR, file_pattern)):
                try:
                    os.remove(file_path)
                    print(f"Cleaned up: {file_path}")
                except:
                    pass
    except Exception as e:
        print(f"Error during cleanup: {e}")

# Register the cleanup function to run when the application exits
atexit.register(cleanup_temp_files)

# Initialize Flask app
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload size
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')  # For session management

# Function to evaluate MCQs
def evaluate_mcq(student_answer, correct_answer):
    if pd.isna(student_answer):  # Check for missing values
        return 0
    student_answer = str(student_answer).strip().upper()
    return 1 if student_answer == correct_answer.upper() else 0

# Function to evaluate textual answers using cosine similarity
def evaluate_textual_answer(student_answer, ideal_answer):
    if pd.isna(student_answer) or not str(student_answer).strip():  # Handle missing/empty values
        return 0  # Assign zero similarity score for missing answers

    student_answer = str(student_answer).strip()
    ideal_answer = str(ideal_answer).strip()
    
    # If either answer is very short, do exact matching instead
    if len(student_answer) < 5 or len(ideal_answer) < 5:
        return 10 if student_answer.lower() == ideal_answer.lower() else 0
    
    try:
        # Configure vectorizer to handle small documents better
        vectorizer = TfidfVectorizer(stop_words=None, lowercase=True, min_df=1, max_df=1.0)
        
        try:
            vectors = vectorizer.fit_transform([student_answer, ideal_answer])
            
            # Check if we have non-empty vocabulary
            if len(vectorizer.get_feature_names_out()) == 0:
                raise ValueError("Empty vocabulary")
                
            similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
            
        except ValueError:
            # Fall back to character level if we have empty vocabulary
            print("Falling back to character-level n-grams")
            vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(2, 4), min_df=1, max_df=1.0)
            vectors = vectorizer.fit_transform([student_answer, ideal_answer])
            similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    except Exception as e:
        print(f"Error in similarity calculation: {str(e)}")
        # If TF-IDF fails, use a simpler string comparison
        from difflib import SequenceMatcher
        similarity = SequenceMatcher(None, student_answer.lower(), ideal_answer.lower()).ratio()
    
    return round(similarity * 10, 2)  # Convert similarity to a 10-point scale

# Process student responses
def evaluate_responses(df, questions_data):
    scores = []
    
    for _, row in df.iterrows():
        student_id = row["Student_ID"]
        student_scores = {"Student_ID": student_id}
        total_score = 0
        
        # Evaluate each question based on the questions data
        for question in questions_data:
            q_id = question.get('column_id', question['id'])  # Use column_id if available, fallback to id
            q_type = question['type']
            
            # Check if this question exists in the student response
            if q_id in df.columns:
                if q_type == 'mcq':
                    score = evaluate_mcq(row[q_id], question['answer'])
                    student_scores[f"{q_id}_Score"] = score
                    total_score += score
                elif q_type == 'text':
                    score = evaluate_textual_answer(row[q_id], question['answer'])
                    student_scores[f"{q_id}_Score"] = score
                    total_score += score
            else:
                # Question not found in responses, score as 0
                student_scores[f"{q_id}_Score"] = 0
                print(f"Warning: Column '{q_id}' not found in student responses")
        
        student_scores["Total_Score"] = total_score
        scores.append(student_scores)
    
    return pd.DataFrame(scores)

# Generate visualizations
def generate_visualizations(results_df):
    visualizations = {}
    
    try:
        # Use Agg backend to prevent display issues
        import matplotlib
        matplotlib.use('Agg')
        
        # Score distribution
        plt.figure(figsize=(10, 6))
        sns.histplot(results_df['Total_Score'], bins=12, kde=True)
        plt.title('Distribution of Total Scores')
        plt.xlabel('Total Score')
        plt.ylabel('Number of Students')
        plt.tight_layout()
        
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png', dpi=100)
        buffer.seek(0)
        score_dist_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        visualizations['score_distribution'] = f'data:image/png;base64,{score_dist_b64}'
        plt.close()
        
        # Question performance - get only score columns
        score_cols = [col for col in results_df.columns if col.endswith('_Score') and col != 'Total_Score']
        
        if score_cols:  # Only create this visualization if we have score columns
            plt.figure(figsize=(10, 6))
            avg_scores = results_df[score_cols].mean()
            
            # Create a readable version of the question IDs for the plot
            score_labels = [col.replace('_Score', '') for col in score_cols]
            
            # Truncate long question texts for better display
            score_labels = [label[:20] + '...' if len(label) > 20 else label for label in score_labels]
            
            sns.barplot(x=score_labels, y=avg_scores.values, palette="viridis")
            plt.title('Average Score by Question')
            plt.xlabel('Question')
            plt.ylabel('Average Score')
            plt.xticks(rotation=45)  # Rotate labels for better readability
            plt.tight_layout()
            
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            question_perf_b64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            visualizations['question_performance'] = f'data:image/png;base64,{question_perf_b64}'
            plt.close()
        
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")
        # Provide empty placeholders if visualization fails
        visualizations['score_distribution'] = ""
        visualizations['question_performance'] = ""
    
    return visualizations

# Routes
@app.route('/')
def index():
    return render_template('index2.html')

@app.route('/setup_assessment', methods=['POST'])
def setup_assessment():
    try:
        data = request.json
        questions_data = data.get('questions', [])
        
        # Validate the questions data
        if not questions_data:
            return jsonify({"status": "error", "message": "No questions provided"})
        
        # Generate a session ID for this assessment
        assessment_id = str(uuid.uuid4())
        
        # Use the full question text as the column ID (what will appear in Excel)
        for question in questions_data:
            question['column_id'] = question['text']
        
        # Store the questions data in the session
        session['assessment_id'] = assessment_id
        session['questions_data'] = questions_data
        
        # Calculate total possible points
        total_points = sum(1 if q['type'] == 'mcq' else 10 for q in questions_data)
        session['total_points'] = total_points
        
        # Generate a sample Excel template for the teacher
        sample_columns = ['Student_ID'] + [q['column_id'] for q in questions_data]
        sample_df = pd.DataFrame(columns=sample_columns)
        sample_df.loc[0] = ['Student1'] + ['' for _ in questions_data]  # Add a sample row
        
        # Save to the temp directory
        sample_file = os.path.join(TEMP_DIR, f'assessment_template_{assessment_id}.xlsx')
        sample_df.to_excel(sample_file, index=False)
        session['template_file'] = sample_file
        
        return jsonify({
            "status": "success", 
            "message": "Assessment setup successfully",
            "assessment_id": assessment_id,
            "total_points": total_points,
            "has_template": True
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/upload_responses', methods=['POST'])
def upload_responses():
    # Check if we have questions data in the session
    if 'questions_data' not in session:
        return jsonify({
            "status": "error", 
            "message": "No assessment configured. Please set up questions and answers first."
        })
    
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file and file.filename.endswith(('.xlsx', '.xls')):
        # Save the file to the temp directory
        temp_path = os.path.join(TEMP_DIR, f'temp_responses_{session["assessment_id"]}.xlsx')
        file.save(temp_path)
        
        # Process the file
        try:
            df = pd.read_excel(temp_path)
            
            # Validate that Student_ID column exists
            if "Student_ID" not in df.columns:
                return jsonify({
                    "status": "error", 
                    "message": "Student response file must contain a 'Student_ID' column"
                })
            
            # Get the questions data from the session
            questions_data = session['questions_data']
            total_points = session['total_points']
            
            # Evaluate responses using the questions data
            results_df = evaluate_responses(df, questions_data)
            
            # Generate summary statistics
            passing_threshold = total_points * 0.6  # 60% as passing grade
            
            summary = {
                "total_students": len(results_df),
                "average_score": round(results_df['Total_Score'].mean(), 2),
                "highest_score": float(results_df['Total_Score'].max()),
                "total_possible": total_points,
                "passing_threshold": passing_threshold,
                "passing_rate": round(len(results_df[results_df['Total_Score'] >= passing_threshold]) / len(results_df) * 100, 2)
            }
            
            # Generate visualizations
            visualizations = generate_visualizations(results_df)
            
            # Save the results to a temporary CSV file
            results_file = os.path.join(TEMP_DIR, f'results_{session["assessment_id"]}.csv')
            results_df.to_csv(results_file, index=False)
            session['results_file'] = results_file
            
            return jsonify({
                "status": "success",
                "summary": summary,
                "visualizations": visualizations
            })
            
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)})
        finally:
            # Clean up the temporary file
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return jsonify({"status": "error", "message": "Invalid file format"})

@app.route('/download_results')
def download_results():
    if 'results_file' in session and os.path.exists(session['results_file']):
        return send_file(session['results_file'], as_attachment=True, download_name="student_evaluation_results.csv")
    else:
        return jsonify({"status": "error", "message": "Results file not found"})

@app.route('/download_template')
def download_template():
    """Download an Excel template that matches the assessment structure"""
    if 'template_file' in session and os.path.exists(session['template_file']):
        return send_file(
            session['template_file'], 
            as_attachment=True, 
            download_name="student_response_template.xlsx"
        )
    else:
        return jsonify({"status": "error", "message": "Template file not found"})

@app.route('/clear_assessment', methods=['POST'])
def clear_assessment():
    """Clear the current assessment data from the session"""
    # Clean up files
    if 'results_file' in session and os.path.exists(session['results_file']):
        os.remove(session['results_file'])
        
    if 'template_file' in session and os.path.exists(session['template_file']):
        os.remove(session['template_file'])
    
    # Clear session data
    session.pop('assessment_id', None)
    session.pop('questions_data', None)
    session.pop('total_points', None)
    session.pop('results_file', None)
    session.pop('template_file', None)
    
    return jsonify({"status": "success", "message": "Assessment data cleared"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)