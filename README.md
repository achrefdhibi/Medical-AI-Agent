
# 🧠 Medical AI Agent – Powered by LangGraph & LangChain

This project introduces an artificial intelligence agent specialized in the medical field, built using LangGraph and LangChain. It can intelligently converse with users, understand their healthcare needs, and provide accurate, reliable, and contextualized responses.

## 🚀 Key Features
- **Natural Language Processing (NLP)** to analyze medical requests
- **🤖 Intelligent Architecture** based on the ReAct Agent model
- **Integration of Medical Tools** and trustworthy knowledge bases
- **💬 Dynamic and Contextual Interaction** with users
- **🧠 Conversational Memory System** for personalized follow-up

## 🎯 Project Objectives
This project aims to demonstrate how AI agents can be used in the medical sector to assist users, improve the accuracy of information provided, and offer a smarter, more accessible, and responsive service.

## 🧰 Technologies Used
- [LangGraph](https://www.langchain.com/langgraph)
- [LangChain](https://www.langchain.com/)
- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [groq api](https://groq.com/)

## 🛠️ Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/medical-ai-agent.git
   cd medical-ai-agent
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows
   ```

3. **Install Dependencies**
   ```bash
   echo "langchain==0.2.0\nlanggraph==0.1.0\nstreamlit==1.36.0\npython-dotenv==1.0.1" > requirements.txt
   pip install -r requirements.txt
   ```

4. **API Key Configuration**
   Create a `.env` file in the project root with your Grok API key (obtained from [xAI API](https://x.ai/api)):
   ```bash
   echo "GROQ_API_KEY=your-grok-api-key-here" > .env
   ```

5. **Run the Application**
   Launch the Streamlit app to interact with the Medical AI Agent:
   ```bash
   streamlit run app.py
   ```
   The application will be available at `http://localhost:8501`.
```
