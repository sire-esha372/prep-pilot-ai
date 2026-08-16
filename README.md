# 🚀 PrepPilot AI

### AI-Powered Personalized Exam Preparation Planner

PrepPilot AI is an intelligent Streamlit-based application that helps students create personalized exam preparation plans, track their study progress, and analyze their performance.

It combines **Generative AI, LangChain, Groq, MongoDB, and data visualization** to provide an interactive and personalized study planning experience.

## 🚀 Live Demo

🔗 **[Launch PrepPilot AI](https://prep-pilot-ai.streamlit.app/)**

Try the deployed application directly on Streamlit Community Cloud.


---

## ✨ Features

### 🔐 User Authentication
- User registration and login
- Secure password hashing using bcrypt
- User-specific study data
- MongoDB-based authentication
- Logout functionality

### 🤖 AI-Powered Study Plan Generation
- Generates personalized exam preparation plans
- Uses LangChain and Groq LLM
- Considers:
  - Exam subject
  - Exam date
  - Available daily study hours
  - Learning style
  - Weak topics
  - Exam type
- Provides structured AI-generated study recommendations

### 📚 Study Planner
- Create personalized study plans
- Calculate remaining days until the exam
- Calculate available study hours
- Display generated preparation plans
- Collect student feedback and ratings

### 📈 Progress Tracking
- Record daily study hours
- Track study completion status
- Maintain study history
- Store progress data securely in MongoDB

### 📊 Analytics Dashboard
- Track study performance
- Analyze completed study sessions
- Display performance metrics
- Visualize progress using interactive charts
- Analyze user feedback and ratings

### 🎨 Interactive UI
- Streamlit-based interface
- Personalized welcome screen
- Responsive dashboard layout
- Dark-themed sidebar
- AI-focused visual design
- Simple navigation

---

## 🧠 How It Works

```text
User Registration / Login
          ↓
     Home Dashboard
          ↓
    Enter Exam Details
          ↓
   AI Study Plan Generator
          ↓
    LangChain + Groq LLM
          ↓
 Personalized Study Plan
          ↓
   Track Daily Progress
          ↓
       MongoDB
          ↓
   Analytics Dashboard
          ↓
 Performance Insights