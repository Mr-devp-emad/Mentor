import streamlit as st
import io
import sys
import base64
from google import generativeai as genai

# Configure Gemini API
genai.configure(api_key="AIzaSyA2w5xa573pBt1euAR5Hpk2ma6R_oVFAQ8")

def get_ai_response(question):
    try:
        client = genai.GenerativeModel("gemini-2.0-flash")
        response = client.generate_content(question)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

def execute_python_code(code):
    try:
        output_capture = io.StringIO()
        sys.stdout = output_capture
        exec(code, {})
        sys.stdout = sys.__stdout__
        return output_capture.getvalue()
    except Exception as e:
        return f"Error: {str(e)}"

# Function to create an HTML preview for HTML & CSS
def create_html_preview(html_code, css_code=""):
    full_code = f"""
    <html>
    <head>
        <style>{css_code}</style>
    </head>
    <body>{html_code}</body>
    </html>
    """
    return "data:text/html;base64," + base64.b64encode(full_code.encode()).decode()

# Streamlit Page Config
st.set_page_config(page_title="Coding Mentor", page_icon="💻", layout="wide")

st.markdown("""
    <style>
        body { font-family: 'Arial', sans-serif; background-color: #181818; }
        .stTextArea, .stButton { border-radius: 8px; }
        .stButton > button { background-color: #4CAF50; color: white; border-radius: 8px; width: 100%; font-size: 16px; padding: 10px; }
        .stButton > button:hover { background-color: #45a049; }
        .stCodeBlock { border-radius: 8px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

st.title("👨‍💻 Coding Mentor - Learn & Practice")

language = st.sidebar.selectbox("📌 Choose Language", ["Python", "JavaScript", "TypeScript", "HTML", "CSS"])

st.subheader(f"🔍 Ask Anything About {language}")
query = st.text_area("Type your question...")
if st.button("Get Explanation"):
    if query.strip():
        st.success(get_ai_response(query))
    else:
        st.warning("Please enter a question.")

st.subheader("🛠️ Code Playground")

col1, col2, col3 = st.columns([1, 1.2, 1])

with col1:
    st.markdown("### 📜 Example Code")
    example_code = {
        "Python": "print('Hello, World!')",
        "JavaScript": "console.log('Hello, World!');",
        "TypeScript": "let message: string = 'Hello, World!'; console.log(message);",
        "HTML": "<h1>Hello, World!</h1>",
        "CSS": "h1 { color: blue; }"
    }
    st.code(example_code.get(language, ""), language.lower())

with col2:
    st.markdown("### ✍️ Code Playground")
    user_code = st.text_area("Write your code here...")

with col3:
    st.markdown("### ⚡ Output")
    if st.button("▶ Run Code"):
        if language == "Python":
            result = execute_python_code(user_code)
            st.code(result)
        elif language in ["JavaScript", "TypeScript"]:
            st.markdown(f"""
            <script>
                try {{
                    var output = eval(`{user_code}`);
                    document.getElementById("output").innerText = output;
                }} catch (err) {{
                    document.getElementById("output").innerText = "Error: " + err;
                }}
            </script>
            <div id="output" style="padding: 10px; background-color: #222; color: white; border-radius: 5px;">Output will appear here...</div>
            """, unsafe_allow_html=True)
        elif language == "HTML":
            html_preview = create_html_preview(user_code)
            st.markdown(f'<iframe src="{html_preview}" width="100%" height="300"></iframe>', unsafe_allow_html=True)
        elif language == "CSS":
            html_preview = create_html_preview("<h1>Styled Text</h1>", user_code)
            st.markdown(f'<iframe src="{html_preview}" width="100%" height="300"></iframe>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("🚀Idea By Emad Ahmed Created With The Help Of Gpt/ Self-learning and Streamlit | [GitHub](https://github.com/Mr-devp-emad/)")
