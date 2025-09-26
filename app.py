import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.7)

st.title("Daily Mood & Productivity Coach")

# keep history for this session
if "history" not in st.session_state:
    st.session_state.history = []

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

# main button to get a new plan
if st.button("Get Plan"):
    with st.spinner("Thinking..."):
        res = model.invoke(prompt)
        st.session_state.history.append(res.content)
        st.subheader("Your Plan")
        st.write(res.content)

# NEW: button to show chat history in a pop-up area
if st.button("Show Chat History"):
    if st.session_state.history:
        st.subheader("Chat History")
        for i, msg in enumerate(st.session_state.history, 1):
            st.markdown(f"**Plan {i}:**\n{msg}\n---")
    else:
        st.info("No history yet.")
