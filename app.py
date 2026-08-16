

import streamlit as st
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, datetime, timedelta, time
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import csv

from auth.authentication import create_user, authenticate_user
from database.mongodb import (
    get_study_plans_collection,
    get_progress_collection,
    get_feedback_collection
)

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Aura Learn",
    layout="wide"
)


# =========================================================
# SESSION
# =========================================================

def init_session():

    defaults = {
        "page": "Home",
        "plan_generated": False,
        "plan_output": "",
        "days_remaining": 0,
        "daily_hours": 0,
        "exam_subject": "",
        "logged_in": False,
        "user": None,
    }

    for key, value in defaults.items():

        if key not in st.session_state:
            st.session_state[key] = value


# =========================================================
# UI / BACKGROUND
# =========================================================

# =========================================================
# UI / BACKGROUND
# =========================================================

def set_home_background(image_path):

    import base64

    # -----------------------------------------------------
    # LOAD BACKGROUND IMAGE
    # -----------------------------------------------------

    if image_path.startswith("http"):

        bg_url = image_path

    else:

        with open(image_path, "rb") as f:

            encoded = base64.b64encode(
                f.read()
            ).decode()

        bg_url = f"data:image/jpg;base64,{encoded}"

    # -----------------------------------------------------
    # GLOBAL UI CSS
    # -----------------------------------------------------

    st.markdown(
        """
        <style>

        /* =================================================
           MAIN BACKGROUND
           ================================================= */

        [data-testid="stAppViewContainer"] {
            background-image: url("BACKGROUND_URL");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }


        /* =================================================
           REMOVE STREAMLIT TOP WHITE HEADER
           ================================================= */

        header[data-testid="stHeader"] {
            display: none !important;
            height: 0 !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }


        /* =================================================
           REMOVE TOP SPACING
           ================================================= */

        section.main {
            padding-top: 0 !important;
        }

        [data-testid="stAppViewContainer"] > .main {
            padding-top: 0 !important;
        }

        [data-testid="stAppViewContainer"] .block-container {
            padding-top: 15px !important;
            margin-top: 0 !important;
        }


        /* =================================================
           MAIN CONTENT CONTAINER
           ================================================= */

        .block-container {
            background-color: rgba(0, 0, 0, 0.60);
            padding: 15px 20px 25px 20px;
            border-radius: 10px;
        }


        /* =================================================
           SIDEBAR
           ================================================= */

        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
            border-right: 1px solid #334155 !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background-color: #0F172A !important;
        }

        [data-testid="stSidebarContent"] {
            background-color: #0F172A !important;
        }


        /* Sidebar headings */

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {
            color: #F8FAFC !important;
        }


        /* Sidebar general text */

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #F8FAFC !important;
        }


        /* Sidebar email */

        [data-testid="stSidebar"] .stCaption {
            color: #94A3B8 !important;
        }


        /* Sidebar dividers */

        [data-testid="stSidebar"] hr {
            border-color: #334155 !important;
        }


        /* Sidebar logout button */

        [data-testid="stSidebar"] button {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }


        [data-testid="stSidebar"] button:hover {
            background-color: #334155 !important;
            color: #38BDF8 !important;
            border-color: #38BDF8 !important;
        }


        /* =================================================
           INPUTS
           ================================================= */

        input,
        textarea {
            background-color: white !important;
            color: black !important;
        }

        div[data-baseweb="select"] > div {
            background-color: white !important;
            color: black !important;
        }

        div[data-testid="stDateInput"] input,
        div[data-testid="stTimeInput"] input {
            background-color: white !important;
            color: black !important;
        }


        /* =================================================
           MAIN PAGE TEXT
           ================================================= */

        label,
        h1,
        h2,
        h3,
        h4,
        h5,
        h6,
        p,
        span {
            color: white !important;
        }


        /* =================================================
           METRICS
           ================================================= */

        [data-testid="stMetricLabel"] {
            color: white !important;
        }

        [data-testid="stMetricValue"] {
            color: white !important;
            font-weight: 700 !important;
        }

        [data-testid="stMetricDelta"] {
            color: white !important;
        }

        [data-testid="stMetric"] {
            background-color: rgba(0, 0, 0, 0.45) !important;
            padding: 18px !important;
            border-radius: 12px !important;
        }


        /* =================================================
           SUBHEADERS
           ================================================= */

        .stSubheader {
            color: white !important;
        }


        /* =================================================
           GENERAL STREAMLIT TEXT
           ================================================= */

        .stMarkdown,
        .stText {
            color: white !important;
        }


        /* =================================================
           BUTTONS
           ================================================= */

        .stButton > button,
        .stFormSubmitButton > button {
            background-color: #FFFFFF !important;
            color: #111827 !important;
            border: 1px solid #D1D5DB !important;
            font-weight: 600 !important;
            border-radius: 8px !important;
        }


        .stButton > button p,
        .stButton > button span,
        .stFormSubmitButton > button p,
        .stFormSubmitButton > button span {
            color: #111827 !important;
        }


        .stButton > button:hover,
        .stFormSubmitButton > button:hover {
            background-color: #F3F4F6 !important;
            color: #111827 !important;
        }


        .stButton > button:hover p,
        .stButton > button:hover span,
        .stFormSubmitButton > button:hover p,
        .stFormSubmitButton > button:hover span {
            color: #111827 !important;
        }


        /* =================================================
           DATAFRAME
           ================================================= */

        [data-testid="stDataFrame"] {
            color: white !important;
        }

        </style>
        """.replace(
            "BACKGROUND_URL",
            bg_url
        ),
        unsafe_allow_html=True
    )
