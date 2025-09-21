import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()  # reads GOOGLE_API_KEY from .env

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

st.title("Daily Mood & Productivity Coach")

mood = st.selectbox("How do you feel today?",
                    ["Happy", "Neutral", "Sad", "Stressed", "Tired"])
tasks = st.text_area("Today's tasks",
                     placeholder="e.g. finish homework, exercise")
sleep = st.number_input("Hours of sleep last night", 0, 24, 7)
energy = st.slider("Energy level (0–10)", 0, 10, 5)

prompt = f"""
You are a friendly coach.
Mood: {mood}
Sleep: {sleep} hours
Energy: {energy}/10
Tasks: {tasks}

Give:
1. A short motivational note.
2. A prioritized task list.
3. One productivity tip.
"""

if st.button("Get Plan"):
    with st.spinner("Thinking..."):
        res = model.invoke(prompt)
        st.subheader("Your Plan")
        st.write(res.content)
