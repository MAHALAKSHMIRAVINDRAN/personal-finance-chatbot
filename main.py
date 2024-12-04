import os
from dotenv import load_dotenv
from google.cloud import dialogflow_v2 as dialogflow
from google.protobuf.json_format import MessageToDict

# Your other code for interacting with Dialogflow and FastAPI

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from dialogflow_integration import detect_intent_texts  # Import the Dialogflow function

# Load environment variables from the .env file
load_dotenv()

# Get database credentials from environment variables
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

# Initialize FastAPI app
app = FastAPI()

# Define Pydantic models for request and response validation
class Expense(BaseModel):
    category: str
    amount: float
    date: str  # format: YYYY-MM-DD

class SavingsGoal(BaseModel):
    goal_name: str
    target_amount: float
    saved_amount: float = 0.0
    deadline: str  # format: YYYY-MM-DD

# Helper function to connect to the database
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return connection
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Database connection error: {err}")

# 1. Log Expense Endpoint
@app.post("/log-expense")
async def log_expense(expense: Expense):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO expenses (user_id, category, amount, expense_date, description)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (1, expense.category, expense.amount, expense.date, "Expense logged via API")
        )
        connection.commit()
        return {"message": "Expense logged successfully"}
    except mysql.connector.Error as err:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error logging expense: {err}")
    finally:
        cursor.close()
        connection.close()

# 2. View Expenses Endpoint
@app.get("/view-expenses")
async def view_expenses():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM expenses WHERE user_id = 1")
        expenses = cursor.fetchall()
        return {"expenses": expenses}
    except mysql.connector.Error as err:
        raise HTTPException(status_code=500, detail=f"Error retrieving expenses: {err}")
    finally:
        cursor.close()
        connection.close()

# 3. Set Savings Goal Endpoint
@app.post("/set-savings-goal")
async def set_savings_goal(goal: SavingsGoal):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute(
            """
            INSERT INTO savings_goals (user_id, goal_name, target_amount, saved_amount, deadline)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (1, goal.goal_name, goal.target_amount, goal.saved_amount, goal.deadline)
        )
        connection.commit()
        return {"message": "Savings goal set successfully"}
    except mysql.connector.Error as err:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error setting savings goal: {err}")
    finally:
        cursor.close()
        connection.close()

# 4. Get Budgeting Advice Endpoint
@app.get("/get-budgeting-advice")
async def get_budgeting_advice():
    advice = [
        "Track your expenses daily.",
        "Set aside at least 20% of your income for savings.",
        "Review your spending monthly and adjust your budget."
    ]
    return {"budgeting_advice": advice}

# 5. Get Savings Tips Endpoint
@app.get("/get-savings-tips")
async def get_savings_tips():
    tips = [
        "Automate your savings to ensure consistency.",
        "Cut down on non-essential expenses.",
        "Create an emergency fund for unexpected situations."
    ]
    return {"savings_tips": tips}

# 6. Dialogflow Interaction Endpoint
@app.post("/dialogflow-query")
async def dialogflow_query(text: str):
    try:
        # Replace with your Dialogflow project ID and session ID (can use a random string)
        project_id = "personal-finance-chatbot-mk9x"
        session_id = "123456789"  # You can make this dynamic if needed
        response = detect_intent_texts(project_id, session_id, text)

        # Return Dialogflow's response
        return {"query_text": text, "dialogflow_response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error with Dialogflow interaction: {str(e)}")

