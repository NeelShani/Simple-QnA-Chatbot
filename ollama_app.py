import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.llms import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
 
import os
from dotenv import load_dotenv

load_dotenv()

##lansmith tracking 
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_PROJECT"] = "Simple QnA Chatbot with OLLAMA"

 
 
##prompt template

prompt = ChatPromptTemplate.from_messages([
    ("system","You are a helpful assistance, please response to the user queries."),
    ("user","Question:{question}")
])

def generate_resonse(question, engine, temperature, max_tokens):
    llm = Ollama(model=engine)
    output_parser=StrOutputParser()
    chain=prompt|llm|output_parser
    answer = chain.invoke({'question':question})
    return answer


## Title of the app

st.title("Q&A Chatbot with Ollama")

# Drop down to select the model
engine =st.sidebar.selectbox("Select an Open AI Model", ["mistral", "gemma2:2b"])

temperature = st.sidebar.slider("Creativity",min_value=0.0, max_value=1.0, value=0.7)
max_tokens = st.sidebar.slider("Max Token",min_value=50, max_value=300, value=150)

#Main interface for user input
st.write("Ask your question")
user_input = st.text_input("You:")

if user_input:
    response = generate_resonse(user_input, engine, temperature, max_tokens)
    st.write(response)
    
else:
    st.write("Please ask the qustions")