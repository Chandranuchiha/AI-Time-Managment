import streamlit as st
import pandas as pd
import joblib
from xgboost import XGBRegressor
import plotly.express as px

st.set_page_config(
    page_title="Time Management using AI",
    page_icon="⏱️",
    layout="wide"
)

# Load trained model
preprocessor = joblib.load("task_preprocessor.pkl")

model = XGBRegressor()
model.load_model("task_xgboost.json")

features = joblib.load("task_features.pkl")

st.title("⏱️ Time Management using AI")
st.subheader("🤖 AI Task Completion Time Prediction")

st.write(
    "Enter task details to predict how much time "
    "you may need to complete the task."
)

with st.form("prediction_form"):

    col1, col2 = st.columns(2)

    with col1:
        task_category = st.selectbox(
            "Task Category",
            ["Coding", "Studying", "Assignment",
             "Project", "Meeting", "Research",
             "Documentation", "Presentation"]
        )

        task_difficulty = st.selectbox(
            "Task Difficulty",
            ["Easy", "Medium", "Hard"]
        )

        task_priority = st.selectbox(
            "Task Priority",
            ["Low", "Medium", "High"]
        )

        task_complexity_score = st.slider(
            "Task Complexity", 1, 10, 5
        )

        user_experience_level = st.selectbox(
            "Experience Level",
            ["Beginner", "Intermediate", "Advanced"]
        )

        estimated_workload_minutes = st.number_input(
            "Estimated Workload (minutes)",
            min_value=1,
            value=120
        )

        daily_available_hours = st.number_input(
            "Daily Available Hours",
            min_value=0.5,
            max_value=24.0,
            value=6.0
        )

        historical_avg_completion_minutes = st.number_input(
            "Historical Average Completion Time",
            min_value=1.0,
            value=120.0
        )

        preferred_work_session_minutes = st.number_input(
            "Preferred Work Session (minutes)",
            min_value=10,
            value=45
        )

    with col2:
        break_frequency = st.number_input(
            "Expected Break Frequency",
            min_value=0,
            value=3
        )

        avg_break_duration_minutes = st.number_input(
            "Average Break Duration",
            min_value=0,
            value=10
        )

        distraction_level = st.selectbox(
            "Distraction Level",
            ["Low", "Medium", "High"]
        )

        focus_score = st.slider(
            "Focus Score", 1, 10, 7
        )

        ai_assistance_used = st.selectbox(
            "AI Assistance Used?",
            [0, 1]
        )

        deadline_hours = st.number_input(
            "Hours Until Deadline",
            min_value=0.1,
            value=24.0
        )

    submitted = st.form_submit_button(
        "🔮 Predict Completion Time"
    )

