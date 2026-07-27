import streamlit as st
# streamlit: Web based app making 
# light python framework 
st.title("AI Resume Maker")

st.markdown("""## User can create or 
download AI created Resume based on high ATS
Score""")



#========AGENT CODE=========
import os
import time
import langchain
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
import pytesseract as pyt
from tavily import TavilyClient
from langchain.messages import SystemMessage, HumanMessage
import numpy as np
import streamlit as st
from langchain_community.document_loaders import PyMuPDFLoader

#========== API KEY LOAD ===============

GOOGLE_API_KEY = st.sidebar.text_input("GOOGLE_API_KEY",type="password")
GROQ_API_KEY = st.sidebar.text_input("GROQ_API_KEY",type="password")
TAVILY_API_KEY = st.sidebar.text_input("TAVILY_API_KEY",type="password")

#========= MODEL BUILDING ===============

model = ChatGoogleGenerativeAI(
    model = 'gemini-3.5-flash',
    google_api_key = GOOGLE_API_KEY
)
# tool
def search_recent_news_jobs(query):
  """This function helps to search
  recent news or recent jobs
  related to given search query
  suppose user write Python Development jobs
  It should return trending news and jobs link"""
  client = TavilyClient(
      api_key = TAVILY_API_KEY
  )
  return client.search(query)


# agent creation
from langchain.agents import create_agent
agent = create_agent(
    model = model,
    tools = [search_recent_news_jobs]
)

#====== PROMPT GENERATOR =========


def prompt_generator(agent):
  """This functipn help to give detailed prompt
  followed by chain of thoughts and
  persona based prompting, main task is to give
  detailed prompt to build Resume for
  students or Experienced person
  Based on their given personal information.
   """

  prompt = """You are a senior HR resume analyzer,
  main task is to give
  detailed prompt to build Resume for
  students or Experienced person
  Based on their given personal information.
  System Instruction I want Model to generate resume
  in HTML from include that in prompt"""

  response = agent.invoke(prompt)
  file_name = 'prompt.py'
  with open (file_name, 'w') as f:
    f.write(response.content[-1]['text'])
  return "Prompt file generated successfully, agent can read it "

  #========== tool 2 ================
prompt_generator(model)
def resume_maker_prompt():
  """this fucntion just gives
  updated prompt for model"""

  with open('prompt.py', 'r') as f:
    prompt = f.read()
  return prompt
    
resume_maker_prompt()
# ========= GENERATE RESUME ==========

prompt = """You are a helpful AI assistant
with job resume maker, your task is to give
HTML format resume, with proper designing using recent css and js
code, with professional design Format.
User will upload data and return HTML format resume
Always use different styling"""

final_prompt = prompt + resume_maker_prompt()

user_details = """user details : given below :
My name is Ujjwal Raina currently studying in 2nd year ip university
course - bca . very passionate about ai and software development had completed multiple value added courses
and also done multiple certification code in the field of ai and software development participated in different high level
hackathons and competition did my schooling from kamal model sr. sec. school 12th percentage is 76 percent my email is singhabhigyan922@gmail.com"""

query = final_prompt + user_details

if st.button("Generate Resume"):
  with st.spinner("Running Agent....."):

    response = agent.invoke ({'messages':[{'role':'user','content':query}]})
    code = response['messages'][-1].content[-1]['text']

    #st.markdown(code)
    st.html(code, width = "stretch", unsafe_allow_javascript = True)
