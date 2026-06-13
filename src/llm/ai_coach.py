import ollama


def generate_plan(
    goal,
    bmi,
    bodyfat,
    obesity_risk,
    calories
):

    prompt = f"""
You are a certified fitness coach.

Goal: {goal}

BMI: {bmi}

Body Fat: {bodyfat}

Obesity Risk: {obesity_risk}

Calories Burned: {calories}

Create:

1. Weekly workout plan
2. Daily meal plan
3. Health advice

Keep it practical.
"""

    response = ollama.chat(
        model="qwen3:8b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]