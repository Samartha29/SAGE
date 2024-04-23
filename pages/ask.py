import streamlit as st
import streamlit as st
from langchain_community.llms import OpenAI

from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.chains import ConversationChain


class Chatbot:
    def __init__(self):
        if not st.session_state.loggedin:
            st.switch_page("app.py")
            
        # print(conversation("Hello"))
        # print(conversation("what to do today"))
        # print(conversation("how is the weather"))
        # print(conversation("what to eat"))
        # print(conversation("whats a dosa"))

        if ("chatset" not in st.session_state) or (st.session_state.chatset == False) :
            st.session_state.chatquery=[]
            st.session_state.chatresponse=[]
            st.session_state.chatset=True
            llm = OpenAI(temperature=0.9, max_tokens=-1)

            st.session_state.conversation = ConversationChain(
                llm=llm,
                memory=ConversationBufferWindowMemory(k=3)
            )
    
    def clear(self):
        st.session_state.chatset=False
        if ("chatset" not in st.session_state) or (st.session_state.chatset == False) :
            st.session_state.chatquery=[]
            st.session_state.chatresponse=[]
            st.session_state.chatset=True
            llm = OpenAI(temperature=0.9, max_tokens=-1)

            st.session_state.conversation = ConversationChain(
                llm=llm,
                memory=ConversationBufferWindowMemory(k=3)
            )
            st.rerun()

    def get_reply(self, text):
        conv=st.session_state.conversation(text)
        res=conv['response']
        print("\n\n\n")
        print(conv)
        return res

    def converse(self, topic):
        if "chattopic" not in st.session_state:
            prompt = st.chat_input(f"ask something about your coursework")
        else:
            prompt = st.chat_input(f"ask something about {st.session_state.chattopic}")
        if prompt:
            st.session_state.chatquery.append(prompt)
            st.session_state.chatresponse.append(self.get_reply(f"In the context of {topic} reply to: {prompt}"))
            
        for i in range(len(st.session_state.chatquery)):
            
            with st.chat_message("human"):
                st.write(st.session_state.chatquery[i])
                
            if i<len(st.session_state.chatresponse):
                with st.chat_message("AI"):
                    st.write(st.session_state.chatresponse[i])
            else:
                with st.chat_message("AI"):
                    st.write("...")
                    
        clr=st.button("Clear Chat")
        if clr:
            self.clear()

c=Chatbot()
if st.session_state.chatset == False:
    c.clear()
if "chattopic" not in st.session_state:
    c.converse("coursework")
else:
    c.converse(st.session_state.chattopic)