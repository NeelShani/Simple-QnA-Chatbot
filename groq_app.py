import streamlit as st

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
 
import os
from dotenv import load_dotenv

load_dotenv()

##lansmith tracking 
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"] = "Simple QnA Chatbot with Groq"
 
 
##prompt template

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistance, please response to the user queries."),
    ("user","Question:{question}")
])

def generate_resonse(question, api_key, llm, temperature, max_tokens):
    llm = ChatGroq(model=llm, groq_api_key=api_key)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer

## Title of the app

st.title("Q&A Chatbot with Groq")

## sidebar for setting

st.sidebar.title("Setting")
api_key = st.sidebar.text_input("Enter your Groq API Key", type="password")

# Drop down to select the model
llm =st.sidebar.selectbox("Select an Open AI Model", ["llama3-groq-70b-8192-tool-use-preview", "llama3-groq-8b-8192-tool-use-preview"])

temperature = st.sidebar.slider("Creativity",min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Token",min_value=50, max_value=300, value=150)

#Main interface for user input
st.write("Ask your question")
user_input = st.text_input("You:")

if user_input:
    response = generate_resonse(user_input, api_key, llm, temperature, max_tokens)
    st.write(response)
elif user_input:
    st.warning("Please enter the Groq API key in the side bar")
else:
    st.write("Please ask the qustions")