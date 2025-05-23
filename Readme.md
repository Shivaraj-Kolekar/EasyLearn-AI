# EasyLearn AI Study Companion 📚

AI Study Companion is an interactive learning tool that helps students and professionals study more effectively by leveraging AI to generate study materials, practice quizzes, and conduct mock interviews.

![Screenshot 2025-05-23 200612](https://github.com/user-attachments/assets/024788fb-a037-4550-a2e1-d57b2149184b)


## Features 🌟

- **📖 Study Material Generation**

  - Convert PDF documents into comprehensive study notes
  - Generate concise summaries of complex materials
  - Extract key concepts and definitions

- **🗂️ Interactive Flashcards**

  - Create AI-generated flashcards from your study material
  - Customize number of cards (1-20)
  - Interactive flip functionality

- **📝 Personal Notes**

  - Take and save personal notes
  - Auto-save study sessions
  - Track your learning progress

- **❓ Practice Quizzes**

  - Generate multiple-choice questions
  - Test your understanding
  - Get immediate feedback

- **💭 AI Chat Assistant**

  - Ask questions about the study material
  - Get detailed explanations
  - Context-aware responses

- **🎯 Mock Interview Preparation**
  - Generate role-specific interview questions
  - Multiple interview types (Technical, Behavioral, System Design, etc.)
  - Get AI feedback on your answers
  - Customizable difficulty levels

## Installation 🔧

1. **Clone the repository**

```bash
git clone https://github.com/Shivaraj-Kolekar/EasyLearn-AI.git
cd ai-study-companion
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- Windows:

```bash
.\venv\Scripts\activate
```

- Unix/MacOS:

```bash
source venv/bin/activate
```

4. **Install required packages**

```bash
pip install -r requirements.txt
```

5. **Create a `.env` file and add your Google API key**

```plaintext
GOOGLE_API_KEY=your_api_key_here
```

## Requirements 📋

Create a `requirements.txt` file with these dependencies:

```plaintext
streamlit
pypdf2
langchain
langchain-google-genai
faiss-cpu
google-generativeai
python-dotenv
```

## Usage 🚀

1. **Start the application**

```bash
streamlit run app.py
```

2. **Access the web interface**

- Open your browser and go to `http://localhost:8501`
- The application will also be available at `http://YOUR_IP:8501` on your local network

3. **Using the application**
   - Upload a PDF document
   - Enter your Google API key in the sidebar
   - Choose from available features in the tabs
   - Generate study materials, flashcards, or start a mock interview

## Study Session Management 📊

- Study sessions are automatically saved in the `study_sessions` directory
- Each session includes:
  - Timestamp
  - Generated notes
  - Flashcards
  - Summary
  - Personal notes

## Mock Interview Feature 🎯

1. **Configure your interview:**

   - Select job role
   - Specify years of experience
   - Choose interview type
   - Set difficulty level
   - List required skills

2. **During the interview:**
   - Answer generated questions
   - Get AI feedback on your responses
   - View sample answers
   - Track your progress

## Environment Variables 🔐

Create a `.env` file with the following:

```plaintext
GOOGLE_API_KEY=your_google_api_key_here
```

## Getting an API Key 🔑

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Generative AI API
4. Create credentials (API key)
5. Copy the API key to your `.env` file

## Contributing 🤝

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💡

For support, please open an issue in the GitHub repository or contact the maintainers.

## Acknowledgments 🙏

- Google Generative AI
- Langchain
- Streamlit
- FAISS
- PyPDF2

## Note ⚠️

Remember to keep your API keys secure and never commit them to version control.
