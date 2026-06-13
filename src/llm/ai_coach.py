import streamlit as st
from google import genai


def generate_plan(
    goal,
    bmi,
    bodyfat,
    risk,
    calories
):

    client = genai.Client(
        api_key=st.secrets["GEMINI_API_KEY"]
    )

    prompt = f"""
    You are an expert fitness trainer and nutritionist.

    User Information:
    - Goal: {goal}
    - BMI: {bmi}
    - Body Fat: {bodyfat:.2f}%
    - Obesity Risk: {risk}
    - Calories Burned: {calories:.0f} kcal

    Create a detailed personalized report containing:

    # Health Assessment

    # Recommended Daily Calories

    # 7-Day Workout Plan

    # Nutrition Recommendations

    # Foods to Prioritize

    # Foods to Avoid

    # Lifestyle Tips

    Keep recommendations realistic and motivating.
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text