if submitted:

    workload_hours = estimated_workload_minutes / 60

    break_time_minutes = (
        break_frequency * avg_break_duration_minutes
    )

    workload_per_available_hour = (
        workload_hours / max(daily_available_hours, 0.1)
    )

    input_data = pd.DataFrame([{
        "task_category": task_category,
        "task_difficulty": task_difficulty,
        "task_priority": task_priority,
        "task_complexity_score": task_complexity_score,
        "user_experience_level": user_experience_level,
        "historical_avg_completion_minutes": historical_avg_completion_minutes,
        "daily_available_hours": daily_available_hours,
        "preferred_work_session_minutes": preferred_work_session_minutes,
        "estimated_workload_minutes": estimated_workload_minutes,
        "break_frequency": break_frequency,
        "avg_break_duration_minutes": avg_break_duration_minutes,
        "distraction_level": distraction_level,
        "focus_score": focus_score,
        "ai_assistance_used": ai_assistance_used,
        "deadline_hours": deadline_hours,
        "workload_hours": workload_hours,
        "break_time_minutes": break_time_minutes,
        "workload_per_available_hour": workload_per_available_hour
    }])

    input_data = input_data[features]

    processed_data = preprocessor.transform(input_data)

    prediction = model.predict(processed_data)[0]

    prediction = max(0, float(prediction))

    hours = int(prediction // 60)
    minutes = int(round(prediction % 60))

    st.success(
        f"⏱️ Estimated Task Completion Time: "
        f"{prediction:.1f} minutes"
    )

    st.info(
        f"Approximately {hours} hours and {minutes} minutes"
    )

    st.caption(
        "Prediction is based on a model trained using synthetic task data."
    )

    # Deadline Risk Assessment

    st.header("🚨 Deadline Risk Assessment")

    available_minutes = (
        deadline_hours / 24
    ) * daily_available_hours * 60

    if prediction > available_minutes:
        risk_level = "High Risk"
        risk_message = "Task may not be completed before the deadline."

    elif prediction > available_minutes * 0.8:
        risk_level = "Medium Risk"
        risk_message = "Task may be completed close to the deadline."

    else:
        risk_level = "Low Risk"
        risk_message = "Task is likely to be completed before the deadline."

    if risk_level == "High Risk":
        st.error(f"🔴 {risk_level}")
    elif risk_level == "Medium Risk":
        st.warning(f"🟡 {risk_level}")
    else:
        st.success(f"🟢 {risk_level}")

    st.write(risk_message)

    st.write(
        f"Available Working Time: {available_minutes:.1f} minutes"
    )

    st.write(
        f"Predicted Required Time: {prediction:.1f} minutes"
    )

    # Task Prioritization

    st.header("📌 AI-Assisted Task Prioritization")

    priority_score = 0

    if task_priority == "High":
        priority_score += 3
    elif task_priority == "Medium":
        priority_score += 2
    else:
        priority_score += 1

    if risk_level == "High Risk":
        priority_score += 3
    elif risk_level == "Medium Risk":
        priority_score += 2
    else:
        priority_score += 1

    if deadline_hours <= 12:
        priority_score += 3
    elif deadline_hours <= 24:
        priority_score += 2
    else:
        priority_score += 1

    if priority_score >= 8:
        recommended_priority = "High Priority"
    elif priority_score >= 5:
        recommended_priority = "Medium Priority"
    else:
        recommended_priority = "Low Priority"

    st.info(
        f"📌 Recommended Task Priority: {recommended_priority}"
    )

    st.write(f"Priority Score: {priority_score}/9")

    # Personalized Schedule Generation

    st.header("📅 Personalized Schedule Generation")

    remaining_time = prediction
    session_number = 1
    schedule = []

    while remaining_time > 0:

        # Calculate work session duration
        work_duration = min(
            preferred_work_session_minutes,
            remaining_time
        )

        schedule.append({
            "Session": session_number,
            "Activity": f"Work Session {session_number}",
            "Duration (minutes)": round(work_duration, 1)
        })

        remaining_time -= work_duration

        # Add break only if more work remains
        if remaining_time > 0 and avg_break_duration_minutes > 0:
            schedule.append({
                "Session": session_number,
                "Activity": "Break",
                "Duration (minutes)": avg_break_duration_minutes
            })

        session_number += 1

    schedule_df = pd.DataFrame(schedule)

    st.dataframe(
        schedule_df,
        use_container_width=True
    )

    total_work_time = prediction

    total_break_time = sum(
        item["Duration (minutes)"]
        for item in schedule
        if item["Activity"] == "Break"
    )

    total_schedule_time = (
        total_work_time + total_break_time
    )

    st.subheader("⏱️ Schedule Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Work Time",
        f"{total_work_time:.1f} min"
    )

    col2.metric(
        "Break Time",
        f"{total_break_time:.1f} min"
    )

    col3.metric(
        "Total Schedule Time",
        f"{total_schedule_time:.1f} min"
    )

    # Check deadline feasibility
    if total_schedule_time <= available_minutes:
        st.success(
            "✅ Your personalized schedule fits within "
            "the estimated available working time."
        )
    else:
        st.warning(
            "⚠️ Your personalized schedule may not fit "
            "within the estimated available working time."
        )

    # Personalized Recommendations

    st.header("💡 Personalized Recommendations")

    recommendations = []

    # Recommendation based on focus score
    if focus_score <= 4:
        recommendations.append(
            "🎯 Your focus score is low. Try working in "
            "short sessions of 25–30 minutes."
        )

    # Recommendation based on distraction level
    if distraction_level == "High":
        recommendations.append(
            "📵 High distraction detected. Keep your "
            "phone notifications off during work sessions."
        )

    # Recommendation based on task difficulty
    if task_difficulty == "Hard":
        recommendations.append(
            "🧩 This is a difficult task. Divide it into "
            "smaller, manageable subtasks."
        )

    # Recommendation based on deadline risk
    if risk_level == "High Risk":
        recommendations.append(
            "🚨 High deadline risk! Start this task as early "
            "as possible and focus on important sections first."
        )

    elif risk_level == "Medium Risk":
        recommendations.append(
            "⏳ Your deadline is approaching. Monitor your "
            "progress regularly to avoid delays."
        )

    # Recommendation based on schedule feasibility
    if total_schedule_time > available_minutes:
        recommendations.append(
            "📅 Your schedule exceeds the estimated available "
            "working time. Consider reducing interruptions "
            "or adjusting the deadline."
        )

    # Recommendation based on break frequency
    if break_frequency == 0 and prediction > 60:
        recommendations.append(
            "☕ Consider including short breaks between "
            "long work sessions to maintain concentration."
        )

    # Recommendation based on AI assistance
    if ai_assistance_used == 0:
        recommendations.append(
            "🤖 You can explore AI tools for planning, "
            "organizing tasks, and tracking progress."
        )

    # Recommendation based on priority
    if recommended_priority == "High Priority":
        recommendations.append(
            "📌 This task has high priority. Schedule it "
            "during your most productive working hours."
        )

    # Default recommendation
    if not recommendations:
        recommendations.append(
            "✅ Your current task plan looks manageable. "
            "Continue following your schedule and track progress."
        )

    # Display recommendations
    for number, recommendation in enumerate(
        recommendations, start=1
    ):
        st.info(f"{number}. {recommendation}")

    st.caption(
        "Recommendations are generated using rule-based "
        "logic based on the user's task details and "
        "predicted completion time."
    )

# ======================================
# TASK MANAGER
# ======================================

st.divider()

st.header("📝 Task Manager")

st.write(
    "Add tasks, track progress, and manage your daily activities."
)

# Initialize session state
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Add new task
with st.form("task_manager_form"):

    task_name = st.text_input("Enter Task Name")

    task_category_manager = st.selectbox(
        "Select Task Category",
        [
            "Coding",
            "Studying",
            "Assignment",
            "Project",
            "Meeting",
            "Research",
            "Documentation",
            "Presentation"
        ]
    )

    task_priority_manager = st.selectbox(
        "Select Task Priority",
        ["Low", "Medium", "High"]
    )

    task_deadline = st.date_input(
        "Select Task Deadline"
    )

    add_task = st.form_submit_button(
        "➕ Add Task"
    )

if add_task:

    if task_name.strip():

        new_task = {
            "id": st.session_state.get("next_task_id", 1),
            "Task Name": task_name.strip(),
            "Category": task_category_manager,
            "Priority": task_priority_manager,
            "Deadline": str(task_deadline),
            "Status": "Pending"
        }

        st.session_state.tasks.append(new_task)

        st.session_state.next_task_id = (
            new_task["id"] + 1
        )

        st.success("Task Added Successfully!")

    else:
        st.warning("Please enter a task name.")

# Task Statistics
st.subheader("📊 Task Statistics")

total_tasks = len(st.session_state.tasks)

completed_tasks = sum(
    task["Status"] == "Completed"
    for task in st.session_state.tasks
)

pending_tasks = total_tasks - completed_tasks

col1, col2, col3 = st.columns(3)

col1.metric("Total Tasks", total_tasks)
col2.metric("Completed Tasks", completed_tasks)
col3.metric("Pending Tasks", pending_tasks)

# Display Tasks
st.subheader("📋 Your Task List")

if st.session_state.tasks:

    for task in st.session_state.tasks:

        with st.container(border=True):

            st.write(
                f"**Task:** {task['Task Name']}"
            )

            st.write(
                f"**Category:** {task['Category']}"
            )

            st.write(
                f"**Priority:** {task['Priority']}"
            )

            st.write(
                f"**Deadline:** {task['Deadline']}"
            )

            st.write(
                f"**Status:** {task['Status']}"
            )

            col1, col2 = st.columns(2)

            with col1:

                if task["Status"] == "Pending":

                    if st.button(
                        "✅ Mark Completed",
                        key=f"complete_{task['id']}"
                    ):

                        task["Status"] = "Completed"
                        st.rerun()

            with col2:

                if st.button(
                    "🗑️ Delete Task",
                    key=f"delete_{task['id']}"
                ):

                    st.session_state.tasks = [
                        item
                        for item in st.session_state.tasks
                        if item["id"] != task["id"]
                    ]

                    st.rerun()

else:

    st.info(
        "No tasks added yet. Add your first task!"
    )

# ======================================
# ANALYTICS DASHBOARD
# ======================================

st.divider()

st.header("📊 Task Analytics Dashboard")

st.write(
    "Analyze task completion, priority, and category distribution."
)

# Check whether tasks are available
if st.session_state.tasks:

    # Convert task list into DataFrame
    task_df = pd.DataFrame(st.session_state.tasks)

    # Calculate task statistics
    total = len(task_df)

    completed = len(
        task_df[task_df["Status"] == "Completed"]
    )

    pending = len(
        task_df[task_df["Status"] == "Pending"]
    )

    completion_percentage = (
        completed / total
    ) * 100

    # Display metrics
    st.subheader("📈 Productivity Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Tasks", total)

    col2.metric("Completed Tasks", completed)

    col3.metric("Pending Tasks", pending)

    col4.metric(
        "Completion Rate",
        f"{completion_percentage:.1f}%"
    )

    # Task completion progress
    st.subheader("🎯 Task Completion Progress")

    st.progress(
        completion_percentage / 100
    )

    # Task Status Distribution
    st.subheader("🥧 Task Status Distribution")

    status_counts = (
        task_df["Status"]
        .value_counts()
        .reset_index()
    )

    status_counts.columns = [
        "Status",
        "Count"
    ]

    status_fig = px.pie(
        status_counts,
        names="Status",
        values="Count",
        title="Completed vs Pending Tasks",
        hole=0.4
    )

    st.plotly_chart(
        status_fig,
        use_container_width=True
    )

    # Task Category Distribution
    st.subheader("📚 Task Category Distribution")

    category_counts = (
        task_df["Category"]
        .value_counts()
        .reset_index()
    )

    category_counts.columns = [
        "Category",
        "Count"
    ]

    category_fig = px.bar(
        category_counts,
        x="Category",
        y="Count",
        title="Tasks by Category"
    )

    st.plotly_chart(
        category_fig,
        use_container_width=True
    )

    # Task Priority Distribution
    st.subheader("📌 Task Priority Distribution")

    priority_counts = (
        task_df["Priority"]
        .value_counts()
        .reset_index()
    )

    priority_counts.columns = [
        "Priority",
        "Count"
    ]

    priority_fig = px.bar(
        priority_counts,
        x="Priority",
        y="Count",
        title="Tasks by Priority"
    )

    st.plotly_chart(
        priority_fig,
        use_container_width=True
    )

    # Display task data
    st.subheader("📋 Task Analytics Data")

    st.dataframe(
        task_df,
        use_container_width=True
    )

else:

    st.info(
        "No task data available. Add tasks in the Task Manager "
        "to view analytics."
    )



