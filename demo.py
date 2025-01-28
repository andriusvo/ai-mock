import streamlit as st

st.set_page_config(page_title="Login | AI Mock Interview", initial_sidebar_state="collapsed")
st.title("Login Page")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username == "turing" and password == "turing":
        st.session_state.authenticated = True
        st.switch_page('pages/bot.py')
    else:
        st.error("Invalid username or password")