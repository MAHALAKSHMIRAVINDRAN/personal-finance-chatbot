import requests
import logging
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000"  # Adjust this if the server is running elsewhere

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# 1. Test Log Expenses
def test_log_expense():
    payload = {
        "category": "Food",
        "amount": 20.50,
        "date": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")  # Dynamic date
    }
    response = requests.post(f"{BASE_URL}/log-expense", json=payload)
    logging.info("Log Expense Response: %s", response.json())
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

# 2. Test View Expenses
def test_view_expenses():
    response = requests.get(f"{BASE_URL}/view-expenses")
    logging.info("View Expenses Response: %s", response.json())
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert isinstance(response.json().get("expenses"), list), "Expected expenses to be a list"

# 3. Test Set Savings Goal
def test_set_savings_goal():
    payload = {
        "goal_name": "Emergency Fund",
        "target_amount": 5000.00,  # Correct field name (instead of goal_amount)
        "saved_amount": 0.0,  # Optional field
        "deadline": (datetime.now() + timedelta(days=365)).strftime("%Y-%m-%d")
        # Correct field name (instead of target_date)
    }
    response = requests.post(f"{BASE_URL}/set-savings-goal", json=payload)
    logging.info("Set Savings Goal Response: %s", response.json())
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"

# 4. Test Get Budgeting Advice
def test_get_budgeting_advice():
    response = requests.get(f"{BASE_URL}/get-budgeting-advice")
    logging.info("Get Budgeting Advice Response: %s", response.json())
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert isinstance(response.json().get("budgeting_advice"), list), "Expected budgeting_advice to be a list"

# 5. Test Get Savings Tips
def test_get_savings_tips():
    response = requests.get(f"{BASE_URL}/get-savings-tips")
    logging.info("Get Savings Tips Response: %s", response.json())
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    assert isinstance(response.json().get("savings_tips"), list), "Expected savings_tips to be a list"

if __name__ == "__main__":
    # Run all tests
    test_log_expense()
    test_view_expenses()
    test_set_savings_goal()
    test_get_budgeting_advice()
    test_get_savings_tips()






