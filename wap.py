import streamlit as st
import google.generativeai as genai
import graphviz

# -------------------------------
# Gemini API Setup
# -------------------------------
GEMINI_API_KEY = "AIzaSyCTK6i0B4554jLwUx2IbnZcYVlb2mAD7sw"  # <-- put your Gemini key here
genai.configure(api_key=GEMINI_API_KEY)
model_instance = genai.GenerativeModel("gemini-1.5-flash")

# -------------------------------
# Helper: Call Gemini
# -------------------------------
def gemini_generate(prompt):
    response = model_instance.generate_content(prompt)
    return response.text if response and response.text else "⚠️ No response from Gemini."

# -------------------------------
# Helper: Function Flow (Graphviz)
# -------------------------------
def generate_function_flow(code):
    prompt = f"""
    Analyze this code and extract function call relationships.
    Return them strictly in format 'caller -> callee', one per line.
    Example:
    main -> helper
    helper -> calculate
    """
    response = model_instance.generate_content(prompt)
    edges = response.text.strip().splitlines()

    dot = graphviz.Digraph()
    for edge in edges:
        if "->" in edge:
            caller, callee = edge.split("->")
            dot.edge(caller.strip(), callee.strip())
    return dot

# -------------------------------
# Streamlit UI
# -------------------------------
st.set_page_config(page_title="AI Code Analyzer", page_icon="💻", layout="wide")
st.title("💻 AI Code Analyzer")
st.write("Explain, fix, and translate code  🚀")

tab1, tab2, tab3 = st.tabs(["📖 Explain Code", "🛠 Fix Errors", "🌍 Translate Code"])

# -------------------------------
# Tab 1: Explain Code
# -------------------------------
with tab1:
    st.subheader("📖 Explain Code")
    uploaded_file = st.file_uploader("Upload a code file", type=["py", "java", "cpp", "js"])
    code_input = st.text_area("Or paste your code here:", height=200)

    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")

    if st.button("Explain"):
        if code_input.strip():
            with st.spinner("🔎 Analyzing code ...."):
                explanation = gemini_generate(
                    f"Explain this code in detail, classify variables, functions, classes, loops, and conditions. "
                    f"Use emojis/icons for clarity. Also provide a step-by-step algorithm.\n\nCode:\n{code_input}"
                )
                algorithm = gemini_generate(f"Write a step-by-step algorithm for this code:\n{code_input}")
                flowchart = generate_function_flow(code_input)

                st.success("✅ Code Explanation:")
                st.write(explanation)

                st.info("🧩 Algorithm (Step-by-step):")
                st.write(algorithm)

                st.info("📊 Function Call Flow:")
                st.graphviz_chart(flowchart)
        else:
            st.warning("⚠️ Please upload or paste code.")

# -------------------------------
# Tab 2: Fix Errors
# -------------------------------
with tab2:
    st.subheader("🛠 Fix Errors")
    code_input = st.text_area("Paste your buggy code here:", height=200)

    if st.button("Fix"):
        if code_input.strip():
            with st.spinner("🔧 Fixing code with Gemini..."):
                fixed_code = gemini_generate(
                    f"Check this code for errors. "
                    f"If errors exist, return ONLY corrected code. "
                    f"If no errors, return exactly: '✅ No errors or bugs found in this program.'\n\nCode:\n{code_input}"
                )
                bug_summary = gemini_generate(
                    f"List only the bugs fixed in this code. "
                    f"If no errors, return exactly: 'No bugs were fixed.'\n\nCode:\n{code_input}"
                )

                st.success("✅ Corrected / Fixed Code:")
                st.code(fixed_code, language="python")

                st.info("🐞 Bugs Fixed:")
                st.write(bug_summary)

                st.download_button("📋 Copy Fixed Code", fixed_code, file_name="fixed_code.py")
        else:
            st.warning("⚠️ Please paste some code.")

# -------------------------------
# Tab 3: Translate Code
# -------------------------------
with tab3:
    st.subheader("🌍 Translate Code")
    code_input = st.text_area("Paste your code here:", height=200)
    target_lang = st.selectbox("Translate to:", ["Python", "Java", "C++", "JavaScript"])

    if st.button("Translate"):
        if code_input.strip():
            with st.spinner("🌍 Translating code with Gemini..."):
                translation = gemini_generate(
                    f"Translate this code into {target_lang}. Return ONLY the translated code:\n\n{code_input}"
                )
                st.success(f"✅ Code Translated to {target_lang}:")
                st.code(translation, language=target_lang.lower())
                st.download_button("📋 Copy Translated Code", translation, file_name=f"translated_code.{target_lang.lower()}")
        else:
            st.warning("⚠️ Please paste some code.")
