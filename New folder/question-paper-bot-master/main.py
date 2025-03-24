import streamlit as st
import time
import qpm_logic
import random

# Page configuration
st.set_page_config(
    page_title="Question Paper Generator",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
    }
    .stButton>button {
        background-color: #1E88E5;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .question-box {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 1rem;
    }
    .history-item {
        padding: 0.5rem;
        border-radius: 5px;
        margin-bottom: 0.5rem;
        background-color: #f1f1f1;
    }
    .stExpander {
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

# Streamed response emulator to show questions being generated
def response_generator(topic, question_type, num_questions):
    response = qpm_logic.generate_questions(topic, question_type, num_questions)
    for line in response.split('\n'):
        yield line + "\n"
        time.sleep(0.05)

st.title("Professor AI - Question Paper Generator")
st.write("Generate educational questions for assessments and learning materials.")

# Sidebar for input controls
with st.sidebar:
    st.header("Question Settings")
    topic = st.text_input("Topic", placeholder="e.g., Photosynthesis in plants")
    question_type = st.selectbox(
        "Question Type",
        options=["mcq", "text", "both"],
        format_func=lambda x: {
            "mcq": "Multiple Choice Questions",
            "text": "Text/Short Answer Questions", 
            "both": "Mix of Both Types"
        }.get(x),
    )
    num_questions = st.slider("Number of Questions", min_value=1, max_value=10, value=5)
    
    generate_button = st.button("Generate Questions")

# Initialize session state
if "questions" not in st.session_state:
    st.session_state.questions = None
if "history" not in st.session_state:
    st.session_state.history = []

# Handle generation
if generate_button and topic:
    with st.spinner("Generating questions..."):
        st.session_state.questions = qpm_logic.generate_questions(topic, question_type, num_questions)
        # Save to history
        st.session_state.history.append({
            "topic": topic,
            "type": question_type,
            "count": num_questions,
            "questions": st.session_state.questions
        })

# Display generated questions
if st.session_state.questions:
    st.header("Generated Questions")
    st.markdown(st.session_state.questions)
    
    # Add export options
    st.download_button(
        "Download Questions",
        st.session_state.questions,
        file_name=f"questions_{topic.replace(' ', '_')}.txt",
        mime="text/plain"
    )

# Show generation history
if st.session_state.history:
    with st.expander("Question Generation History"):
        for i, item in enumerate(st.session_state.history):
            st.write(f"**{i+1}. {item['topic']}** ({item['count']} {item['type']} questions)")
            if st.button(f"Show questions #{i+1}"):
                st.session_state.questions = item['questions']
                st.experimental_rerun()