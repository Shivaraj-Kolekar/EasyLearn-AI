import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS  # Updated import
from langchain.chains.question_answering import load_qa_chain
import datetime
import json
import os
from google.oauth2 import service_account
# New helper functions
def save_study_session(notes, flashcards, summary):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    session_data = {
        "timestamp": timestamp,
        "notes": notes,
        "flashcards": flashcards,
        "summary": summary
    }
    
    if not os.path.exists("study_sessions"):
        os.makedirs("study_sessions")
        
    with open(f"study_sessions/session_{timestamp}.json", "w") as f:
        json.dump(session_data, f)

def generate_study_notes(text, Apikey):
    prompt = """Generate comprehensive study notes from the following text. 
    Include: 
    1. Main concepts
    2. Key points
    3. Important definitions
    4. Examples
    Format it in a clear, structured manner:"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=Apikey,
        temperature=0.5
    )
    response = llm.invoke(prompt + text)
    return response.content

def generate_summary(text, Apikey):
    prompt = "Generate a concise summary of the main points from the following text:"
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=Apikey,
        temperature=0.3
    )
    response = llm.invoke(prompt + text)
    return response.content

def generate_questions(experience,questions_count, interview_type, difficulty, skills, api_key, jobrole):
    prompt = f"""Generate interview questions based on:
    Job Role: {jobrole}
    Experience: {experience} years
    Skills: {skills}
    Interview: {interview_type}
    Number of Questions: {questions_count}
    and ask all the questions based on the Difficulty: {difficulty}    
"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",  # Updated model name
        google_api_key=api_key,
        temperature=0.7
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating questions: {str(e)}"

# Add this new function for answer evaluation
def evaluate_answer(question, user_answer, api_key):
    prompt = f"""Evaluate this interview answer:
    Question: {question}
    Candidate's Answer: {user_answer}
    
    Provide feedback in this format:
    Score (0-10): <score>
    Strengths: <what was good>
    Areas for Improvement: <what could be better>
    Sample Better Answer: <example of a strong answer>
    """
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.3
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error evaluating answer: {str(e)}"

# Update the generate_questions function
def generate_questions(experience, questions_count, interview_type, difficulty, skills, api_key, jobrole):
    prompt = f"""Generate {questions_count} interview questions based on:
    Job Role: {jobrole}
    Experience Level: {experience} years
    Skills: {skills}
    Interview Type: {interview_type}
    Difficulty Level: {difficulty}/5
    
    Format each question as:
    Q<number>. <question>
    Context: <brief context or why this is important>
    Expected Answer Points:
    - <key point 1>
    - <key point 2>
    - <key point 3>
    
    Make questions practical and scenario-based."""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=api_key,
        temperature=0.7
    )
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error generating questions: {str(e)}"

# Update the mock interview tab section in main()
def generate_practice_quiz(text, Apikey, num_questions=5):
    prompt = f"""Generate {num_questions} multiple-choice questions based on the text. 
    Format: Q: question
    A) option1
    B) option2
    C) option3
    D) option4
    Correct: letter"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=Apikey,
        temperature=0.7
    )
    response = llm.invoke(prompt + text)
    return response.content

def generate_flashcards(text, Apikey, num_cards):
    prompt = f"""Generate {num_cards} flashcards from the following text.
    Format each flashcard as:
    Q: <question>|A: <answer>
    
    Make sure each card tests understanding of key concepts.
    Text: {text}"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=Apikey,
        temperature=0.7
    )
    try:
        response = llm.invoke(prompt)
        # Split the response into individual flashcards
        cards = [card.strip() for card in response.content.split('\n') if card.strip()]
        return cards
    except Exception as e:
        st.error(f"Error generating flashcards: {str(e)}")
        return []

