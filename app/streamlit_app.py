import sys
import os
import pandas as pd
import streamlit as st

sys.path.append(os.path.abspath("."))

from src.inference.predict_obesity import predict_obesity
from src.inference.predict_bodyfat import predict_bodyfat
from src.inference.predict_calories import predict_calories
from src.llm.ai_coach import generate_plan
import plotly.graph_objects as go


########################################
# Utility Functions
########################################

def calculate_bmi(weight, height_cm):

    height_m = height_cm / 100

    return round(
        weight / (height_m ** 2),
        2
    )


def calculate_bmr(
    gender,
    weight,
    height_cm,
    age
):

    if gender == "Male":

        return round(
            10 * weight +
            6.25 * height_cm -
            5 * age +
            5,
            2
        )

    return round(
        10 * weight +
        6.25 * height_cm -
        5 * age -
        161,
        2
    )


def calculate_tdee(
    bmr,
    activity_level
):

    multipliers = {
        "Sedentary": 1.2,
        "Light": 1.375,
        "Moderate": 1.55,
        "Active": 1.725,
        "Very Active": 1.9
    }

    return round(
        bmr * multipliers[activity_level],
        2
    )
def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    else:
        return "Obese"

def calculate_health_score(
    bmi,
    bodyfat,
    risk
):

    score = 100

    if bmi < 18.5 or bmi > 30:
        score -= 20

    if bodyfat > 25:
        score -= 20

    if "Overweight" in risk:
        score -= 15

    if "Obesity" in risk:
        score -= 30

    return max(score, 0)

########################################
# Page Config
########################################

st.set_page_config(
    page_title="AI Fitness Coach",
    layout="wide"
)

st.title(
    "🏋️ AI Fitness & Nutrition Coach"
)
st.markdown("""
<style>

/* KPI Cards */
div[data-testid="stMetric"]{
    border:4px solid #49485C;
    border-radius:12px;
    padding:15px;
    height:120px;
}

/* Label */
div[data-testid="stMetric"] label{
    width:100%;
    display:flex;
    justify-content:center;
    text-align:center;
    font-size:30px !important;
    font-weight:600 !important;
}

/* Value */
div[data-testid="stMetricValue"]{
    text-align:center;
    justify-content:center;
    font-weight: bold;
    font-size:40px !important;
}

/* Delta (if used later) */
div[data-testid="stMetricDelta"]{
    justify-content:center;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stTabs button {
    flex-grow: 1 !important;
}

.stTabs button p {
    font-size: 30px !important;
    font-weight: 700 !important;
}

</style>
""", unsafe_allow_html=True)


age = st.sidebar.number_input(
    "Age",
    18,
    100,
    25
)

gender = st.sidebar.selectbox(
    "Gender",
    ["Male", "Female"]
)

height = st.sidebar.number_input(
    "Height (cm)",
    100,
    250,
    175
)

weight = st.sidebar.number_input(
    "Weight (kg)",
    30,
    250,
    80
)

activity_level = st.sidebar.selectbox(
    "Activity Level",
    [
        "Sedentary",
        "Light",
        "Moderate",
        "Active",
        "Very Active"
    ]
)

########################################
# Goal
########################################

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🎯 Fitness Goal"
)

goal = st.sidebar.selectbox(
    "Goal",
    [
        "Weight Loss",
        "Muscle Gain",
        "Maintenance"
    ]
)

########################################
# Body Measurements
########################################

st.sidebar.markdown("---")

st.sidebar.subheader(
    "📏 Body Measurements"
)

neck = st.sidebar.number_input(
    "Neck (cm)",
    20,
    60,
    40
)

chest = st.sidebar.number_input(
    "Chest (cm)",
    50,
    150,
    100
)

abdomen = st.sidebar.number_input(
    "Abdomen (cm)",
    50,
    180,
    90
)

hip = st.sidebar.number_input(
    "Hip (cm)",
    50,
    180,
    95
)

thigh = st.sidebar.number_input(
    "Thigh (cm)",
    30,
    100,
    60
)

########################################
# Workout Information
########################################

st.sidebar.markdown("---")

st.sidebar.subheader(
    "🏃 Workout Information"
)

duration = st.sidebar.slider(
    "Workout Duration (minutes)",
    min_value=10,
    max_value=180,
    value=60
)

heart_rate = st.sidebar.slider(
    "Heart Rate (bpm)",
    min_value=60,
    max_value=200,
    value=120
)

