import streamlit as st
import requests
import json
url = 'http://127.0.0.1:5000'

def registration():
    with st.form("Registration"):
        username = st.text_input("username")
        password = st.text_input("password", type="password")

    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            response = requests.post(url+'/register', json={"username": username, "password":password})
            if response.status_code == 200:
                print(response.text)
                st.session_state.user=json.loads(response.text)
                st.session_state.loggedin=True
                st.rerun()
            else:
                print(response.status_code)
                
def login():
    with st.form("Login"):
        username = st.text_input("username")
        password = st.text_input("password", type="password")

    # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            response = requests.post(url+'/login', json={"username": username, "password":password})
            if response.status_code == 200:
                print(response.text)
                st.session_state.user=json.loads(response.text)
                st.session_state.loggedin=True
                st.rerun()
            else:
                print(response.status_code)

def logout():
    st.session_state.loggedin=False
    st.session_state.user={}
    st.session_state.clear()
    st.rerun()