# =========================================================
# AUTHENTICATION PAGE
# =========================================================

def authentication_page():

    set_home_background("bg2.jpeg")

    st.markdown(
        """
        <h1 style='text-align:center;'>
            🎯 Aura Learn
        </h1>

        <p style='text-align:center;'>
            AI-Powered Personalized Exam Preparation
        </p>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        login_tab, signup_tab = st.tabs(
            ["🔐 Login", "📝 Sign Up"]
        )

        # =================================================
        # LOGIN
        # =================================================

        with login_tab:

            st.subheader("Welcome Back 👋")

            login_email = st.text_input(
                "Email",
                key="login_email"
            )

            login_password = st.text_input(
                "Password",
                type="password",
                key="login_password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                if not login_email or not login_password:

                    st.warning(
                        "Please enter your email and password."
                    )

                else:

                    user = authenticate_user(
                        login_email,
                        login_password
                    )

                    if user:

                        st.session_state.logged_in = True
                        st.session_state.user = user
                        st.session_state.page = "Home"

                        st.success(
                            f"Welcome back, {user['name']}!"
                        )

                        st.rerun()

                    else:

                        st.error(
                            "Invalid email or password."
                        )

        # =================================================
        # SIGN UP
        # =================================================

        with signup_tab:

            st.subheader("Create Your Account 🚀")

            signup_name = st.text_input(
                "Name",
                key="signup_name"
            )

            signup_email = st.text_input(
                "Email",
                key="signup_email"
            )

            signup_password = st.text_input(
                "Password",
                type="password",
                key="signup_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password"
            )

            if st.button(
                "Create Account",
                use_container_width=True
            ):

                if not signup_name or not signup_email or not signup_password:

                    st.warning(
                        "Please fill in all fields."
                    )

                elif signup_password != confirm_password:

                    st.error(
                        "Passwords do not match."
                    )

                elif len(signup_password) < 6:

                    st.warning(
                        "Password must contain at least 6 characters."
                    )

                else:

                    success, message = create_user(
                        signup_name,
                        signup_email,
                        signup_password
                    )

                    if success:

                        st.success(message)

                        st.info(
                            "Your account has been created. "
                            "Please log in."
                        )

                    else:

                        st.error(message)


# =========================================================
# LLM
# =========================================================

def generate_study_plan(inputs):

    try:

        api_key = st.secrets["GROQ_API_KEY"]

        llm = ChatGroq(
            temperature=0.7,
            model_name="openai/gpt-oss-120b",
            api_key=api_key
        )

        template = """
        Generate a structured study plan:

        Exam: {exam_subject}
        Duration: {duration_weeks} weeks
        Daily Hours: {daily_hours}
        Weaknesses: {weaknesses}
        Learning Style: {learning_style}
        Exam Type: {exam_type}
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a study planner."
                ),
                (
                    "user",
                    template
                )
            ]
        )

        chain = (
            prompt
            | llm
            | StrOutputParser()
        )

        return chain.invoke(inputs)

    except Exception as e:

        st.error(
            "Unable to generate the study plan."
        )

        return f"ERROR: {e}"


