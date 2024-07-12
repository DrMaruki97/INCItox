import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as ggi

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
    try:
        response = chat.send_message(question, stream=True)
        parts = []
        for word in response:
            if hasattr(word, 'text'):
                parts.append(word.text)
            else:
                st.error("No text part in response.")
                return []
        
        # Log the raw response for debugging
        st.write("Raw Response:", response)

        if not parts:
            # Check for safety ratings
            if hasattr(response, 'safety_ratings') and response.safety_ratings:
                st.error(f"Response was blocked due to safety ratings: {response.safety_ratings}")
            else:
                st.error("No valid response generated.")
            return []
        
        return parts
    except ValueError as ve:
        st.error(f"ValueError: {ve}")
    except Exception as e:
        st.error(f"Error in generating response: {e}")
    return []

st.title("Chat Application using Gemini Pro")

user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = LLM_Response(user_quest)
    if result:
        st.subheader("Response : ")
        for word in result:
            st.text(word)
    else:
        st.error("No valid response generated.")
