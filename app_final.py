import openai
import streamlit as st

def suggest_code_completion(incomplete_code, language):
    api_key = os.getenv("OPENAI_API_KEY")
    openai.api_key = api_key
    
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

def download_file(content, language):
    """Generate downloadable file content based on selected language."""
    file_extension = {
        "Python": "py",
        "Java": "java",
        "TypeScript": "ts"
    }
    return f"data:text/plain;charset=utf-8,{content}", f"code_completion.{file_extension.get(language, 'txt')}"

def insert_placeholder_code(language):
    """Insert a simple placeholder code based on the selected language."""
    placeholder_code = {
        "Python": "def hello_world():\n    print('Hello, World!')",
        "Java": "public class HelloWorld {\n    public static void main(String[] args) {\n        System.out.println('Hello, World!');\n    }\n}",
        "TypeScript": "function helloWorld(): void {\n    console.log('Hello, World!');\n}"
    }
    return placeholder_code.get(language, "")

def analyze_code_quality(code):
    """Analyze the code for basic quality issues. (This is a placeholder for demonstration.)"""
    issues = []
    if 'print' not in code and 'System.out.println' not in code:
        issues.append("Consider adding output statements to show results.")
    if len(code.splitlines()) > 20:
        issues.append("Your code is quite long; consider breaking it into smaller functions.")
    return issues

# Streamlit UI
st.set_page_config(page_title="✨ Code Completion Assistant", page_icon="📝", layout="wide")

# Sidebar theme toggle
dark_mode = st.sidebar.checkbox("🌓 Enable Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
        .css-18e3th9 {background-color: #2E2E2E; color: white;}
        </style>
        """, unsafe_allow_html=True)

st.title("✨ Code Completion Assistant")

# Dropdown for selecting programming language
language = st.selectbox("🛠️ Select the programming language:", ["Python", "Java", "TypeScript"])

# Text area for input with placeholder
incomplete_code = st.text_area("📝 Enter your incomplete code here:", height=200, help="Paste your incomplete code here or use the placeholder code below.", value=insert_placeholder_code(language))

# History for previous inputs
if 'history' not in st.session_state:
    st.session_state.history = []

if st.button("🤖 Suggest Completion"):
    if incomplete_code.strip():
        with st.spinner("Fetching suggestions..."):
            try:
                completion = suggest_code_completion(incomplete_code, language)
                st.subheader("💡 Suggested Completion:")
                st.code(completion, language=language.lower())
                
                # Save to history
                st.session_state.history.append((language, incomplete_code, completion))
                
                # Provide download option
                download_link, filename = download_file(completion, language)
                st.download_button("📥 Download Suggested Code", download_link, file_name=filename)
                
                # Analyze code quality
                issues = analyze_code_quality(incomplete_code)
                if issues:
                    st.warning("⚠️ Code Quality Suggestions:")
                    for issue in issues:
                        st.write(f"- {issue}")
                else:
                    st.success("✅ Your code looks good!")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.error("❌ Please enter some code!")

# Show history with a clear option
if st.session_state.history:
    st.subheader("🗂️ Previous Inputs and Suggestions:")
    for lang, code, suggestion in st.session_state.history:
        st.write(f"**Language:** {lang}")
        st.code(code, language=lang.lower())
        st.write(f"**Suggestion:**")
        st.code(suggestion, language=lang.lower())
        st.markdown("---")
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.success("History cleared.")

# Sidebar for additional information and links
st.sidebar.header("ℹ️ About")
st.sidebar.write(
    "This application help users complete and optimize their code. "
    "Select a programming language, input your incomplete code, and get suggestions instantly!"
)
st.sidebar.write("### Example Projects:")
st.sidebar.write("- [Python Examples](https://www.python.org/doc/)")
st.sidebar.write("- [Java Examples](https://docs.oracle.com/javase/tutorial/)")
st.sidebar.write("- [TypeScript Examples](https://www.typescriptlang.org/docs/)")

# Adding example snippets for each language
st.sidebar.write("### Example Code Snippets:")
if st.sidebar.button("🔍 Show Example Snippet"):
    example_snippets = {
        "Python": "```python\ndef add(a, b):\n    return a + b\n```",
        "Java": "```java\npublic class Example {\n    public static void main(String[] args) {\n        System.out.println('Hello World');\n    }\n}```",
        "TypeScript": "```typescript\nfunction add(a: number, b: number): number {\n    return a + b;\n}```"
    }
    st.sidebar.markdown(example_snippets[language])