body_temp = st.sidebar.slider(
    "Body Temperature (°C)",
    min_value=36.0,
    max_value=40.0,
    value=37.0
)


########################################
# Health Metrics
########################################

bmi = calculate_bmi(
    weight,
    height
)

bmr = calculate_bmr(
    gender,
    weight,
    height,
    age
)

tdee = calculate_tdee(
    bmr,
    activity_level
)

def get_bmi_category(bmi):

    if bmi < 18.5:
        return "Underweight"

    elif bmi < 25:
        return "Normal"

    elif bmi < 30:
        return "Overweight"

    return "Obese"


def calculate_health_score(
    bmi,
    bodyfat,
    risk
):

    score = 100

    if bmi < 18.5 or bmi > 30:
        score -= 20

    if bodyfat > 25:
        score -= 20

    if "Overweight" in risk:
        score -= 15

    if "Obesity" in risk:
        score -= 30

    return max(score, 0)

########################################
# Obesity Prediction
########################################

obesity_input = {

    "Gender": gender,
    "Age": age,
    "Height": height / 100,
    "Weight": weight,

    "family_history_with_overweight": "yes",
    "FAVC": "yes",
    "FCVC": 2.5,
    "NCP": 3.0,
    "CAEC": "Sometimes",
    "SMOKE": "no",
    "CH2O": 2.0,
    "SCC": "no",
    "FAF": 2.0,
    "TUE": 1.0,
    "CALC": "Sometimes",
    "MTRANS": "Walking"
}

risk = predict_obesity(
    obesity_input
)


########################################
# Body Fat Prediction
########################################

bodyfat_input = {

    "Density": 1.05,
    "Age": age,
    "Weight": weight * 2.20462,
    "Height": height / 2.54,

    "Neck": neck,
    "Chest": chest,
    "Abdomen": abdomen,
    "Hip": hip,
    "Thigh": thigh,

    "Knee": 40,
    "Ankle": 25,
    "Biceps": 35,
    "Forearm": 30,
    "Wrist": 18
}

bodyfat = predict_bodyfat(
    bodyfat_input
)


########################################
# Calories Prediction
########################################

calorie_input = {

    "Gender": gender,
    "Age": age,
    "Height": height,
    "Weight": weight,
    "Duration": duration,
    "Heart_Rate": heart_rate,
    "Body_Temp": body_temp
}

calories = predict_calories(
    calorie_input
)
bmi_category = get_bmi_category(
    bmi
)

health_score = calculate_health_score(
    bmi,
    bodyfat,
    risk
)


########################################
# Dashboard Cards
########################################

st.markdown("---")

# Row 1
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "BMI",
    bmi
)

col2.metric(
    "BMR",
    f"{bmr:.0f}"
)

col3.metric(
    "TDEE",
    f"{tdee:.0f}"
)

col4.metric(
    "Body Fat %",
    f"{bodyfat:.2f}%"
)

col5.metric(
    "Calories Burn",
    f"{calories:.0f}"
)

st.markdown("<br>", unsafe_allow_html=True)

# Row 2
col6, col7 = st.columns(2)

if bmi_category == "Normal":
    bmi_color = "#0C4120"

elif bmi_category == "Overweight":
    bmi_color = "#B79716"

else:
    bmi_color = "#701010"


st.subheader("🏥 Health Score")

fig = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=health_score,

        title={
            "text": "Health Score"
        },

        gauge={
            "axis": {
                "range": [0, 100]
            },

            "bar": {
                "color": "white"
            },

            "steps": [
                {
                    "range": [0, 40],
                    "color": "#7D0E0E"
                },
                {
                    "range": [40, 70],
                    "color": "#FACC15"
                },
                {
                    "range": [70, 100],
                    "color": "#0F7133"
                }
            ],

            "threshold": {
                "line": {
                    "color": "white",
                    "width": 4
                },
                "thickness": 0.75,
                "value": health_score
            }
        }
    )
)