# =========================================================
# HOME
# =========================================================

# =========================================================
# HOME DASHBOARD
# =========================================================

def home_page():

    set_home_background("bg2.jpeg")

    # =====================================================
    # USER
    # =====================================================

    user_name = st.session_state.user["name"]

    user_id = st.session_state.user["id"]

    # =====================================================
    # LOAD MONGODB DATA
    # =====================================================

    try:

        study_plans_collection = (
            get_study_plans_collection()
        )

        progress_collection = (
            get_progress_collection()
        )

        # -------------------------------------------------
        # LATEST STUDY PLAN
        # -------------------------------------------------

        latest_plan = (
            study_plans_collection
            .find_one(
                {
                    "user_id": user_id
                },
                sort=[
                    ("created_at", -1)
                ]
            )
        )

        # -------------------------------------------------
        # USER PROGRESS
        # -------------------------------------------------

        progress_records = list(
            progress_collection.find(
                {
                    "user_id": user_id
                }
            )
        )

    except Exception as e:

        st.error(
            "❌ Could not load dashboard data."
        )

        st.write(str(e))

        return

    # =====================================================
    # CALCULATE DASHBOARD DATA
    # =====================================================

    total_sessions = len(
        progress_records
    )

    total_planned = sum(
        float(
            record.get(
                "planned_hours",
                0
            )
        )
        for record in progress_records
    )

    total_completed = sum(
        float(
            record.get(
                "completed_hours",
                0
            )
        )
        for record in progress_records
    )

    if total_planned > 0:

        completion_rate = (
            total_completed /
            total_planned
        ) * 100

    else:

        completion_rate = 0

    # =====================================================
    # HEADER
    # =====================================================

    st.title(
       "🎯 AI Driven Personalized Exam Preparation Planner"
    )

    st.markdown(
       f"### Welcome back, {user_name}! 👋"
    )

    st.markdown(
       "Plan smarter • Study better • Achieve more 🚀"
    )

    # =====================================================
    # CURRENT STUDY PLAN
    # =====================================================

    if latest_plan:

        exam_subject = latest_plan.get(
            "exam_subject",
            "Not available"
        )

        exam_type = latest_plan.get(
            "exam_type",
            "Not specified"
        )

        daily_hours = float(
            latest_plan.get(
                "daily_hours",
                0
            )
        )

        exam_date = latest_plan.get(
            "exam_date"
        )

        # -----------------------------------------------
        # DAYS REMAINING
        # -----------------------------------------------

        if exam_date:

            if isinstance(
                exam_date,
                datetime
            ):

                exam_date_only = (
                    exam_date.date()
                )

            else:

                exam_date_only = exam_date

            days_remaining = (
                exam_date_only -
                date.today()
            ).days

            if days_remaining < 0:

                days_remaining = 0

        else:

            days_remaining = 0

        # =================================================
        # CURRENT EXAM CARD
        # =================================================

        st.markdown(
            """
            <h2>📚 Current Study Plan</h2>
            """,
            unsafe_allow_html=True
        )

        plan_col1, plan_col2, plan_col3 = st.columns(3)

        with plan_col1:

            st.metric(
                "Exam / Subject",
                exam_subject
            )

        with plan_col2:

            st.metric(
                "Days Remaining",
                days_remaining
            )

        with plan_col3:

            st.metric(
                "Daily Study",
                f"{daily_hours:.1f} hrs"
            )

        st.caption(
            f"Exam Type: {exam_type}"
        )

    else:

        st.info(
            "📚 You haven't created a study plan yet. "
            "Start planning your preparation!"
        )

    # =====================================================
    # STUDY OVERVIEW
    # =====================================================

    st.markdown(
        "<h2>📊 Study Overview</h2>",
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Study Sessions",
            total_sessions
        )

    with col2:

        st.metric(
            "Planned Hours",
            f"{total_planned:.1f}"
        )

    with col3:

        st.metric(
            "Completed Hours",
            f"{total_completed:.1f}"
        )

    with col4:

        st.metric(
            "Completion Rate",
            f"{completion_rate:.1f}%"
        )

    # =====================================================
    # PROGRESS BAR
    # =====================================================

    if total_planned > 0:

        st.markdown(
            "<h3>🎯 Overall Study Progress</h3>",
            unsafe_allow_html=True
        )

        st.progress(
            min(
                completion_rate / 100,
                1.0
            )
        )

        st.caption(
            f"You have completed "
            f"{total_completed:.1f} of "
            f"{total_planned:.1f} planned hours."
        )

    # =====================================================
    # QUICK ACTIONS
    # =====================================================

    st.markdown(
        "<h2>🚀 Quick Actions</h2>",
        unsafe_allow_html=True
    )

    action1, action2, action3 = st.columns(3)

    with action1:

        if st.button(
            "📚 Study Planner",
            use_container_width=True
        ):

            st.session_state.page = "Planner"

            st.rerun()

    with action2:

        if st.button(
            "📈 Progress Tracker",
            use_container_width=True
        ):

            st.session_state.page = (
                "Progress Tracker"
            )

            st.rerun()

    with action3:

        if st.button(
            "📊 Analytics",
            use_container_width=True
        ):

            st.session_state.page = "Analytics"

            st.rerun()

    # =====================================================
    # LATEST PLAN PREVIEW
    # =====================================================

    if latest_plan:

        st.markdown(
            "<h2>📝 Latest AI Study Plan</h2>",
            unsafe_allow_html=True
        )

        generated_plan = latest_plan.get(
            "generated_plan",
            ""
        )

        if generated_plan:

            # Display a limited preview
            plan_preview = generated_plan[:1200]

            st.markdown(
                f"""
                <div style="
                    background:rgba(0,0,0,0.55);
                    color:white;
                    padding:20px;
                    border-radius:12px;
                    line-height:1.6;
                ">
                    {plan_preview}
                </div>
                """,
                unsafe_allow_html=True
            )

            if len(generated_plan) > 1200:

                st.caption(
                    "Showing a preview of your latest "
                    "AI-generated study plan. "
                    "Open Study Planner to view the full plan."
                )


