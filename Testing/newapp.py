import os
from dotenv import load_dotenv
import streamlit as st
import genai
import google.generativeai as ggi
#import fitz
#from pypdf import PdfReader

# Assuming this is the package that requires the API key

# Load environment variables from .env file
dotenv_path = '.env.txt'
load_dotenv(dotenv_path)

# Debugging: Print out to check if the .env file is loaded correctly
if not os.path.exists(dotenv_path):
  st.error(f"The file {dotenv_path} does not exist.")
else:
  st.write(f"Loading environment variables from {dotenv_path}")

# Get the API key from environment variables
api_key = os.getenv('API_KEY')

# Debugging: Print the API key to verify it's loaded
st.write(f"Loaded API Key: {api_key}")

if not api_key:
  st.error("No API key found. Please set the API_Key environment variable.")
else:
  # Configure the genai package with the API key
  ggi.configure(api_key=api_key)
  st.success("API key successfully configured.")
  model = ggi.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat()
def LLM_Response(question):
    response = chat.send_message(question,stream=True)
    return response

st.title("Chat Application using Gemini Pro")

user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)
