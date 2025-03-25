from dotenv import load_dotenv
load_dotenv()

import os
import google.generativeai as genai

genai.configure(api_key=os.environ["AIzaSyBOVINvSND0SRDOpj1Jr7ezXcxpp_jXWSk"])

# Create the model with modified settings
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 300,  # Reduced to make responses shorter
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
)


def generate_response(prompt):
    response = model.generate_content([
    "You are a teaching chatbot with an understanding of all subjects. Your goal is to help students learn concepts clearly and also aid in doing their homework by helping them build intution to solve a problem. Keep your answers brief, focused and to the point.\nExplain topics concisely but accurately.\nUse simple language and short examples.\n\nFocus on the important points.",
    "input: who are you",
    "output: I'm a teaching assistant designed to help you learn. I can explain concepts from various subjects in a simple, straightforward way, with respect to the token limit.",
    f'input: {prompt}',
    "output: ",
    ])
    return (response.text)


# while True:
#     string= str(input("Enter your question: "))
#     print("bot : ", generate_response(string))

