import streamlit as st
import requests
from auth import auth_ui, logout_button
from auth_db import save_history, get_user_history, delete_history_entry
from fpdf import FPDF
from datetime import datetime
import base64
import pandas as pd

st.set_page_config(page_title="SkillMatch.AI", page_icon="🧠", layout="centered")

# Custom styles
st.markdown("""
    <style>
        body { background-color: #f5f7fa; }
        .title {
            text-align: center;
            font-size: 3em;
            font-weight: 700;
            background: -webkit-linear-gradient(#ff416c, #ff4b2b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2em;
            color: #5e5e5e;
            margin-bottom: 30px;
        }
        .stTextInput > label, .stFileUploader > label, .stTextArea > label {
            font-weight: bold;
            color: #ff4b4b;
        }
    </style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    auth_ui()
    st.stop()

logout_button()

st.markdown('''
    <div style="text-align:center; font-size: 3em;">
        📄 <span style="
            font-weight:700;
            background: -webkit-linear-gradient(#ff416c, #ff4b2b);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        ">SkillMatch.AI</span>
    </div>
''', unsafe_allow_html=True)
st.markdown('<div class="subtitle">✨ Smart Resume Analyzer That Matches You To Your Dream Job ✨</div>', unsafe_allow_html=True)
st.markdown("---")

st.subheader("📝 Job Description")
jd = st.text_area("Paste the Job Description:", height=250)

st.subheader("📁 Resume Upload")
file = st.file_uploader("Upload your Resume (PDF or DOCX)", type=["pdf", "docx"])

def create_pdf(skills, score, username):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="SkillMatch.AI Resume Report", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"User: {username}", ln=True)
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Extracted Skills:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=", ".join(skills))
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(200, 10, txt="Match Score:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"{score}%", ln=True)
    return pdf.output(dest='S').encode('latin1')

if file and jd:
    with st.spinner("🔍 Analyzing your resume..."):
        response = requests.post(
            "https://skillmatch-ai-mllr.onrender.com",
            data={"jd": jd},
            files={"file": (file.name, file, file.type)}
        )
        result = response.json()
        st.success("✅ Analysis Complete!")

        st.markdown("### 📌 Extracted Skills")
        st.code(", ".join(result["skills"]), language="text")

        st.markdown("### 📊 Resume–JD Match Score")
        st.metric(label="Score", value=f"{result['match_score']}%")

        save_history(st.session_state.username, result["skills"], result["match_score"])

        pdf_bytes = create_pdf(result["skills"], result["match_score"], st.session_state.username)
        b64 = base64.b64encode(pdf_bytes).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="SkillMatch_Report.pdf">📥 Download Report (PDF)</a>'
        st.markdown(href, unsafe_allow_html=True)

# Dashboard
st.markdown("---")
st.subheader("📂 Your Resume Analysis History")

history = get_user_history(st.session_state.username)

if not history:
    st.info("No previous resume analyses found.")
else:
    st.markdown("### 📈 Match Score Trend")
    history_data = pd.DataFrame({
        "Date": [entry.date for entry in history],
        "Score": [float(entry.score) for entry in history]
    }).sort_values("Date")
    st.line_chart(history_data.set_index("Date"))

    st.markdown("### 📋 History Log")
    for entry in history:
        col1, col2 = st.columns([6, 1])
        with col1:
            st.markdown(f"""
            **🗓 Date:** {entry.date.strftime('%Y-%m-%d %H:%M')}  
            **📌 Skills:** {entry.skills}  
            **📊 Score:** {entry.score}%  
            """)
        with col2:
            if st.button("🗑️ Delete", key=f"del-{entry.id}"):
                delete_history_entry(entry.id)
                st.rerun()

