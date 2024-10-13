import openai
import streamlit as st

def suggest_code_completion(incomplete_code, language):
    # Make sure your API key is set up correctly
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    
    # Use the correct method for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are an assistant that helps users complete and optimize their code in {language}."},
            {"role": "user", "content": f"Here's the incomplete code in {language}:\n{incomplete_code}\nCan you help me complete it?"}
        ],
        temperature=0.7,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    return response['choices'][0]['message']['content']

# Streamlit UI
st.title("Code Completion Assistant")

# Dropdown for selecting programming language
language = st.selectbox("Select the programming language:", ["Python", "Java", "TypeScript"])

# Text area for input
incomplete_code = st.text_area("Enter your incomplete code here:", height=200)

if st.button("Suggest Completion"):
    if incomplete_code:
        try:
            completion = suggest_code_completion(incomplete_code, language)
            st.subheader("Suggested Completion:")
            st.code(completion, language=language.lower())  # Use lowercase for syntax highlighting
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.error("Please enter some code!")