# =========================================================
# PLANNER
# =========================================================

def planner_page():

    set_home_background("bg2.jpeg")

    st.markdown(
        "<h1>📚 Study Plan Generator</h1>",
        unsafe_allow_html=True
    )

    with st.form("form"):

        subject = st.text_input("Subject")

        exam_date = st.date_input(
            "Exam Date"
        )

        start = st.time_input(
            "Start Time",
            value=time(18, 0)
        )

        end = st.time_input(
            "End Time",
            value=time(21, 0)
        )

        style = st.multiselect(
            "Learning Style",
            [
                "Visual",
                "Auditory",
                "Kinesthetic",
                "Reading"
            ]
        )

        weak = st.text_area(
            "Weaknesses"
        )

        exam_type = st.text_input(
            "Exam Type"
        )

        submit = st.form_submit_button(
            "Generate"
        )

    if submit:

        # -----------------------------------------
        # VALIDATION
        # -----------------------------------------

        if not subject.strip():

            st.warning(
                "Please enter the exam subject."
            )

            return

        days = (
            exam_date - date.today()
        ).days

        if days < 0:

            st.warning(
                "Please select a future exam date."
            )

            return

        weeks = round(
            days / 7,
            1
        )

        start_dt = datetime.combine(
            datetime.today(),
            start
        )

        end_dt = datetime.combine(
            datetime.today(),
            end
        )

        if end_dt <= start_dt:

            end_dt += timedelta(
                days=1
            )

        hours = round(
            (
                end_dt - start_dt
            ).total_seconds() / 3600,
            2
        )

        # -----------------------------------------
        # AI INPUTS
        # -----------------------------------------

        inputs = {

            "exam_subject": subject,

            "duration_weeks": weeks,

            "daily_hours": hours,

            "weaknesses": weak,

            "learning_style": style,

            "exam_type": exam_type,
        }

        # -----------------------------------------
        # GENERATE AI PLAN
        # -----------------------------------------

        with st.spinner(
            "🤖 Creating your personalized study plan..."
        ):

            output = generate_study_plan(
                inputs
            )

        # -----------------------------------------
        # SAVE PLAN TO SESSION
        # -----------------------------------------

        if not output.startswith("ERROR"):

            st.session_state.plan_generated = True

            st.session_state.plan_output = output

            st.session_state.days_remaining = days

            st.session_state.daily_hours = hours

            st.session_state.exam_subject = subject

            # -------------------------------------
            # SAVE PLAN TO MONGODB
            # -------------------------------------

            try:

                study_plans = (
                    get_study_plans_collection()
                )

                study_plans.insert_one(
                    {
                        "user_id":
                            st.session_state.user["id"],

                        "exam_subject":
                            subject,

                        "exam_date":
    datetime.combine(exam_date, time.min),

                        "daily_hours":
                            hours,

                        "duration_weeks":
                            weeks,

                        "learning_style":
                            style,

                        "weaknesses":
                            weak,

                        "exam_type":
                            exam_type,

                        "generated_plan":
                            output,

                        "created_at":
                            datetime.utcnow()
                    }
                )

                st.success(
                    "✅ Study plan generated and saved!"
                )

            except Exception as e:

                st.error(
                    "Study plan generated, "
                    "but could not be saved."
                )

                st.write(str(e))

    # =================================================
    # DISPLAY GENERATED PLAN
    # =================================================

        if st.session_state.plan_generated:

            st.success(
        f"{st.session_state.days_remaining} days left"
    )

    st.info(
        f"{st.session_state.daily_hours} hrs/day"
    )

    st.markdown(
        f"""
        <div style="
            background:#1e1e1e;
            color:white;
            padding:20px;
            border-radius:10px;
        ">
        {st.session_state.plan_output}
        </div>
        """,
        unsafe_allow_html=True
    )

        # =================================================
        # FEEDBACK
        # =================================================

    with st.form("feedback"):

            fb = st.text_area("Feedback")

            rate = st.slider(
                "Rating",
                1,
                5
            )

            submit_feedback = st.form_submit_button(
                "Submit"
            )

            if submit_feedback:

                try:

                    feedback_collection = (
                        get_feedback_collection()
                    )

                    feedback_collection.insert_one(
                        {
                            "user_id":
                                st.session_state.user["id"],

                            "exam":
                                st.session_state.exam_subject,

                            "rating":
                                rate,

                            "feedback":
                                fb.strip(),

                            "created_at":
                                datetime.utcnow()
                        }
                    )

                    st.success(
                        "✅ Feedback saved successfully!"
                    )

                except Exception as e:

                    st.error(
                        "❌ Could not save feedback."
                    )

                    st.write(str(e))
                
