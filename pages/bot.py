from openai import OpenAI
import streamlit as st

st.set_page_config(page_title="Inteview | AI Mock Interview", initial_sidebar_state="collapsed")
st.title("AI Mock Interviewer")
slider_value = st.slider("Select temperature", 0.0, 1.0, 0.7, 0.1)

system_prompt = """
You are a professional recruiter conducting a mock interview. Your goal is to evaluate the candidate's strengths and weaknesses for the role of {role}.

**Instructions:**
1. Ask exactly 5 unique, well-structured, and role-specific questions, one at a time.
   - Each question should assess a different aspect of the candidate's skills, experience, or suitability for the role.
2. Wait for the candidate's response to each question before asking the next one.
   - If the candidate's response is negative (e.g., they lack experience or knowledge), acknowledge their honesty and move to the next question.
3. Avoid repeating questions or revisiting previously covered topics.
4. After the candidate answers all 5 questions, provide a concise and constructive summary, including:
   - Their key strengths.
   - Areas for improvement.
   - A final assessment of how prepared they are for the role.
5. User input should be specifically on interview question topic, otherwise ask to provide a correct input.

**Tone and Approach:**
- Be professional, supportive, and objective.
- Offer encouragement when appropriate and ensure a friendly tone.

Let’s begin the mock interview.
"""
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.switch_page('demo.py')

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt.format(role="{role}")},
        {"role": "assistant", "content": "Welcome to Interviewer 3000! Please write a role you want to mock interview for:"}
    ]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if prompt := st.chat_input("Message InterviewGPT"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=st.session_state.messages,
            temperature=slider_value,
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})

