# Advanced Assignment Grader

A modern web application for creating assessments, evaluating student responses, and generating personalized feedback with powerful analytics.

![Advanced Assignment Grader](https://img.shields.io/badge/Version-1.0-blue.svg) ![Python](https://img.shields.io/badge/Python-3.8+-orange.svg) ![Flask](https://img.shields.io/badge/Flask-2.0+-purple.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Question Types](#question-types)
- [Evaluation Methods](#evaluation-methods)
- [Personalized Feedback](#personalized-feedback)
- [Data Visualization](#data-visualization)
- [Demo](#demo)
- [Contributing](#contributing)
- [Future Enhancements](#future-enhancements)


## Overview

The Advanced Assignment Grader is a comprehensive web-based tool designed to streamline the assessment process for educators. It allows teachers to create custom assessments with different question types, automatically evaluate student responses with advanced NLP techniques, and generate insightful analytics and personalized feedback.

## Features

- **Intuitive Assessment Creation**: Easily create assessments with multiple-choice and text-based questions
- **Automatic Grading**: Process student responses automatically with machine learning techniques
- **Dark/Light Mode**: Modern UI with theme switching capability
- **Advanced Text Evaluation**: Utilize NLP techniques to evaluate text answers
- **Data Visualization**: Generate insightful charts showing score distribution and question performance
- **Personalized Feedback**: Generate individualized student feedback based on performance
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Excel Template Generation**: Create downloadable templates for student responses
- **Secure File Handling**: All files are handled securely in isolated temporary directories

## Technologies Used

- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Backend**: Python, Flask
- **Data Processing**: Pandas, NumPy
- **Machine Learning**: Scikit-learn, TF-IDF vectorization
- **Visualization**: Matplotlib, Seaborn
- **File Handling**: Excel/CSV via Pandas

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/advanced-assignment-grader.git
   cd advanced-assignment-grader
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python graderv2.py
   ```

5. Access the application in your web browser at:
   ```
   http://127.0.0.1:5000/
   ```

## Usage

### Step 1: Create an Assessment

1. Navigate to the application homepage
2. Click "Add Multiple Choice" or "Add Text Question" to create questions
3. Enter the question text and the correct answer for each question
4. Click "Save Assessment" when finished

### Step 2: Upload Student Responses

1. Download the Excel template (automatically generated after creating the assessment)
2. Fill in the template with student responses (or have students fill it out)
3. Upload the completed Excel file
4. The system will automatically evaluate the responses

### Step 3: View Results and Analytics

1. Review the summary statistics (average score, passing rate, etc.)
2. Explore the visual representations of score distribution and question performance
3. Download the complete results CSV file with scores and personalized feedback

## Project Structure

```
auto_grader/
│
├── graderv2.py           # Main Flask application
├── requirements.txt      # Python dependencies
│
├── templates/
│   └── index2.html       # Frontend interface
│
└── README.md             # Project documentation
```

## Question Types

### Multiple Choice Questions (MCQs)
- Each MCQ is worth 1 point
- Evaluation is done via exact string matching (case insensitive)
- Ideal for objective assessment with definite answers

### Text Questions
- Each text question is worth 10 points
- Evaluation uses TF-IDF vectorization and cosine similarity
- Falls back to character-level n-grams when necessary
- Perfect for subjective questions requiring detailed responses

## Evaluation Methods

### MCQ Evaluation
The system compares the student's answer with the correct option using case-insensitive string matching.

### Text Answer Evaluation
The system uses a pipeline of techniques:
1. **TF-IDF Vectorization**: Converts text answers to numerical vectors
2. **Cosine Similarity**: Calculates the similarity between student and model answers
3. **Fallback Mechanisms**: Uses character n-grams or SequenceMatcher when TF-IDF fails
4. **Scoring Scale**: Converts similarity (0-1) to a 10-point scale

## Personalized Feedback

After evaluating student responses, the system generates personalized feedback:

1. **Overall Assessment**: Based on total score percentage
2. **Strengths Identification**: Highlights questions where the student performed exceptionally
3. **Areas for Improvement**: Identifies topics needing more attention
4. **Comparative Analysis**: Considers how the student performed relative to class averages
5. **Encouragement**: Provides motivational messages tailored to performance level

## Data Visualization

### Score Distribution
A histogram showing the distribution of total scores across all students, with a kernel density estimate overlay.

### Question Performance
A bar chart displaying the average score for each question, helping identify which topics are well-understood and which need reinforcement.

## Demo

To test the application with sample data:

1. Start the application
2. Create a simple assessment with 2-3 questions
3. Download the Excel template
4. Fill in sample responses for 5-10 fictional students
5. Upload the file and explore the results

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Future Enhancements

- Additional question types (numeric, matching, code evaluation)
- User authentication and role-based access control
- Integration with learning management systems
- Advanced analytics including item analysis
- Spaced repetition recommendations based on student performance
- Collaborative assessment creation



---

Developed with ❤️ for educators