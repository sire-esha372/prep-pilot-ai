AI Driven Personalized study planner
AI Study Planner is a Streamlit-based intelligent application that helps users plan, track, and 
analyze their study progress using data analytics (Pandas), visualization (Plotly), and AI assistance (LangChain + Groq).
What it Does
allows users to plan and manage daily study tasks
tracks study progress and completion status
analyzes performance using pandas
generates insights and suggestions using AI
visualizes progress using interactive charts
provides a simple and user-friendly dashboard
Main Features
1. Study Planner
create daily/weekly study plans
manage subjects and tasks
mark tasks as completed
structured planning interface
2. AI Assistant
generates study suggestions using LangChain + Groq
helps in improving productivity
provides personalized recommendations
supports prompt-based interaction
3. Progress Tracking
tracks completed vs pending tasks
calculates performance metrics
maintains study history
uses pandas for data processing
4. Analytics Dashboard
visualizes progress using plotly
displays:
completion rate
subject-wise performance
consistency trends
interactive charts and graphs
Tech Stack
Python 3.9+
Streamlit
Pandas
Plotly
LangChain
LangChain Core
LangChain Groq
Project Structure

AI-Study-Planner/
│
├── app.py                  # main streamlit app
├── requirements.txt       # dependencies
├── .env                   # API key configuration
│
├── modules/
│   ├── planner.py
│   ├── analytics.py
│   ├── ai_helper.py
│
├── data/
│   └── study_data.csv
Execution Process
1. Clone the Repository

git clone https://github.com/your-username/ai-study-planner.git
cd ai-study-planner
2. Create Virtual Environment

python -m venv venv
Activate Environment
Windows
Bash
venv\Scripts\activate
Mac/Linux

source venv/bin/activate
3. Install Dependencies

pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file:

GROQ_API_KEY=your_api_key_here
5. Run the Application

streamlit run app.py
6. Open in Browser

http://localhost:8501
Important Runtime Flow
user enters study tasks
data is stored and managed using pandas
AI module generates suggestions via LangChain + Groq
progress is tracked and updated
plotly generates visual charts
streamlit displays dashboard and analytics
Data Handling
study data stored in CSV / memory
pandas used for:
data cleaning
analysis
aggregation
results updated dynamically
Security And Notes
API key stored in .env file
do not expose API key publicly
requires internet for AI features
lightweight and easy to run locally
Configuration
.env → API keys
requirements.txt → dependencies
app.py → main configuration
Future Enhancements
user authentication system
database integration (MySQL)
mobile-friendly UI
advanced AI recommendations
cloud deployment
Conclusion
This project provides a smart and interactive study management system
 that combines planning, tracking, analytics, and AI-based suggestions to improve productivity and learning efficiency.