# =========================================================
# PROGRESS TRACKER
# =========================================================

def progress_tracker_page():

    set_home_background("bg2.jpeg")

    st.markdown(
        "<h1>📈 Study Progress Tracker</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "Track your planned and completed study hours.",
        unsafe_allow_html=True
    )

    # =====================================================
    # PROGRESS FORM
    # =====================================================

    with st.form("progress_form"):

        exam = st.text_input(
            "Exam / Subject",
            value=st.session_state.exam_subject
        )

        col1, col2 = st.columns(2)

        with col1:

            study_date = st.date_input(
                "Study Date",
                value=date.today()
            )

            planned_hours = st.number_input(
                "Planned Hours",
                min_value=0.0,
                max_value=24.0,
                value=2.0,
                step=0.5
            )

        with col2:

            completed_hours = st.number_input(
                "Completed Hours",
                min_value=0.0,
                max_value=24.0,
                value=0.0,
                step=0.5
            )

            status = st.selectbox(
                "Status",
                [
                    "Completed",
                    "Partially Completed",
                    "Missed"
                ]
            )

        notes = st.text_area(
            "Notes",
            placeholder=(
                "What did you study? "
                "Any difficulties?"
            )
        )

        save_progress = st.form_submit_button(
            "💾 Save Progress",
            use_container_width=True
        )

    # =====================================================
    # SAVE TO MONGODB
    # =====================================================

    if save_progress:

        if not exam.strip():

            st.warning(
                "Please enter the exam or subject."
            )

            return

        if completed_hours > planned_hours:

            st.warning(
                "Completed hours cannot be greater "
                "than planned hours."
            )

            return

        try:

            progress_collection = (
                get_progress_collection()
            )

            progress_collection.insert_one(
                {
                    "user_id":
                        st.session_state.user["id"],

                    "exam":
                        exam.strip(),

                    "date":
                        datetime.combine(
                            study_date,
                            time.min
                        ),

                    "planned_hours":
                        planned_hours,

                    "completed_hours":
                        completed_hours,

                    "status":
                        status,

                    "notes":
                        notes.strip(),

                    "created_at":
                        datetime.utcnow()
                }
            )

            st.success(
                "✅ Progress saved successfully!"
            )

        except Exception as e:

            st.error(
                "❌ Could not save progress."
            )

            st.write(str(e))

    # =====================================================
    # RECENT PROGRESS
    # =====================================================

    st.divider()

    st.subheader(
        "📋 Recent Progress"
    )

    try:

        progress_collection = (
            get_progress_collection()
        )

        records = list(
            progress_collection.find(
                {
                    "user_id":
                        st.session_state.user["id"]
                }
            ).sort(
                "date",
                -1
            ).limit(20)
        )

        if records:

            progress_data = []

            for record in records:

                progress_data.append(
                    {
                        "Exam":
                            record.get(
                                "exam",
                                ""
                            ),

                        "Date":
                            record.get(
                                "date"
                            ),

                        "Planned Hours":
                            record.get(
                                "planned_hours",
                                0
                            ),

                        "Completed Hours":
                            record.get(
                                "completed_hours",
                                0
                            ),

                        "Status":
                            record.get(
                                "status",
                                ""
                            ),

                        "Notes":
                            record.get(
                                "notes",
                                ""
                            )
                    }
                )

            progress_df = pd.DataFrame(
                progress_data
            )

            st.dataframe(
                progress_df,
                use_container_width=True,
                hide_index=True
            )

        else:

            st.info(
                "No progress records yet. "
                "Start tracking your study sessions!"
            )

    except Exception as e:

        st.error(
            "Could not load progress records."
        )

        st.write(str(e))        

