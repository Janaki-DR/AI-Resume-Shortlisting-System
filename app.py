import streamlit as st 
st.set_page_config(page_title="AI Hiring System")
st.title("AI-Based Resume Shortlisting System")
st.write("Company Hiring Portal")
roles={
    "AI/ML Engineer":["python", "machine learning", "deep learning", "sgl"],
    "Data Scientist":["python", "statistics", "data analysis", "sql"],
    "Data Analyst":["sql", "excel", "power bi", "python"],
}
selected_role=st.selectbox("Select Job Role", list(roles.keys()))
threshold=st.slider("set selection threshold (%)", 50, 100, 70)
resume_text=st.text_area("Paste Cndidate Resume Here")
if st.button("Analyze Resume"):
    if resume_text.strip()=="":
        st.warning("Please paste resume text first.")
    else:
        resume_text=resume_text.lower()
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
            
st.write("---")
st.caption("This system assissts HR in resume screening. Final hiring decisions require human evaluation.")

            
            
            