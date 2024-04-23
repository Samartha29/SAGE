import streamlit as st
import os
import json
import matplotlib.pyplot as plt
import requests

url = 'http://127.0.0.1:5000'

def recommendation(courseid, course_name, userid):
    st.header("recommendations")
    
    testresponse=requests.get(url+f'/get_test_scores/{userid}/{courseid}')
    tests=json.loads(testresponse.text)
    scores=0
    count=0
    for test in tests["test_scores"]:
        scores=scores+test["score"]
        count=count+100
    
    
    
    advanced=False
    try:
        advanced=((scores/count)>0.6)
        st.write(f'your rating: **{(scores/count)}**/100')
    except:
        advanced=False
        st.write(f'your rating: **{0}**/100')
        
    if advanced:
        st.write("showing advanced courses")
    else:
        st.write("showing basic courses")
        
    response=requests.post(url+'/recommend', json={"prompt":course_name, "advanced":advanced})
    recs=json.loads(response.text)["courses"]
    for rec in recs:
        with st.expander(f'🧑‍🏫 {rec[0]}'):
            st.header(rec[0])
            # difficulty=rec[1]
            st.link_button("visit course", rec[2])
            difficulty=""
            for d in range(int(rec[1])+1):
                difficulty=difficulty+"🔥"
            st.write(f'**difficulty:** {difficulty}')
            st.subheader("description:")
            st.write(rec[3])
            