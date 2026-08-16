import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def get_database():
    client = MongoClient(
        st.secrets["MONGODB_URI"]
    )

    # Verify MongoDB connection
    client.admin.command("ping")

    return client["aura_learn"]


def get_users_collection():
    db = get_database()
    return db["users"]


def get_study_plans_collection():
    db = get_database()
    return db["study_plans"]


def get_progress_collection():
    db = get_database()
    return db["progress"]


def get_feedback_collection():
    db = get_database()
    return db["feedback"]