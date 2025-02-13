import streamlit as st
import google.generativeai as genai
import os
import json

# Load API key from text file
def load_api_key():
    try:
        with open("API_key.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        st.error("API key file 'API_key.txt' not found.")
        return None

# Function to review the code using Google Generative AI (Gemini)
def review_code(code):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(f"Review this Python code and suggest improvements:\n\n{code}")
        return response.text
    except Exception as e:
        st.error(f"Error while reviewing code: {e}")
        return None

# Function to handle .ipynb files
def process_ipynb(file):
    try:
        notebook_content = json.load(file)
        code_cells = [cell['source'] for cell in notebook_content['cells'] if cell['cell_type'] == 'code']
        return "\n\n".join(["".join(cell) for cell in code_cells])
    except Exception as e:
        st.error(f"Error processing .ipynb file: {e}")
        return None

# Streamlit UI Creation
st.title("AI-Powered Python Code Reviewer")
st.subheader("Submit your Python code for AI-powered bug detection and improvements.")

# Load API Key
api_key = load_api_key()
if api_key:
    genai.configure(api_key=api_key)

# Input: Either Text Area or File Upload
user_code = st.text_area("Enter your Python code here:", height=150)

# File uploader for both .py and .ipynb files
uploaded_file = st.file_uploader("Or upload a .py or .ipynb file", type=["py", "ipynb"])

if uploaded_file:
    # Read file and process depending on type
    if uploaded_file.name.endswith('.py'):
        user_code = uploaded_file.read().decode("utf-8")
    elif uploaded_file.name.endswith('.ipynb'):
        user_code = process_ipynb(uploaded_file)

# Review Code Button
if st.button("Review Code"):
    if user_code.strip():
        with st.spinner("Analyzing your code..."):
            feedback = review_code(user_code)  # Get AI-generated feedback
            if feedback:
                # Display results
                st.subheader("Code Review & Suggestions")
                st.write(feedback)
            else:
                st.error("Could not generate code review.")
    else:
        st.warning("Please enter or upload Python code before submitting.")
