from dotenv import load_dotenv
load_dotenv() ## loading all the environment variables

import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Define the teacher persona
TEACHER_PERSONA = """You are a helpful and patient teacher assistant named "Professor AI". 
Your role is to:
- Explain concepts clearly using simple language appropriate for students
- Provide examples to illustrate complex ideas
- Ask clarifying questions when needed
- Encourage critical thinking
- Respond with enthusiasm and positivity
- Always be supportive and never condescending
- Focus on explaining rather than just providing answers
- Adapt explanations based on student needs

Your expertise covers all academic subjects including mathematics, science, languages, history, and more."""

## function to load Gemini Pro model and get responses
def get_gemini_response(question):
    model = genai.GenerativeModel("gemini-1.5-pro")
    
    # Create a chat session with the teacher persona
    chat = model.start_chat(history=[
        {"role": "user", "parts": [TEACHER_PERSONA]},
        {"role": "model", "parts": ["I understand my role as Professor AI. I'll provide helpful, clear, and supportive educational assistance to students."]}
    ])
    
    response = chat.send_message(question, stream=True)
    return response

##initialize our streamlit app

st.set_page_config(page_title="Professor AI - Your Educational Assistant")

st.header("Professor AI - Your Educational Assistant")
st.markdown("_Ask any question and receive helpful educational guidance_")

# Initialize session state for chat history and session management
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
    
if 'sessions' not in st.session_state:
    st.session_state['sessions'] = []
    
if 'current_session' not in st.session_state:
    # Initialize first session with timestamp
    session_id = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state['current_session'] = session_id
    st.session_state['sessions'].append({"id": session_id, "messages": []})

# New session button
if st.button("Start New Session"):
    # Create a new session with timestamp
    session_id = datetime.now().strftime("%Y-%m-%d %H:%M")
    st.session_state['current_session'] = session_id
    st.session_state['sessions'].append({"id": session_id, "messages": []})
    st.success(f"Started new session: {session_id}")

input = st.text_input("Your question:", key="input", placeholder="Ask me anything about your studies...")
submit = st.button("Ask Professor AI")

if submit and input:
    response = get_gemini_response(input)
    
    # Find current session
    current_session_id = st.session_state['current_session']
    current_session = next((s for s in st.session_state['sessions'] if s["id"] == current_session_id), None)
    
    # Add user query to current session
    current_session["messages"].append(("Student", input))
    
    # Display streamed response while collecting full response
    st.subheader("Professor AI's Response:")
    full_response = ""
    response_container = st.empty()
    
    for chunk in response:
        full_response += chunk.text
        response_container.write(full_response)
    
    # Add complete bot response to current session
    current_session["messages"].append(("Professor AI", full_response))

# Most recent conversation (current session)
st.subheader("Current Conversation:")
current_session_id = st.session_state['current_session']
current_session = next((s for s in st.session_state['sessions'] if s["id"] == current_session_id), None)

if current_session and current_session["messages"]:
    for role, text in current_session["messages"]:
        if role == "Student":
            st.markdown(f"**👨‍🎓 {role}:** {text}")
        else:
            st.markdown(f"**👨‍🏫 {role}:** {text}")

# Past sessions in collapsible sections
if len(st.session_state['sessions']) > 1:
    st.subheader("Past Conversations:")
    
    # Display past sessions (excluding current)
    for session in reversed(st.session_state['sessions']):
        if session["id"] != current_session_id and session["messages"]:
            with st.expander(f"Session: {session['id']}"):
                for role, text in session["messages"]:
                    if role == "Student":
                        st.markdown(f"**👨‍🎓 {role}:** {text}")
                    else:
                        st.markdown(f"**👨‍🏫 {role}:** {text}")