def main():
    st.set_page_config(page_title="AI Study Companion", layout="wide")
    
    # Sidebar
    st.sidebar.header("📚 AI STUDY COMPANION")
    
    # Session State initialization
    if 'study_notes' not in st.session_state:
        st.session_state.study_notes = []
    if 'current_flashcards' not in st.session_state:
        st.session_state.current_flashcards = []
    if 'summary' not in st.session_state:
        st.session_state.summary = ""
        
    # Main interface
    tabs = st.tabs(["📖 Study Material", "🗂️ Flashcards", "📝 Notes", "❓ Quiz", "💭 Chat", "🧑‍💻 Mock interview"])
    
    pdf = st.sidebar.file_uploader("Upload Study Material (PDF)", type='pdf')
    Apikey = st.sidebar.text_input("Enter API Key", type="password")
    
    if pdf is not None and Apikey:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
            
        text_splitter = CharacterTextSplitter(
            separator='\n',
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)
        
        # Study Material Tab
        with tabs[0]:
            st.header("📖 Study Material")
            if st.button("Generate Study Notes"):
                with st.spinner("Generating comprehensive study notes..."):
                    study_notes = generate_study_notes(text, Apikey)
                    st.session_state.study_notes = study_notes
                    st.markdown(study_notes)
                    
            if st.button("Generate Summary"):
                with st.spinner("Generating summary..."):
                    summary = generate_summary(text, Apikey)
                    st.session_state.summary = summary
                    st.markdown(summary)
        
        # Flashcards Tab
        with tabs[1]:
            st.header("🗂️ Flashcards")
            num_cards = st.number_input("Number of flashcards", 1, 20, 5)
            if st.button("Generate Flashcards"):
                with st.spinner("Creating flashcards..."):
                    flashcards = generate_flashcards(text, Apikey, num_cards)
                    st.session_state.current_flashcards = flashcards
                    for i, card in enumerate(flashcards, 1):
                        if '|' in card:
                            question, answer = card.split('|')
                            with st.expander(f"📋 {question.replace('Q:', '').strip()}"):
                                st.write(answer.replace('A:', '').strip())
        
        # Notes Tab
        with tabs[2]:
            st.header("📝 Personal Notes")
            personal_notes = st.text_area("Add your notes here")
            if st.button("Save Study Session"):
                save_study_session(
                    personal_notes,
                    st.session_state.current_flashcards,
                    st.session_state.summary
                )
                st.success("Study session saved successfully!")
        
        # Quiz Tab
        with tabs[3]:
            st.header("❓ Practice Quiz")
            if st.button("Generate Quiz"):
                with st.spinner("Creating quiz..."):
                    quiz = generate_practice_quiz(text, Apikey)
                    st.markdown(quiz)
        
        # Chat Tab
        with tabs[4]:
            st.header("💭 Ask Questions")
            user_question = st.chat_input("Ask anything about the material...")
            if user_question:
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=Apikey
                )
                knowledge_base = FAISS.from_texts(chunks, embeddings)
                docs = knowledge_base.similarity_search(user_question)
                
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=Apikey,
                    temperature=0.7
                )
                chain = load_qa_chain(llm, chain_type="stuff")
                response = chain.run(input_documents=docs, question=user_question)
                
                st.write("You: ", user_question)
                st.write("AI: ", response)

        with tabs[5]:
            st.header("🎯 Mock Interview Generator")
            
            # Interview Configuration
            col1, col2 = st.columns(2)
            with col1:
                jobrole = st.text_input("Job Role", placeholder="e.g., Senior Python Developer")
                experience = st.number_input("Years of Experience", min_value=0, max_value=50, value=0)
                questions_count = st.number_input("Number of Questions", min_value=1, max_value=10, value=5)
            
            with col2:
                interview_type = st.selectbox("Interview Type", 
                    ["Technical", "Behavioral", "System Design", "Problem Solving", "Leadership"])
                difficulty = st.slider("Difficulty Level", min_value=1, max_value=5, value=3)
                skills = st.text_area("Required Skills", placeholder="Python, SQL, AWS, etc.")

            if st.button("Start Mock Interview", type="primary"):
                if not all([jobrole, skills]):
                    st.warning("Please fill in all required fields")
                else:
                    # Initialize or get session state for tracking questions and answers
                    if 'current_question_idx' not in st.session_state:
                        st.session_state.current_question_idx = 0
                    if 'interview_questions' not in st.session_state:
                        with st.spinner("Generating interview questions..."):
                            st.session_state.interview_questions = generate_questions(
                                experience, questions_count, interview_type, 
                                difficulty, skills, Apikey, jobrole
                            )
                    
                    # Display current question
                    questions = st.session_state.interview_questions
                    st.markdown("### Current Question")
                    st.markdown(questions)
                    
                    # Answer section
                    user_answer = st.text_area(
                        "Your Answer",
                        placeholder="Type your answer here...",
                        height=150
                    )
                    
                    col1, col2 = st.columns([1, 5])
                    with col1:
                        if st.button("Submit Answer"):
                            if user_answer:
                                with st.spinner("Evaluating your answer..."):
                                    feedback = evaluate_answer(
                                        questions,
                                        user_answer,
                                        Apikey
                                    )
                                    st.markdown("### Feedback")
                                    st.markdown(feedback)
                            else:
                                st.warning("Please provide an answer before submitting")
                    
                    with col2:
                        if st.button("End Interview"):
                            st.session_state.current_question_idx = 0
                            st.session_state.interview_questions = None
                            st.success("Interview session ended!")

    else:
        st.title("🎓 Welcome to AI Study Companion!")
        st.write("""
        ### Features:
        - 📖 Generate comprehensive study notes
        - 🗂️ Create interactive flashcards
        - 📝 Take and save personal notes
        - ❓ Practice with AI-generated quizzes
        - 💭 Chat with AI about the study material
        
        To begin, upload a PDF and enter your API key in the sidebar.
        """)

if __name__ == "__main__":
    main()