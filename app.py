from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from prompt import *

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Function to generate README using LLM
def generate_readme(project_name, requirements, code_snippet):
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-002", temperature=1, api_key=GOOGLE_API_KEY)
    PROMPT_TEMPLATE = PROMPT
    prompt = PromptTemplate(
        input_variables=["project_name", "requirements", "code_snippet"],
        template=PROMPT_TEMPLATE,
    )
    llm_chain = LLMChain(llm=llm, prompt=prompt)
    response = llm_chain.run({
        "project_name": project_name,
        "requirements": requirements,
        "code_snippet": code_snippet,
    })
    return response

# Streamlit App Configuration
st.set_page_config(page_title="README Generator", layout="wide")
st.header("Manual Input README Generator")

# Input Fields
project_name = st.text_input("Enter the Project Name", placeholder="e.g., My Awesome Project")
requirements = st.text_area("Enter the Requirements", placeholder="e.g., Python 3.9, Flask, NumPy")
code_snippet = st.text_area("Enter the Code Snippet", placeholder="Paste a code snippet or example usage here")

# Generate README
if st.button("Generate README"):
    if not project_name.strip():
        st.error("Please provide a project name.")
    elif not requirements.strip():
        st.error("Please provide requirements.")
    elif not code_snippet.strip():
        st.error("Please provide a code snippet.")
    else:
        try:
            # Generate README
            readme_content = generate_readme(project_name, requirements, code_snippet)
            
            # Display the README and provide download options
            st.subheader("Generated README:")
            st.text_area("README Content", readme_content, height=400)

            st.download_button(
                label="Download as README.md",
                data=readme_content,
                file_name="README.md",
                mime="text/markdown",
            )
        except Exception as e:
            st.error(f"Failed to generate README: {e}")
