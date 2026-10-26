# AI-Time-Managment
An AI-powered time management system that predicts task completion time using machine learning and provides deadline risk assessment, intelligent task prioritization, personalized scheduling, task recommendations, and interactive analytics using Streamlit.

AI-Powered-Time-Management-System
Repository navigation
Code
Issues
Pull requests
Actions
AathifaFathima
AI-Powered-Time-Management-System
Public
About
An AI-powered time management system that predicts task completion time using machine learning and provides deadline risk assessment, intelligent task prioritization, personalized scheduling, task recommendations, and interactive analytics using Streamlit.

Resources
Readme
Activity
Stars
0 stars
Watchers
0 watching
Forks
0 forks
Report repository
Chandran
Chandran
2 days ago
Name	
.gitignore
2 days ago
README.md
2 days ago
app.py
2 days ago
daily_productivity.csv
2 days ago
label_encoder.pkl
2 days ago
requirements.txt
2 days ago
scaler.pkl
2 days ago
task_completion_engineered.csv
2 days ago
task_features.pkl
2 days ago
task_preprocessor.pkl
2 days ago
Repository files navigation
README
⏱️ AI-Powered Time Management System
An intelligent time management application developed using Machine Learning, Python, and Streamlit.

📌 Project Overview
The AI-Powered Time Management System helps users organize tasks, estimate completion times, assess deadline risks, and generate personalized work schedules.

The application uses an XGBoost regression model to predict task completion time based on task characteristics and user preferences.

🚀 Features
AI-Based Task Completion Time Prediction
Deadline Risk Assessment
Intelligent Task Prioritization
Personalized Schedule Generation
Personalized Task Recommendations
Task Management System
Interactive Analytics Dashboard
Task Completion Tracking
🛠️ Technologies Used
Python
Streamlit
Pandas
NumPy
Scikit-learn
XGBoost
Plotly
Joblib
Google Colab
Visual Studio Code
🤖 Machine Learning
The project includes:

Data Cleaning and Preprocessing
Exploratory Data Analysis
Feature Engineering
Multiple Regression Model Training
Hyperparameter Tuning
Model Evaluation
Task Completion Time Prediction
The prototype model was trained using synthetic task-completion data.

📂 Project Structure
AI-Powered-Time-Management-System/
│
├── app.py
├── task_xgboost.json
├── task_preprocessor.pkl
├── task_features.pkl
├── requirements.txt
├── README.md
└── .gitignore
▶️ How to Run
1. Clone the Repository
git clone https://github.com/YOUR_USERNAME/AI-Powered-Time-Management-System.git
2. Install Dependencies
Use Python 3.13 in a virtual environment.

pip install -r requirements.txt
3. Run the Application
streamlit run app.py
📊 Application Modules
Task Completion Prediction
Predicts the estimated time required to complete a task using an XGBoost regression model.

Deadline Risk Assessment
Estimates deadline risk based on predicted completion time and available working time.

Task Prioritization
Recommends task priority using predefined scoring rules.

Personalized Scheduling
Creates work sessions and breaks based on predicted task duration and user preferences.

Personalized Recommendations
Provides rule-based time management suggestions.

Task Manager
Allows users to add, complete, and delete tasks.

Analytics Dashboard
Visualizes task completion progress, category distribution, and priority distribution.

⚠️ Limitations
The machine learning model uses synthetic training data.
Deadline risk, scheduling, and recommendations are rule-based.
Task Manager data is stored in Streamlit session state and is not permanently saved.
🔮 Future Enhancements
Database Integration
Calendar Integration
Real-Time Notifications
User Authentication
Improved Personalized Scheduling
Model Training with Real-World Data
👩‍💻 Project Type
Machine Learning and Artificial Intelligence Internship Project
