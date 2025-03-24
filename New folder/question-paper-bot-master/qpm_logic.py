from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["AIzaSyBMi_YlMSsxvQI5l2AmE0uL00um7EIy3As"])

# Modified settings for question generation
# - Lower temperature for more consistent, structured output
# - Higher max tokens to allow for multiple questions
generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 800,  # Increased to allow for multiple questions
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def generate_questions(topic, question_type="both", num_questions=5):
    """
    Generate educational questions based on the provided topic.
    
    Args:
        topic (str): The subject or topic to generate questions about
        question_type (str): Type of questions to generate - "mcq", "text", or "both"
        num_questions (int): Number of questions to generate
        
    Returns:
        str: Generated questions
    """
    # Create a prompt that instructs the model to generate specific question types
    system_prompt = """You are an educational question generator for teachers. 
Your task is to create high-quality assessment questions on specific topics.
Follow these guidelines:

1. Create clear, concise, and pedagogically sound questions
2. For multiple-choice questions:
   - Include 4 options (A, B, C, D)
   - Make distractors plausible
   - Put each option on a new line
   - After all options, indicate the correct answer on a new line as "Ans: X" where X is the correct option letter
3. For text questions:
   - Create a mix of factual recall and critical thinking questions
   - Include a brief model answer after each question
4. Format the output with clear question numbering
5. Ensure questions test different cognitive levels (recall, application, analysis)"""

    # Determine what type of questions to generate
    instruction = f"Generate {num_questions} "
    if question_type == "mcq":
        instruction += "multiple-choice questions"
    elif question_type == "text":
        instruction += "text/short answer questions"
    else:
        instruction += f"questions ({num_questions//2} multiple-choice and {num_questions - num_questions//2} text questions)"
    
    instruction += f" about the following topic: {topic}"

    # Generate the questions
    response = model.generate_content([
        system_prompt,
        instruction
    ])
    
    return response.text

# Example usage
# topic = "Photosynthesis in plants"
# print(generate_questions(topic, question_type="both", num_questions=6))

