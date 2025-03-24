import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import flask
from flask import Flask, render_template, request, jsonify, send_file
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64

# Initialize Flask app
app = Flask(__name__)

# Set a larger maximum file size (default is 16MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max upload size

# Define the answer key
ANSWER_KEY = {
    "MCQ_1": "B",  
    "MCQ_2": "A",
    "TEXT_1": "Machine learning is a subset of artificial intelligence.",
    "TEXT_2": "A neural network is composed of layers of neurons."
}

# Function to evaluate MCQs
def evaluate_mcq(student_answer, correct_answer):
    if pd.isna(student_answer):  # Check for missing values
        return 0
    student_answer = str(student_answer).strip().upper()
    return 1 if student_answer == correct_answer.upper() else 0

# Function to evaluate textual answers using cosine similarity
def evaluate_textual_answer(student_answer, ideal_answer):
    if pd.isna(student_answer):  # Handle missing values
        return 0  # Assign zero similarity score for missing answers

    student_answer = str(student_answer).strip()
    ideal_answer = str(ideal_answer).strip()

    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([student_answer, ideal_answer])
    similarity = cosine_similarity(vectors[0], vectors[1])[0][0]
    
    return round(similarity * 10, 2)  # Convert similarity to a 10-point scale

# Process student responses
def evaluate_responses(df):
    scores = []
    
    for _, row in df.iterrows():
        student_id = row["Student_ID"]
        mcq_1_score = evaluate_mcq(row["MCQ_1"], ANSWER_KEY["MCQ_1"])
        mcq_2_score = evaluate_mcq(row["MCQ_2"], ANSWER_KEY["MCQ_2"])
        text_1_score = evaluate_textual_answer(row["TEXT_1"], ANSWER_KEY["TEXT_1"])
        text_2_score = evaluate_textual_answer(row["TEXT_2"], ANSWER_KEY["TEXT_2"])
        
        total_score = mcq_1_score + mcq_2_score + text_1_score + text_2_score
        scores.append({
            "Student_ID": student_id,
            "MCQ_1_Score": mcq_1_score,
            "MCQ_2_Score": mcq_2_score,
            "Text_1_Score": text_1_score,
            "Text_2_Score": text_2_score,
            "Total_Score": total_score
        })
    
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
        
        # Question performance
        plt.figure(figsize=(10, 6))
        question_cols = ["MCQ_1_Score", "MCQ_2_Score", "Text_1_Score", "Text_2_Score"]
        sns.barplot(x=question_cols, y=results_df[question_cols].mean(), palette="viridis")
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
        
        print("Visualizations generated successfully")
    except Exception as e:
        print(f"Error generating visualizations: {str(e)}")
        # Provide empty placeholders if visualization fails
        visualizations['score_distribution'] = ""
        visualizations['question_performance'] = ""
    
    return visualizations

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"status": "error", "message": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"status": "error", "message": "No selected file"})
    
    if file and file.filename.endswith(('.xlsx', '.xls')):
        # Save the file temporarily
        temp_path = 'templates/temp_responses.xlsx'
        file.save(temp_path)
        
        # Process the file
        try:
            df = pd.read_excel(temp_path)
            results_df = evaluate_responses(df)
            
            # Generate summary statistics
            summary = {
                "total_students": len(results_df),
                "average_score": round(results_df['Total_Score'].mean(), 2),
                "highest_score": float(results_df['Total_Score'].max()),
                "passing_rate": round(len(results_df[results_df['Total_Score'] >= 12]) / len(results_df) * 100, 2)
            }
            
            # Generate visualizations
            visualizations = generate_visualizations(results_df)
            
            # Save the results to a CSV file
            results_df.to_csv('final_results.csv', index=False)
            
            # Return only summary and visualizations, not detailed results
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
    if os.path.exists('final_results.csv'):
        return send_file('final_results.csv', as_attachment=True)
    else:
        return jsonify({"status": "error", "message": "Results file not found"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)