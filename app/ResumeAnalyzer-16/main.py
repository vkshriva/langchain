import streamlit as st
from typing import TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pypdf import PdfReader
from docx import Document

load_dotenv()  # Load environment variables from .env file

#Step 0: Streamlit Config (MUST be first)
st.set_page_config(page_title="Resume Analyzer", layout="centered")

#Step1 : State
class State(TypedDict):
    resume:str
    analysis:str
    feedback:str
    count:int

#Step2 : LLM
llm = ChatOpenAI()

#Step3 : Nodes
def analyze_resume(state: State):
    prompt = f"""
    You are a resume analyzer. Analyze the following resume and provide detailed improvement suggestions.
    Focus on :
    -Skills
    -Projects
    -Experience
    -Structure
    -Clarity
    -Impact

     Resume Content:
     {state['resume']}
    Give at least 5 strong suggestions for improvement.
    """
    if(state["feedback"]):
        prompt+=f"\n Previous Feedback : {state['feedback']}. Please improve the analysis based on this feedback."

    response = llm.invoke(prompt)
    return {"analysis": response.content, "count": state.get("count", 0) + 1}
    

def review_analysis(state: State):
    print(f"--Reviewing attempt {state['count']}--\n")
    lines = state["analysis"]
    if len(lines) < 200:
        return {"feedback": "Too Short. Add More Details and Suggestions."}
    if "skills" not in lines.lower():
        return {"feedback": "Missing Skills Section. Please add suggestions related to skills."}
    return {"feedback": "good"}


def should_continue(state: State):
    if state["feedback"] == "good" or state.get("count", 0) >= 3:   
        return "end"
    else:
        return "retry"


builder = StateGraph(State)

builder.add_node("analyze", analyze_resume)
builder.add_node("review", review_analysis)

builder.add_edge(START, "analyze")
builder.add_edge("analyze", "review")
builder.add_conditional_edges("review", should_continue, {
    "retry": "analyze",
    "end": END
})


graph = builder.compile()


#Step 6: Streamlit UI
st.title("Resume Analyzer")

upload = st.file_uploader("Upload your resume (PDF or DOCX)", type=["pdf", "docx"], key="resume_file")

resume_content = ""
if upload is not None:
    if upload.type == "application/pdf":
        pdf_reader = PdfReader(upload)
        for page in pdf_reader.pages:
            resume_content += page.extract_text() + "\n"
    elif upload.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(upload)
        for para in doc.paragraphs:
            resume_content += para.text + "\n"

    st.text_area("Resume Content", value=resume_content, height=200, key="resume_text")

    if st.button("Analyze Resume"):
        with st.spinner("Analyzing resume..."):
            result = graph.invoke({"resume": resume_content, "analysis": "", "feedback": "", "count": 0})
            st.subheader("Analysis Result:")
            st.text_area("Analysis", value=result["analysis"], height=200, key="analysis_result")
            st.subheader("Feedback:")
            st.text_area("Feedback", value=result["feedback"], height=100, key="feedback_result")   
            