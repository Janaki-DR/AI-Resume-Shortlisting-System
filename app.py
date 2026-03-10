import streamlit as st
import pdfplumber
import docx
import nltk 
import re
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
stop_words=set(stopwords.words("english"))
def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
               text += page.extract_text()
    return text
def extract_text_from_docx(file): 
    doc = docx.Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text 
    return text
def preprocess_text(text):
    text=text.lower()
    
    tokens=word_tokenize(text)
    
    filtered_words=[]
    for word in tokens:
        if word.isalpha() and word not in stop_words:
            filtered_words.append(word)
    return filtered_words
def calculate_experience(text):
    match=re.search(r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)', text.lower())
    if match:
        return int(match.group(1))
    if re.search(r'\bfresher\b|\bfresh graduate\b|\bno experience\b', text.lower()):
        return 0
    return None
st.set_page_config(page_title="AI Hiring System")
st.title("AI-Based Resume Shortlisting System")
st.write("Company Hiring Portal")
roles={
    "AI/ML Engineer":["python", "machine learning", "deep learning", "sql"],
    "Data Scientist":["python", "statistics", "data analysis", "sql"],
    "Data Analyst":["sql", "excel", "power bi", "python"],
}
selected_role=st.selectbox("Select Job Role", list(roles.keys()))
threshold=st.slider("set selection threshold (%)", 50, 100, 70)
uploaded_file = st.file_uploader("Upload Candidate Resume", type=["pdf", "docx"])
if st.button("Analyze Resume"):
    if uploaded_file is None:
        st.warning("Please upload a resume file.")
    else:
        if uploaded_file.type == "application/pdf":
            resume_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            resume_text = extract_text_from_docx(uploaded_file)
            
            
            resume_text=resume_text.lower()
            processed_words=preprocess_text(resume_text)
            required_skills=roles[selected_role]
            matched_count=0
            matched_skills=[]
            missing_skills=[]
            for skill in required_skills:
                if skill in resume_text:
                    matched_count+=1
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)
            total_skills=len(required_skills)
            match_percentage=(matched_count/total_skills)*100 
            st.subheader("Evaluation Result")
            st.write(f"Match Percentage:{round(match_percentage, 2)}%")
            st.write("Matched Skills:", matched_skills)
            st.write("Missing Skills:", missing_skills)
            if match_percentage>=threshold:
                st.success("The Candidate has been shortlisted for the interview.")
            else:
                st.error("The Candidate does not meet the required skill threshold.")
            
            exp_years=calculate_experience(resume_text)
            st.subheader("years of experience")
            if exp_years is None or exp_years==0:
                st.info("fresher")
            else:         
                st.success(f"{exp_years} years")
    
st.write("---")
st.caption("This system assists HR in resume screening. Final hiring decisions require human evaluation.")

            
            

            
