import streamlit as st
import os
import datetime
import tempfile
import subprocess
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from pathlib import Path
from dotenv import load_dotenv

# Import the streamlit runner module
from src.streamlit_runner import run_with_streamlit_inputs

# Load environment variables (especially API keys)
load_dotenv()

# --- Streamlit App UI ---
st.set_page_config(page_title="Resume Optimizer AI", layout="wide")
st.title("📄✨ Resume Optimizer with CrewAI")
st.markdown("Upload your resume (.tex or .pdf), provide the job description URL or text, and get an optimized version!")

# --- Input Fields ---
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        uploaded_file = st.file_uploader("1. Upload your Resume", type=['tex', 'pdf'])
    
    with col2:
        job_input_option = st.radio(
            "2. How do you want to provide the job description?",
            ["URL", "Text Input"]
        )
        
        if job_input_option == "URL":
            job_url = st.text_input("Enter the Job Description URL")
            job_text = None
        else:
            job_url = None
            job_text = st.text_area("Paste the Job Description Text", height=150)
            
# Output directory setup
output_dir = os.path.join(os.getcwd(), "output")
os.makedirs(output_dir, exist_ok=True)

# --- Run Button ---
run_button = st.button("🚀 Optimize Resume")

if run_button:
    if not uploaded_file:
        st.error("Please upload your resume file (.tex or .pdf)")
    elif job_input_option == "URL" and not job_url:
        st.error("Please enter the job description URL")
    elif job_input_option == "Text Input" and not job_text:
        st.error("Please enter the job description text")
    else:
        # Create temporary directory for the uploaded file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save the uploaded file
            resume_filename = uploaded_file.name
            temp_resume_path = os.path.join(temp_dir, resume_filename)
            with open(temp_resume_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            # Show processing message
            if job_url:
                st.info(f"Processing '{resume_filename}' for job URL: {job_url}")
            else:
                st.info(f"Processing '{resume_filename}' with provided job description text")
            
            # --- Run the Crew ---
            with st.spinner("🤖 CrewAI is analyzing and optimizing... Please wait."):
                try:
                    # Run the optimization using our streamlit_runner module
                    result, output_file_path = run_with_streamlit_inputs(
                        resume_file_path=temp_resume_path,
                        job_url=job_url,
                        job_text=job_text,
                        output_dir=output_dir
                    )
                    
                    st.success("✅ Optimization Complete!")
                    
                    # --- Semantic Similarity Analysis Section ---
                    st.subheader("📊 Semantic Similarity Analysis")
                    
                    # Look for similarity analysis report
                    similarity_report_path = os.path.join(output_dir, "similarity_analysis_report.md")
                    similarity_content = read_report_file(similarity_report_path)
                    
                    if similarity_content:
                        # Extract similarity score
                        similarity_score = extract_similarity_score(similarity_content)
                        
                        if similarity_score is not None:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                # Display similarity gauge
                                gauge_fig = create_similarity_gauge(similarity_score)
                                if gauge_fig:
                                    st.plotly_chart(gauge_fig, use_container_width=True)
                            
                            with col2:
                                # Display interpretation chart
                                interp_fig = create_interpretation_chart(similarity_score)
                                if interp_fig:
                                    st.plotly_chart(interp_fig, use_container_width=True)
                            
                            # Display semantic analysis insights
                            st.subheader("📝 Semantic Analysis Insights")
                            with st.expander("View Full Similarity Analysis Report", expanded=False):
                                st.markdown(similarity_content)
                        else:
                            st.warning("Could not extract similarity score from the report.")
                            with st.expander("View Similarity Analysis Report", expanded=False):
                                st.markdown(similarity_content)
                    else:
                        st.info("Similarity analysis report not found. The feature may not be enabled.")
                    
                    # --- Additional Reports Section ---
                    st.subheader("📋 Detailed Analysis Reports")
                    
                    # Create tabs for different reports
                    report_tabs = st.tabs([
                        "📄 Resume Analysis", 
                        "🎯 Job Analysis", 
                        "🔧 Resume Adjustments",
                        "📊 Execution Report"
                    ])
                    
                    with report_tabs[0]:
                        # Resume analysis reports
                        extract_report_path = os.path.join(output_dir, "extract_curriculum_data_report.md")
                        extract_content = read_report_file(extract_report_path)
                        if extract_content:
                            st.markdown(extract_content)
                        else:
                            st.info("Resume analysis report not available.")
                    
                    with report_tabs[1]:
                        # Job analysis report
                        job_report_path = os.path.join(output_dir, "analyze_job_description_report.md")
                        job_content = read_report_file(job_report_path)
                        if job_content:
                            st.markdown(job_content)
                        else:
                            st.info("Job analysis report not available.")
                    
                    with report_tabs[2]:
                        # Resume adjustments report
                        adjust_report_path = os.path.join(output_dir, "adjust_resume_for_job_report.md")
                        adjust_content = read_report_file(adjust_report_path)
                        if adjust_content:
                            st.markdown(adjust_content)
                        else:
                            st.info("Resume adjustments report not available.")
                    
                    with report_tabs[3]:
                        # Execution report
                        exec_report_path = os.path.join(output_dir, "execution_report.md")
                        exec_content = read_report_file(exec_report_path)
                        if exec_content:
                            st.markdown(exec_content)
                        else:
                            st.info("Execution report not available.")
                    
                    # --- Display Result & Download ---
                    st.subheader("📥 Download Optimized Resume")
                    st.text_area("Preview (first 1000 chars):", result[:1000] + "...", height=200)
                    
                    # Get the filename from the output path
                    output_filename = os.path.basename(output_file_path)
                    
                    # Provide download for the .tex file
                    st.download_button(
                        label="📥 Download Optimized .tex File",
                        data=result.encode('utf-8'),
                        file_name=output_filename,
                        mime="text/plain" 
                    )
                    
                    # Option to compile to PDF
                    compile_to_pdf = st.checkbox("Compile to PDF (requires LaTeX installed)")
                    if compile_to_pdf:
                        try:
                            # Get base name without extension for PDF output
                            base_name = os.path.splitext(output_filename)[0]
                            pdf_filename = f"{base_name}.pdf"
                            pdf_path = os.path.join(output_dir, pdf_filename)
                            
                            # Run pdflatex to compile the .tex file
                            with st.spinner("Compiling LaTeX to PDF..."):
                                process = subprocess.run(
                                    ['pdflatex', '-output-directory', output_dir, output_file_path],
                                    capture_output=True,
                                    text=True,
                                    check=True
                                )
                                
                                # Check if PDF was created successfully
                                if os.path.exists(pdf_path):
                                    # Read the PDF file and offer for download
                                    with open(pdf_path, 'rb') as pdf_file:
                                        pdf_data = pdf_file.read()
                                    
                                    st.download_button(
                                        label="📥 Download PDF Version",
                                        data=pdf_data,
                                        file_name=pdf_filename,
                                        mime="application/pdf"
                                    )
                                else:
                                    st.error("PDF compilation failed. Check your LaTeX syntax.")
                                    st.code(process.stderr, language="bash")
                        except Exception as e:
                            st.error(f"Error during PDF compilation: {e}")
                            st.info("Make sure LaTeX (pdflatex) is installed on your system")

                except Exception as e:
                    st.error(f"An error occurred: {e}")
                    st.exception(e) # Show full traceback for debugging

# --- Similarity Analysis ---
st.markdown("---")
st.subheader("Similarity Analysis")

# Helper function to read markdown report files
def read_report_file(file_path):
    """Read a report file and return its content"""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
    except Exception as e:
        st.warning(f"Could not read report file {file_path}: {e}")
    return None

# Helper function to extract similarity score from report
def extract_similarity_score(report_content):
    """Extract similarity score from the similarity analysis report"""
    if not report_content:
        return None
    
    # Look for score patterns in the report
    import re
    patterns = [
        r"[Ss]core[:\s]*([0-9]*\.?[0-9]+)",
        r"[Ss]imilaridade[:\s]*([0-9]*\.?[0-9]+)",
        r"([0-9]*\.?[0-9]+)\s*[%]",
        r"([0-9]*\.?[0-9]+)"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, report_content)
        if match:
            try:
                score = float(match.group(1))
                # Normalize score to 0-1 range if it's in percentage
                if score > 1:
                    score = score / 100
                return score
            except:
                continue
    return None

# Helper function to create similarity visualization
def create_similarity_gauge(score):
    """Create a gauge chart for similarity score"""
    if score is None:
        return None
    
    # Create gauge chart
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = score * 100,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Resume-Job Similarity Score (%)"},
        delta = {'reference': 70},
        gauge = {
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "lightgray"},
                {'range': [30, 60], 'color': "yellow"},
                {'range': [60, 85], 'color': "lightgreen"},
                {'range': [85, 100], 'color': "green"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=300)
    return fig

# Helper function to create interpretation chart
def create_interpretation_chart(score):
    """Create a bar chart showing interpretation levels"""
    if score is None:
        return None
    
    levels = ['Poor Match\n(0-30%)', 'Fair Match\n(30-60%)', 'Good Match\n(60-85%)', 'Excellent Match\n(85-100%)']
    colors = ['red', 'orange', 'lightgreen', 'green']
    values = [30, 30, 25, 15]  # Range sizes
    
    # Determine current level
    current_score = score * 100
    current_level = 0
    if current_score >= 85:
        current_level = 3
    elif current_score >= 60:
        current_level = 2
    elif current_score >= 30:
        current_level = 1
    
    # Create highlighting
    bar_colors = ['lightgray'] * 4
    bar_colors[current_level] = colors[current_level]
    
    fig = go.Figure(data=[
        go.Bar(
            x=levels,
            y=values,
            marker_color=bar_colors,
            text=[f'{current_score:.1f}%' if i == current_level else '' for i in range(4)],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title="Similarity Interpretation",
        yaxis_title="Score Range (%)",
        height=300
    )
    
    return fig

# --- Footer/Instructions ---
st.markdown("---")
with st.expander("📋 Instructions & Requirements"):
    st.markdown("""
    ### How to Use
    1. **Upload Resume**: Choose your existing resume in `.tex` or `.pdf` format.
    2. **Job Details**: Provide either a job URL or paste the job description text.
    3. **Optimize**: Click the optimize button and wait for the AI crew to work.
    4. **Download**: Get your optimized resume in `.tex` format, or compile to PDF if LaTeX is installed.
    
    ### Requirements
    - **API Keys**: Ensure your `.env` file with API keys (GEMINI_API_KEY) is present in the project root.
    - **LaTeX**: For PDF compilation, ensure LaTeX is installed on your system.
    
    ### How It Works
    This tool uses CrewAI to coordinate multiple AI agents that work together to:
    - Read and understand your resume
    - Analyze the job requirements
    - Customize your resume to highlight relevant skills and experiences
    """)

st.sidebar.markdown("""
## Resume Optimizer
This tool helps you customize your resume for specific job opportunities.

### AI Agents:
- 📝 Curriculum Reader Agent
- 🔍 Job Analyzer Agent 
- ✍️ Resume Editor Agent
- 📊 Reporting Agent

### Process:
1. Extract Resume Data
2. Analyze Job Requirements
3. Customize Resume for Job
4. Generate Final Report
""")
