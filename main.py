# to_do_list_app.py
import streamlit as st
from datetime import date

st.set_page_config(page_title="To-Do List App", page_icon="✅")

st.title("📝 To-Do List App")

# --- Initialize session state ---
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# --- Add a new task ---
with st.form("task_form", clear_on_submit=True):
    task_text = st.text_input("Enter a task")
    category = st.selectbox("Select Category", ["Work", "Personal", "Urgent", "Other"])
    priority = st.selectbox("Select Priority", ["High", "Medium", "Low"])
    due_date = st.date_input("Select Due Date", min_value=date.today())
    submitted = st.form_submit_button("Add Task")

    if submitted and task_text:
        st.session_state.tasks.append(
            {
                "task": task_text,
                "category": category,
                "priority": priority,
                "due_date": str(due_date),
                "completed": False,
            }
        )

# --- Filters ---
st.sidebar.header("🔍 Filters")
filter_category = st.sidebar.selectbox("Filter by Category", ["All", "Work", "Personal", "Urgent", "Other"])
filter_priority = st.sidebar.selectbox("Filter by Priority", ["All", "High", "Medium", "Low"])

# --- Clear all tasks ---
if st.sidebar.button("🗑️ Clear All Tasks"):
    st.session_state.tasks = []
    st.experimental_rerun()

# --- Display tasks ---
st.subheader("Your Tasks")

if st.session_state.tasks:
    # Filter
    tasks = st.session_state.tasks
    if filter_category != "All":
        tasks = [t for t in tasks if t["category"] == filter_category]
    if filter_priority != "All":
        tasks = [t for t in tasks if t["priority"] == filter_priority]

    # Progress bar
    completed_count = sum(1 for t in tasks if t["completed"])
    if len(tasks) > 0:
        st.progress(completed_count / len(tasks))

    # Show tasks
    for i, task in enumerate(tasks):
        cols = st.columns([3, 2, 2, 1, 1])
        if cols[0].checkbox(task["task"], value=task["completed"], key=f"chk_{i}"):
            st.session_state.tasks[i]["completed"] = True
        else:
            st.session_state.tasks[i]["completed"] = False

        cols[1].write(f"📌 {task['category']}")
        cols[2].write(f"🔥 {task['priority']} | 📅 {task['due_date']}")

        # Edit button
        if cols[3].button("✏️", key=f"edit_{i}"):
            new_text = st.text_input("Edit task", value=task["task"], key=f"edit_text_{i}")
            if st.button("Save", key=f"save_{i}"):
                st.session_state.tasks[i]["task"] = new_text
                st.experimental_rerun()

        # Delete button
        if cols[4].button("❌", key=f"del_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
else:
    st.write("✅ No tasks yet!")
