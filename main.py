# to_do_list_app.py
import streamlit as st
import pandas as pd
import os
from datetime import date

st.set_page_config(page_title="To-Do List App", page_icon="✅")

st.title("📝 To-Do List App")

CSV_FILE = "tasks.csv"

# --- Load tasks from CSV if available ---
if os.path.exists(CSV_FILE):
    st.session_state.tasks = pd.read_csv(CSV_FILE).to_dict("records")
else:
    st.session_state.tasks = []

# --- Add a new task ---
with st.form("task_form", clear_on_submit=True):
    task_text = st.text_input("Enter a task")
    category = st.selectbox("Select Category", ["Work", "Personal", "Urgent", "Other"])
    priority = st.selectbox("Select Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Select Due Date", min_value=date.today())
    submitted = st.form_submit_button("Add Task")

    if submitted and task_text:
        # Append task
        st.session_state.tasks.append(
            {"task": task_text, "category": category, "priority": priority, "due_date": str(due_date)}
        )

        # Save to CSV
        pd.DataFrame(st.session_state.tasks).to_csv(CSV_FILE, index=False)

# --- Display tasks ---
st.subheader("Your Tasks")

if st.session_state.tasks:
    df = pd.DataFrame(st.session_state.tasks)

    # Sort by priority (High > Medium > Low), then due date
    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    df["priority_order"] = df["priority"].map(priority_order)
    df = df.sort_values(by=["priority_order", "due_date"])

    for i, row in df.iterrows():
        cols = st.columns([5, 2, 2, 1])
        cols[0].write(f"**{row['task']}**")
        cols[1].write(f"📌 {row['category']}")
        cols[2].write(f"🔥 {row['priority']} | 📅 {row['due_date']}")
        if cols[3].button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            pd.DataFrame(st.session_state.tasks).to_csv(CSV_FILE, index=False)
            st.experimental_rerun()
else:
    st.write("✅ No tasks yet!")
