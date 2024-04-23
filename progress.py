import streamlit as st
import os
import json
import matplotlib.pyplot as plt
import requests

url = 'http://127.0.0.1:5000'

def progress(userid, courseid):
    st.header("progress graph")
    response=requests.get(url+f'/get_test_scores/{userid}/{courseid}')
    tests=json.loads(response.text)
    scores=[]
    timestamps=[]
    for test in tests["test_scores"]:
        scores.append(test["score"])
        timestamps.append(test["timestamp"])
    chart_data={"scores":scores, "timestamps":timestamps}
    st.line_chart(chart_data, x="timestamps", y="scores")
    
    avgresponse=requests.get(url+f'/average_scores/{courseid}')
    avgscores=json.loads(avgresponse.text)["average_scores"]
    rank=0
    st.header("leaderboard")
    with st.container(border=True):
        col1, col2, col3=st.columns(3)
        col1.write(f"**rank**")
        rank=rank+1
        col2.write("**username**")
        col3.write("**average score**")
    for avgscore in avgscores:
        with st.container(border=True):
            col1, col2, col3=st.columns(3)
            if avgscore["username"]==st.session_state.user["user"]["username"]:
                col1.write(f'**{rank}**')
                col2.write(f'**{avgscore["username"]}**')
                col3.write(f'**{avgscore["average_score"]}**')
            else:
                col1.write(rank)
                col2.write(avgscore["username"])
                col3.write(avgscore["average_score"])
            rank=rank+1
    
    