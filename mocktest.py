import streamlit as st
import os
import json
import matplotlib.pyplot as plt
import requests
from streamlit_extras.stylable_container import stylable_container
import env

url = 'http://127.0.0.1:5000'

from langchain_community.llms import OpenAI

def print_correct_answer_if_submitted(i):
   if st.session_state.submit:
      if st.session_state.quiz_object['correct'][i]==st.session_state.user_answer[i]:
         st.write("✅ correct")
      else:
         st.markdown("❌ incorrect  \n  "  
                     f"⛳️ the correct answer is: **{st.session_state.quiz_object['correct'][i]}**")

def mock_test(course_name):
   llm = OpenAI(temperature=0.9, max_tokens=-1)

   st.title("Interactive MCQ Quiz Generator")

   res = '{"questions": [],"options": [],"correct": []}'

   course_name = st.text_input("Enter the course name:", value=course_name)
   num_questions = st.number_input("Number of questions:", min_value=1, value=3)
   difficulty=st.selectbox("Difficulty:",
      ("easy", "medium", "hard"),
      index=None,
      placeholder="Select difficulty...")

   if "gen_state" not in st.session_state:
      st.session_state.gen_state=False
      st.session_state.quiz_object={}
      st.session_state.user_answer={}
      st.session_state.submit=False
      
   if st.button("Generate Questions") :
      # Prompt LLM to generate questions
      prompt = f"Generate {num_questions} {difficulty} multiple choice questions from the following course: '{course_name}'. return it in json format where the key \"questions\" has the list of questions, key \"options\" has a list of options of which exactly one is correct per question, and key \"correct\" which has the correct answer exactly as in the options list, and a key \"topic\" which has the topic that each question belonged to."
      res = llm(prompt)
      # res = '{"questions": ["1. Which of the following is NOT a supervised learning algorithm?","2. Which of the following is used to measure the performance of a machine learning model?","3. Which of the following is an example of an unsupervised learning algorithm?","4. What is the name of the process used to adjust the weights in a neural network?","5. What type of machine learning algorithm is used for anomaly detection?","6. What is the term used to describe the process of dividing data into training and testing sets?","7. Which of the following is a type of ensemble learning algorithm?","8. Which of the following is a common evaluation metric for regression models?","9. Which of the following is a characteristic of a deep learning model?","10. Which of the following is a technique used to handle missing data in a dataset?"],"options": [["Decision tree", "K-means", "Random forest", "SVM"],["Accuracy", "Precision", "Recall", "F1 score"],["K-means clustering", "Linear regression", "Naive Bayes", "Decision tree"],["Backpropagation", "Gradient descent", "Stochastic optimization", "Supervised learning"],["Clustering", "Classification", "Regression", "Semi-supervised learning"],["Splitting", "Normalization", "Sampling", "Cross-validation"],["AdaBoost", "KNN", "Logistic regression", "Gaussian Naive Bayes"],["RMSE", "ROC AUC", "Log Loss", "MAE"],["Multiple layers", "Sparse data", "Small dataset", "Few parameters"],["Mean imputation", "Random forest imputation", "Forward fill", "Interpolation"]],"correct": ["K-means","F1 score","K-means clustering","Backpropagation","Anomaly detection","Cross-validation","AdaBoost","RMSE","Multiple layers","Mean imputation"]}'
      resObject=json.loads(res)
      print(res)
      st.session_state.gen_state=True
      st.session_state.quiz_object=json.loads(res)
      st.session_state.user_answer={}
      st.session_state.submit=False


   if st.session_state.gen_state or st.session_state.submit:
      quiz_object=st.session_state.quiz_object
      for i in range(len(quiz_object['questions'])):
         st.subheader(f"Question {i + 1}: {quiz_object['questions'][i]}")
         print_correct_answer_if_submitted(i)
         user_answer = st.radio("choose the correct answer:", quiz_object['options'][i], key=i)
         st.session_state.user_answer[i]=user_answer
            
      if not st.session_state.submit:
         if st.button("Submit"):
            st.session_state.submit=True
            print(st.session_state.user_answer)
            print("submitted")
            
            st.rerun()
            
   if st.session_state.submit:
      score=0
      total=len(quiz_object['correct'])
      strengths=[]
      weaknesses=[]
      for i in range(total):
         if st.session_state.user_answer[i]==quiz_object['correct'][i]:
            score=score+1
            strengths.append(quiz_object['topic'][i])
         else:
            weaknesses.append(quiz_object['topic'][i])
            
      labels = 'correct', 'incorrect'
      
      response=requests.post(url+'/submit_test', json={"user_id":st.session_state.user["user"]["id"], "course_id":st.session_state.course["id"], "score":score*100/total})
      
      sizes = [score*100/total, 100-(score*100/total)]
      explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

      fig1, ax1 = plt.subplots()
      ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
      ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

      st.pyplot(fig1)
      
      with st.container():
         col1, col2 = st.columns(2)
         
         with col1.container(border=True):
            st.subheader("strengths")
            for s in strengths:
               with stylable_container(
                  "green",
                  css_styles="""
                  button {
                     color: #1bd15e;
                     transition: background-color 0.3s ease;
                  }
                  button:hover {
                     background-color: #ffffff; /* Change color on hover */
                  }
                  """,
               ):
                  cola, colb= st.columns(2)
                  with cola:
                     if st.button(s, key=f's-{s}'):
                        st.session_state.type="topic"
                        st.session_state.topic=s
                        st.session_state.gen_state=False
                        st.session_state.quiz_object={}
                        st.session_state.submit=False
                        st.switch_page("pages/course_page.py")
                  with colb:
                     if st.button("ask", key=f'sa-{s}'):
                        st.session_state.type="ask"
                        st.session_state.chattopic=s
                        st.session_state.chatset=False
                        st.switch_page('pages/ask.py')
                  
         with col2.container(border=True):
            st.subheader("Weaknesses")
            for w in weaknesses:
               with stylable_container(
                  "red",
                  css_styles="""
                  button {
                     color: #bf172d;
                     transition: background-color 0.3s ease;
                  }
                  button:hover {
                     background-color: #ffffff; /* Change color on hover */
                  }
                  """,
               ):
                  cola, colb= st.columns(2)
                  with cola:
                     if st.button(w, key=f'w-{w}'):
                        st.session_state.type="topic"
                        st.session_state.topic=w
                        st.session_state.gen_state=False
                        st.session_state.quiz_object={}
                        st.session_state.submit=False
                        st.switch_page("pages/course_page.py")
                  with colb:
                     if st.button("ask", key=f'wa-{w}'):
                        st.session_state.type="ask"
                        st.session_state.chattopic=w
                        st.session_state.chatset=False
                        st.switch_page('pages/ask.py')
         
         