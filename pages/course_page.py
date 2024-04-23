import streamlit as st
from mocktest import mock_test
from progress import progress
from recommendation import recommendation
from pages.ask import Chatbot
                    
                    
if not st.session_state.loggedin:
    st.switch_page("app.py")
    
else:
    if "course" in st.session_state:
        course=st.session_state.course
        st.title(course["course_name"])
        if st.session_state.type=="mocktest":
            mock_test(course["course_name"])
        elif st.session_state.type=="progress":
            progress(st.session_state.user["user"]["id"], course["id"])
        elif st.session_state.type=="recommendation":
            recommendation(course["id"],course["course_name"], st.session_state.user["user"]["id"])
        elif st.session_state.type=="topic":
            mock_test(st.session_state.topic)  
        # elif st.session_state.type=="ask": 
        #     c=Chatbot()
        #     c.converse(st.session_state.topic)