# =========================================================
# ANALYTICS
# =========================================================

def analytics_page():

    set_home_background("bg2.jpeg")

    st.markdown(
        "<h1>📊 Analytics Dashboard</h1>",
        unsafe_allow_html=True
    )

    st.markdown(
        "Understand your study performance and progress.",
        unsafe_allow_html=True
    )

    # =====================================================
    # LOAD USER DATA
    # =====================================================

    try:

        progress_collection = (
            get_progress_collection()
        )

        feedback_collection = (
            get_feedback_collection()
        )

        user_id = (
            st.session_state.user["id"]
        )

        progress_records = list(
            progress_collection.find(
                {
                    "user_id": user_id
                }
            )
        )

        feedback_records = list(
            feedback_collection.find(
                {
                    "user_id": user_id
                }
            )
        )

    except Exception as e:

        st.error(
            "❌ Could not load analytics data."
        )

        st.write(str(e))

        return

    # =====================================================
    # PREPARE PROGRESS DATA
    # =====================================================

    if progress_records:

        progress_data = []

        for record in progress_records:

            progress_data.append(
                {
                    "Exam":
                        record.get(
                            "exam",
                            ""
                        ),

                    "Date":
                        record.get(
                            "date"
                        ),

                    "Planned Hours":
                        float(
                            record.get(
                                "planned_hours",
                                0
                            )
                        ),

                    "Completed Hours":
                        float(
                            record.get(
                                "completed_hours",
                                0
                            )
                        ),

                    "Status":
                        record.get(
                            "status",
                            ""
                        )
                }
            )

        progress_df = pd.DataFrame(
            progress_data
        )

        progress_df["Date"] = pd.to_datetime(
            progress_df["Date"]
        )

    else:

        progress_df = pd.DataFrame(
            columns=[
                "Exam",
                "Date",
                "Planned Hours",
                "Completed Hours",
                "Status"
            ]
        )

    # =====================================================
    # PREPARE FEEDBACK DATA
    # =====================================================

    if feedback_records:

        feedback_data = []

        for record in feedback_records:

            feedback_data.append(
                {
                    "Exam":
                        record.get(
                            "exam",
                            ""
                        ),

                    "Rating":
                        float(
                            record.get(
                                "rating",
                                0
                            )
                        ),

                    "Feedback":
                        record.get(
                            "feedback",
                            ""
                        )
                }
            )

        feedback_df = pd.DataFrame(
            feedback_data
        )

    else:

        feedback_df = pd.DataFrame(
            columns=[
                "Exam",
                "Rating",
                "Feedback"
            ]
        )

    # =====================================================
    # KEY METRICS
    # =====================================================

    total_sessions = len(
        progress_df
    )

    total_planned = (
        progress_df["Planned Hours"].sum()
        if not progress_df.empty
        else 0
    )

    total_completed = (
        progress_df["Completed Hours"].sum()
        if not progress_df.empty
        else 0
    )

    if total_planned > 0:

        completion_rate = (
            total_completed /
            total_planned
        ) * 100

    else:

        completion_rate = 0

    completed_sessions = (
        len(
            progress_df[
                progress_df["Status"]
                == "Completed"
            ]
        )
        if not progress_df.empty
        else 0
    )

    # =====================================================
    # TOP METRIC CARDS
    # =====================================================

    st.subheader(
        "📌 Study Overview"
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Total Sessions",
            total_sessions
        )

    with col2:

        st.metric(
            "Planned Hours",
            f"{total_planned:.1f}"
        )

    with col3:

        st.metric(
            "Completed Hours",
            f"{total_completed:.1f}"
        )

    with col4:

        st.metric(
            "Completion Rate",
            f"{completion_rate:.1f}%"
        )

    # =====================================================
    # STATUS CHART
    # =====================================================

    if not progress_df.empty:

        st.divider()

        st.subheader(
            "📊 Study Session Status"
        )

        status_df = (
            progress_df["Status"]
            .value_counts()
            .reset_index()
        )

        status_df.columns = [
            "Status",
            "Sessions"
        ]

        fig_status = px.bar(
            status_df,
            x="Status",
            y="Sessions",
            title="Study Sessions by Status",
            text="Sessions"
        )

        fig_status.update_layout(
            template="plotly_dark",
            xaxis_title="Status",
            yaxis_title="Number of Sessions",
            height=400
        )

        st.plotly_chart(
            fig_status,
            use_container_width=True
        )

    # =====================================================
    # PLANNED VS COMPLETED
    # =====================================================

    if not progress_df.empty:

        st.subheader(
            "⏱️ Planned vs Completed Hours"
        )

        subject_hours = (
            progress_df
            .groupby("Exam")[
                [
                    "Planned Hours",
                    "Completed Hours"
                ]
            ]
            .sum()
            .reset_index()
        )

        fig_hours = go.Figure()

        fig_hours.add_trace(
            go.Bar(
                x=subject_hours["Exam"],
                y=subject_hours["Planned Hours"],
                name="Planned Hours"
            )
        )

        fig_hours.add_trace(
            go.Bar(
                x=subject_hours["Exam"],
                y=subject_hours["Completed Hours"],
                name="Completed Hours"
            )
        )

        fig_hours.update_layout(
            template="plotly_dark",
            barmode="group",
            xaxis_title="Exam / Subject",
            yaxis_title="Hours",
            height=450
        )

        st.plotly_chart(
            fig_hours,
            use_container_width=True
        )

    # =====================================================
    # STUDY PROGRESS TREND
    # =====================================================

    if not progress_df.empty:

        st.subheader(
            "📈 Study Progress Over Time"
        )

        trend_df = (
            progress_df
            .groupby("Date")[
                "Completed Hours"
            ]
            .sum()
            .reset_index()
            .sort_values("Date")
        )

        fig_trend = px.line(
            trend_df,
            x="Date",
            y="Completed Hours",
            markers=True,
            title="Completed Study Hours Over Time"
        )

        fig_trend.update_layout(
            template="plotly_dark",
            xaxis_title="Date",
            yaxis_title="Completed Hours",
            height=400
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

    # =====================================================
    # SUBJECT PERFORMANCE
    # =====================================================

    if not progress_df.empty:

        st.subheader(
            "📚 Subject-wise Performance"
        )

        subject_df = (
            progress_df
            .groupby("Exam")
            .agg(
                Planned_Hours=(
                    "Planned Hours",
                    "sum"
                ),
                Completed_Hours=(
                    "Completed Hours",
                    "sum"
                )
            )
            .reset_index()
        )

        subject_df["Completion %"] = (
            subject_df["Completed_Hours"]
            /
            subject_df["Planned_Hours"]
            * 100
        ).fillna(0)

        fig_subject = px.bar(
            subject_df,
            x="Exam",
            y="Completion %",
            text="Completion %",
            title="Completion Rate by Subject"
        )

        fig_subject.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside"
        )

        fig_subject.update_layout(
            template="plotly_dark",
            xaxis_title="Exam / Subject",
            yaxis_title="Completion %",
            yaxis_range=[
                0,
                max(
                    100,
                    subject_df["Completion %"].max()
                    + 10
                )
            ],
            height=450
        )

        st.plotly_chart(
            fig_subject,
            use_container_width=True
        )

        display_subject_df = (
            subject_df.copy()
        )

        display_subject_df.columns = [
            "Exam",
            "Planned Hours",
            "Completed Hours",
            "Completion %"
        ]

        display_subject_df[
            "Completion %"
        ] = display_subject_df[
            "Completion %"
        ].round(1)

        st.dataframe(
            display_subject_df,
            use_container_width=True,
            hide_index=True
        )

    # =====================================================
    # FEEDBACK ANALYTICS
    # =====================================================

    st.divider()

    st.subheader(
        "⭐ Feedback Analytics"
    )

    if not feedback_df.empty:

        average_rating = (
            feedback_df["Rating"].mean()
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Average Rating",
                f"{average_rating:.1f} / 5"
            )

        with col2:

            st.metric(
                "Total Feedback",
                len(feedback_df)
            )

        rating_df = (
            feedback_df["Rating"]
            .value_counts()
            .sort_index()
            .reset_index()
        )

        rating_df.columns = [
            "Rating",
            "Count"
        ]

        fig_rating = px.bar(
            rating_df,
            x="Rating",
            y="Count",
            text="Count",
            title="Feedback Rating Distribution"
        )

        fig_rating.update_layout(
            template="plotly_dark",
            xaxis_title="Rating",
            yaxis_title="Number of Responses",
            height=400
        )

        st.plotly_chart(
            fig_rating,
            use_container_width=True
        )

        st.subheader(
            "💬 Your Feedback"
        )

        st.dataframe(
            feedback_df,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info(
            "No feedback submitted yet."
        )

# =========================================================
# INITIALIZE SESSION
# =========================================================

init_session()


# =========================================================
# AUTHENTICATION GATE
# =========================================================

if not st.session_state.logged_in:

    authentication_page()

    st.stop()

# =========================================================
# SIDEBAR THEME
# =========================================================

def apply_sidebar_theme():

    st.markdown(
        """
        <style>

        /* SIDEBAR BACKGROUND */

        [data-testid="stSidebar"] {
            background-color: #0F172A !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background-color: #0F172A !important;
        }

        [data-testid="stSidebarContent"] {
            background-color: #0F172A !important;
        }

        /* SIDEBAR TEXT */

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3,
        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] label {
            color: #F8FAFC !important;
        }

        /* EMAIL / SECONDARY TEXT */

        [data-testid="stSidebar"] .stCaption {
            color: #94A3B8 !important;
        }

        /* DIVIDERS */

        [data-testid="stSidebar"] hr {
            border-color: #334155 !important;
        }

        /* LOGOUT BUTTON */

        [data-testid="stSidebar"] button {
            background-color: #1E293B !important;
            color: #F8FAFC !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
        }

        [data-testid="stSidebar"] button:hover {
            background-color: #334155 !important;
            color: #38BDF8 !important;
            border-color: #38BDF8 !important;
        }

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# APPLY SIDEBAR THEME
# =========================================================

apply_sidebar_theme()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
# =========================================================
# SIDEBAR
# =========================================================

    with st.sidebar:
     st.title("📌 Navigation")

    st.write(
        f"👤 {st.session_state.user['name']}"
    )

    st.caption(
        st.session_state.user["email"]
    )

    st.divider()

    pages = [
        "Home",
        "Planner",
        "Progress Tracker",
        "Analytics"
    ]

    selected = st.radio(
        "Go to",
        pages,
        index=pages.index(
            st.session_state.page
        )
    )

    if selected != st.session_state.page:

        st.session_state.page = selected

        st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False

        st.session_state.user = None

        st.session_state.page = "Home"

        st.session_state.plan_generated = False

        st.session_state.plan_output = ""

        st.rerun()


# =========================================================
# ROUTING
# =========================================================

if st.session_state.page == "Home":

    home_page()

elif st.session_state.page == "Planner":

    planner_page()

elif st.session_state.page == "Progress Tracker":

    progress_tracker_page()

elif st.session_state.page == "Analytics":

    analytics_page()