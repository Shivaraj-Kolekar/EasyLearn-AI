import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain

def generate_flashcards(text,Apikey, num_cards):
    # Create a prompt for flashcard generation
    flashcard_prompt = f"""Generate {num_cards} flashcards from the following text in such a way that the flashcards should be able to explain the complete concept in depth and detailed manner and also imrpve the user learning. 
    Format each flashcard as 'Q: <question> | A: <answer>':
    {text}"""
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        google_api_key=Apikey,
        temperature=0.7
    )
    
    response = llm.invoke(flashcard_prompt)
    # Split the response into individual flashcards
    flashcards = [card.strip() for card in response.content.split('\n') if card.strip()]
    return flashcards

def main():
    
    st.set_page_config(page_title="PDF Flashcards Generator")
    st.sidebar.header("PDF FLASHCARDS")
    
    # upload pdf
    pdf = st.sidebar.file_uploader("Upload PDF here", type='pdf')
    Apikey=st.sidebar.text_input("Add you api key here")
    # Add a number input for flashcards
    num_flashcards = st.sidebar.number_input("Number of flashcards to generate", 
                                           min_value=1, max_value=20, value=5)
    
    # Add a button to generate flashcards
    generate_button = st.sidebar.button("Generate Flashcards")
    ask_button=st.sidebar.button("Ask PDF Questions")
    if pdf is not None:
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
        
        if generate_button:
            st.header("Generated Flashcards")
            with st.spinner("Generating flashcards..."):
                flashcards = generate_flashcards(text,Apikey, num_flashcards)
                
                # Display flashcards using expanders
                for i, card in enumerate(flashcards, 1):
                    if '|' in card:
                        question, answer = card.split('|')
                        question = question.replace('Q:', '').strip()
                        answer = answer.replace('A:', '').strip()
                        
                        with st.expander(f"Flashcard {i}: {question}"):
                            st.write("Answer:", answer)
        # Keep the original Q&A functionality
        else:
            user_Q = st.chat_input("Or ask a specific question about the PDF")
            if user_Q:
                embeddings = GoogleGenerativeAIEmbeddings(
                    model="models/embedding-001",
                    google_api_key=Apikey
                )
                knowledge_base = FAISS.from_texts(chunks, embeddings)
                docs = knowledge_base.similarity_search(user_Q)
            
                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    google_api_key=Apikey,
                    temperature=0.7
                )

                chain = load_qa_chain(llm, chain_type="stuff")
                res = chain.run(input_documents=docs, question=user_Q)
                
                st.write("USER👨:", user_Q)
                st.write("CHAD🤖:", res)
    else:
            st.title("What are you learning today ?")
            st.subheader("Upload the pdf and generate the flashcards you want or just ask about the pdf content and solve your doubts")
if __name__ == "__main__":
    main()