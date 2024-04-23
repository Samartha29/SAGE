from mocktest import mock_test
import streamlit as st
import requests
from auth import registration, login, logout



if "loggedin" not in st.session_state:
    st.session_state.loggedin=False
if "user" not in st.session_state:
    st.session_state.user={}
    
if not st.session_state.loggedin:
    if st.selectbox("login/register", ['login', 'register'])=='login':
        login()
    else:
        registration()

if st.session_state.loggedin:
    # st.write(st.session_state.user)
    st.header(f'Welcome {st.session_state.user["user"]["username"]}!')
    if st.button("logout", key="logout"):
        logout()
       

