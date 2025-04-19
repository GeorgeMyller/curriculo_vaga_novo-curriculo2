import streamlit as st
import os
import datetime
import tempfile
from dotenv import load_dotenv

# Assuming your main crew logic is callable from src.main or src.crew
# Adjust the import based on how your project is structured
# Option 1: If main.py has a function to run the crew
# from src.main import run_crew 
# Option 2: If crew.py has the crew setup
from src.crew import create_crew # We might need to refactor crew.py to expose a function

# Load environment variables (especially API keys)
load_dotenv()

# --- Streamlit App UI ---
st.set_page_config(page_title="Resume Optimizer AI", layout="wide")
st.title("📄✨ Resume Optimizer with CrewAI")
st.markdown("Upload your resume (.tex), provide the job description URL, and get an optimized version!")

# --- Input Fields ---
uploaded_file = st.file_uploader("1. Upload your Resume (.tex file)", type=['tex'])
job_url = st.text_input("2. Enter the Job Description URL")

# --- Run Button ---
if st.button("🚀 Optimize Resume"):
    if uploaded_file is not None and job_url:
        # Create temporary directory for the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the uploaded .tex file
            resume_filename = uploaded_file.name
            temp_resume_path = os.path.join(temp_dir, resume_filename)
            with open(temp_resume_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            st.info(f"Processing '{resume_filename}' for job: {job_url}")
            
            # Prepare inputs for the crew
            inputs = {
                'resume_path': temp_resume_path,
                'job_url': job_url
            }

            # --- Run the Crew ---
            with st.spinner("🤖 CrewAI is analyzing and optimizing... Please wait."):
                try:
                    # --- Refactoring Needed ---
                    # We need a way to get the crew and run it. 
                    # Let's assume create_crew() returns the configured crew object
                    # And main.py's logic is adapted or called here.
                    
                    # Example: Instantiate and run the crew
                    resume_crew = create_crew() # Assuming this function exists in src/crew.py
                    result = resume_crew.kickoff(inputs=inputs)
                    
                    st.success("✅ Optimization Complete!")
                    
                    # --- Display Result & Download ---
                    st.subheader("Optimized Resume (.tex)")
                    st.text_area("Preview (first 1000 chars):", result[:1000] + "...", height=200)
                    
                    # Prepare filename for download
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    output_filename = f"optimized_{os.path.splitext(resume_filename)[0]}_{timestamp}.tex"
                    
                    st.download_button(
                        label="📥 Download Optimized .tex File",
                        data=result.encode('utf-8'), # Encode result to bytes
                        file_name=output_filename,
                        mime="text/plain" 
                    )

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.exception(e) # Show full traceback for debugging

    else:
        st.warning("Please upload a .tex resume and enter a job URL.")

# --- Footer/Instructions ---
st.markdown("---")
st.markdown("**Note:** Ensure your `.env` file with API keys is present in the project root.")
