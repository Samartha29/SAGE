import streamlit as st
import json
import requests
from streamlit_elements import elements, mui, html

url = 'http://127.0.0.1:5000'


if not st.session_state.loggedin:
    st.switch_page("app.py")

else:
    st.header("Create Course")

    course_name=st.text_input("Course Name")

    if st.button("create"):
        response = requests.post(url+'/create_course', json={'course_name':course_name})
        if response.status_code==200:
            st.write("course created successfully!")
        else:
            st.write("course creation failed")

    st.header("All Courses: ")

    response = requests.get(url+'/get_all_courses')

    response_json= json.loads(response.text)
    courses=response_json['courses']

    for i in range(len(courses)):
        with st.expander(f'📖 {courses[i]["course_name"]}'):
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button(
                    "mocktest",
                    key=f'{courses[i]["course_name"]}-col1'
                ):
                    st.session_state.gen_state=False
                    st.session_state.quiz_object={}
                    st.session_state.submit=False
                    st.session_state.type='mocktest'
                    st.session_state.course=courses[i]
                    st.switch_page('pages/course_page.py')
            with col2:
                if st.button(
                    "progress",
                    key=f'{courses[i]["course_name"]}-col2'
                ):
                    st.session_state.type='progress'
                    st.session_state.course=courses[i]
                    st.switch_page('pages/course_page.py')
            with col4:
                if st.button(
                    "recommendation",
                    key=f'{courses[i]["course_name"]}-col3'
                ):
                    st.session_state.type='recommendation'
                    st.session_state.course=courses[i]
                    st.switch_page('pages/course_page.py')
                    
            with col3:
                if st.button(
                    "ask",
                    key=f'{courses[i]["course_name"]}-col4'
                ):
                    st.session_state.type="ask"
                    st.session_state.chattopic=courses[i]["course_name"]
                    st.session_state.chatset=False
                    st.switch_page('pages/ask.py')
                    
                

