import streamlit as st
from resume_analyzer import extract_text, analyze_resume

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="centered"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and check how well it matches a job description.")

st.divider()

uploaded_file = st.file_uploader(
    "Upload your Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    placeholder="Example: We are looking for a Python developer with SQL and Machine Learning skills...",
    height=180
)

if st.button("Analyze Resume", type="primary"):

    if uploaded_file is None:
        st.warning("Please upload your resume first.")

    elif not job_description.strip():
        st.warning("Please enter a job description.")

    else:
        try:
            with st.spinner("Analyzing your resume..."):
                resume_text = extract_text(uploaded_file)

                if not resume_text.strip():
                    st.error("No readable text found. Please upload a text-based PDF.")
                else:
                    found_skills, missing_skills, score = analyze_resume(
                        resume_text,
                        job_description
                    )

                    st.subheader("📊 Analysis Results")

                    st.metric("Resume Match Score", f"{score}%")
                    st.progress(min(score / 100, 1.0))

                    st.subheader("✅ Skills Found in Resume")

                    if found_skills:
                        st.write(", ".join(found_skills))
                    else:
                        st.write("No predefined skills detected.")

                    st.subheader("❌ Missing Required Skills")

                    if missing_skills:
                        st.write(", ".join(missing_skills))
                    else:
                        st.success("All detected required skills are present!")

                    st.info(
                        "The match score measures text similarity. "
                        "It is not a guarantee of job selection."
                    )

        except Exception as error:
            st.error(f"An error occurred: {error}")