🏋️ AI Fitness & Nutrition Coach

An AI-powered Fitness & Nutrition Coach built using Machine Learning, Streamlit, and Ollama. This application helps users assess their health status, estimate body fat percentage, predict calories burned, receive personalized fitness recommendations, and generate AI-powered fitness plans.

⸻

🚀 Features

📊 Health Analytics

* BMI (Body Mass Index) Calculation
* BMR (Basal Metabolic Rate) Calculation
* TDEE (Total Daily Energy Expenditure) Estimation
* Health Score Dashboard
* BMI Status Classification

🏥 Obesity Risk Prediction

* Machine Learning model for obesity risk classification
* Personalized risk assessment

🔥 Body Fat Prediction

* Predicts body fat percentage using body measurements
* Uses trained regression model

🏃 Calories Burn Prediction

* Estimates calories burned during workouts
* Based on:
    * Age
    * Gender
    * Height
    * Weight
    * Workout Duration
    * Heart Rate
    * Body Temperature

🎯 Personalized Recommendations

* Goal-based food recommendations
* Goal-based exercise recommendations
* Supports:
    * Weight Loss
    * Muscle Gain
    * Maintenance

🤖 AI Fitness Coach

* Powered by Ollama Local LLM
* Generates personalized fitness plans
* Considers:
    * BMI
    * Body Fat Percentage
    * Obesity Risk
    * Calories Burned
    * Fitness Goal

⸻

🛠️ Tech Stack

Frontend

* Streamlit

Backend

* Python

Machine Learning

* Scikit-Learn
* Pandas
* NumPy

AI

* Ollama
* Qwen 3 8B

Visualization

* Plotly

⸻

📂 Project Structure

RAG-fitness-nutrition-coach/
│
├── app/
│   └── streamlit_app.py
│
├── src/
│   ├── inference/
│   ├── llm/
│   └── utils/
│
├── models/
│   ├── obesity_model.pkl
│   ├── body_fat_model.pkl
│   └── calorie_model.pkl
│
├── Data/
│
├── screenshots/
│
├── requirements.txt
├── README.md
└── .gitignore

⚙️ Installation

Clone Repository

git clone https://github.com/Disura-chan/RAG-fitness-nutrition-coach.git
cd RAG-fitness-nutrition-coach

Create Virtual Environment

python -m venv .venv
source .venv/bin/activate

Install Dependencies

pip install -r requirements.txt

Run Ollama

ollama serve

Pull Model

ollama pull qwen3:8b

Start Application

streamlit run app/streamlit_app.py

⸻

📈 Machine Learning Models

Model	Type
Obesity Prediction	Classification
Body Fat Prediction	Regression
Calories Burn Prediction	Regression



🔮 Future Improvements

* User Authentication
* Progress Tracking
* Weight Forecasting
* Food Image Recognition
* Nutrition Chatbot using RAG
* Cloud Deployment
* Mobile Application

⸻

👨‍💻 Author

Disura Chandrasekara

MSc Data Science Student | Machine Learning Enthusiast | Data Analyst

GitHub: https://github.com/Disura-chan