fig.update_layout(
    height=300,
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.markdown(
    f"""
    <div style="
        background-color:{bmi_color};
        border-radius:5px;
        border:4px solid {bmi_color};
        padding:12px;
        text-align:center;
        color:white;
        margin-bottom:20px;
    ">
        <h3>BMI Status: {bmi_category}</h3>
    </div>
    """,
    unsafe_allow_html=True
)


########################################
# Tabs
########################################

tab3, tab1, tab2 = st.tabs([
    "🏠 Home",
    "🎯 Recommendations",
    "🤖 AI Coach"
])


########################################
# TAB 0 - Home
########################################
with tab3:

    st.header(
        "🏠 Welcome to Your AI Fitness & Nutrition Coach"
    )

    st.markdown("""
    This application provides personalized fitness and nutrition recommendations based on your health metrics and goals.

    Use the sidebar to input your personal information, body measurements, and workout details.

    Navigate through the tabs to view your health metrics, recommended foods and exercises, and receive a personalized fitness plan from our AI coach.
    """)            
    st.subheader("📖 Understanding Your Results")

    st.markdown("""
    ### BMI (Body Mass Index)
    Measures whether your weight is appropriate for your height.

    | BMI Range | Category |
    |------------|-----------|
    | Below 18.5 | Underweight |
    | 18.5 - 24.9 | Healthy |
    | 25.0 - 29.9 | Overweight |
    | 30+ | Obese |

    ### BMR (Basal Metabolic Rate)
    The number of calories your body burns while resting.

    ### TDEE (Total Daily Energy Expenditure)
    The estimated calories you burn in a day.

    ### Body Fat Percentage
    Represents the proportion of fat in your body.

    ### Health Score
    A combined score based on your health indicators.

    ### Obesity Risk
    An AI prediction indicating your likelihood of being overweight or obese.
    """)
    st.subheader("🎯 Which Goal Should I Choose?")

    st.markdown("""
    ### Weight Loss
    Choose this if your objective is reducing body fat and losing weight.

    ### Muscle Gain
    Choose this if your goal is increasing muscle mass and strength.

    ### Maintenance
    Choose this if you are satisfied with your current body composition and want to maintain it.
    """)
    st.subheader("💡 Daily Health Tips")

    tips = [
        "Drink at least 2 liters of water daily.",
        "Aim for 7–9 hours of sleep each night.",
        "Exercise at least 150 minutes per week.",
        "Consume more fruits and vegetables.",
        "Reduce sugary drinks and processed foods.",
        "Take regular breaks from sitting.",
        "Track your progress consistently."
    ]

    for tip in tips:
        st.info(tip)

    st.subheader("⚠️ Health Disclaimer")

    st.warning("""
    This application provides estimates and recommendations based on machine learning models.

    The results should not be considered medical advice, diagnosis, or treatment.

    Always consult a qualified healthcare professional for medical concerns.
    """)

    st.subheader("📚 Common Terms")

    st.markdown("""
    | Term | Meaning |
    |--------|----------|
    | BMI | Body Mass Index |
    | BMR | Basal Metabolic Rate |
    | TDEE | Total Daily Energy Expenditure |
    | kcal | Kilocalories |
    | bpm | Beats Per Minute |
    | AI | Artificial Intelligence |
    | Body Fat % | Percentage of body fat in the body |
    """)


########################################
# TAB 1 - Recommendations
########################################

with tab1:

    st.header(
        "🎯 Personalized Recommendations"
    )

    food_df = pd.read_csv(
    "Data/food_nutrition_dataset.csv")
    

    exercise_df = pd.read_csv(
    "Data/exercise_dataset.csv"
    )

    foods = food_df[
        food_df["Diet_Type"] == goal
    ]

    st.subheader(
        "🥗 Recommended Foods"
    )

    st.dataframe(
        foods.head(10),
        use_container_width=True
    )

    workouts = exercise_df[
        exercise_df["Recommended_Goal"] == goal
    ]

    st.subheader(
        "🏋️ Recommended Exercises"
    )

    st.dataframe(
        workouts.head(10),
        use_container_width=True
    )


########################################
# TAB 2 - AI Coach
########################################

with tab2:

    st.header(
        "🤖 AI Fitness Coach"
    )

    st.write(
        f"""
Goal: **{goal}**

BMI: **{bmi}**

Body Fat: **{bodyfat:.2f}%**

Calories Burned: **{calories:.0f} kcal**

Risk Category: **{risk}**
"""
    )

    if st.button(
        "Generate Personalized Plan"
    ):

        with st.spinner(
            "Generating your personalized fitness plan..."
        ):

            plan = generate_plan(
                goal,
                bmi,
                bodyfat,
                risk,
                calories
            )

        st.markdown(plan)