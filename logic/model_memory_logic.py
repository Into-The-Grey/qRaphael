import os
import psycopg2
from dotenv import load_dotenv
import random

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

def connect_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD
    )
    return conn

def fetch_user_memory(user_id, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT memory_text FROM user_memory WHERE user_id = %s ORDER BY timestamp",
                (user_id,),
            )
            results = cursor.fetchall()
            memory = "\n".join([result[0] for result in results])
            return memory
    except Exception as e:
        print(f"Error fetching user memory: {e}")
        return ""

def save_user_memory(user_id, user_memory, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO user_memory (user_id, memory_text)
                VALUES (%s, %s)
            """,
                (user_id, user_memory),
            )
            conn.commit()
    except Exception as e:
        print(f"Error saving user memory: {e}")

def fetch_user_name(user_id, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM users WHERE user_id = %s", (user_id,))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
    except Exception as e:
        print(f"Error fetching user name: {e}")
        return None

def update_user_name(user_id, name, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "UPDATE users SET name = %s WHERE user_id = %s", (name, user_id)
            )
            conn.commit()
    except Exception as e:
        print(f"Error updating user name: {e}")

def get_raphael_identity():
    identities = [
        "your personal assistant",
        "an assistant of sorts",
        "your AI assistant",
        "your digital assistant",
        "a helpful assistant",
    ]
    capabilities = [
        "I can help you manage your schedule.",
        "I can provide information on various topics.",
        "I can assist with your daily tasks.",
        "I can offer suggestions on things to do.",
        "I can help you track your health and fitness.",
        "I can assist with managing your finances.",
    ]
    identity = {
        "name": "Raphael",
        "role": random.choice(identities),
        "capabilities": capabilities,
    }
    return identity

def get_suggestions(user_preferences):
    suggestions = [
        "How about going for a walk?",
        "Maybe you could read a book.",
        "How about cooking a new recipe?",
        "You could watch a movie.",
        "Why not try a new hobby?",
    ]
    if user_preferences:
        if "outdoors" in user_preferences.get("hobbies", "").lower():
            suggestions.append("How about a hike?")
        if "reading" in user_preferences.get("hobbies", "").lower():
            suggestions.append("You could read a new book.")
    return random.sample(suggestions, 3)

def fetch_user_details(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT detail_type, detail_value FROM user_details WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        details = {result[0]: result[1] for result in results}
        return details

def fetch_user_preferences(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT preference_type, preference_value FROM user_preferences WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        preferences = {result[0]: result[1] for result in results}
        return preferences

def fetch_medical_conditions(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT condition_name, diagnosis_date, status FROM medical_conditions WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        conditions = [
            {
                "condition_name": result[0],
                "diagnosis_date": result[1],
                "status": result[2],
            }
            for result in results
        ]
        return conditions

def fetch_medications(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT medication_name, dosage, start_date, end_date, prescribing_doctor FROM medications WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        medications = [
            {
                "medication_name": result[0],
                "dosage": result[1],
                "start_date": result[2],
                "end_date": result[3],
                "prescribing_doctor": result[4],
            }
            for result in results
        ]
        return medications

def fetch_immunizations(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT vaccine_name, vaccination_date FROM immunizations WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        immunizations = [
            {"vaccine_name": result[0], "vaccination_date": result[1]}
            for result in results
        ]
        return immunizations

def fetch_doctor_visits(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT doctor_name, visit_date, notes FROM doctor_visits WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        visits = [
            {"doctor_name": result[0], "visit_date": result[1], "notes": result[2]}
            for result in results
        ]
        return visits

def fetch_insurance_info(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT provider_name, policy_number, coverage_details FROM insurance_info WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        insurance = [
            {
                "provider_name": result[0],
                "policy_number": result[1],
                "coverage_details": result[2],
            }
            for result in results
        ]
        return insurance

def fetch_health_metrics(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT metric_name, metric_value, recorded_date FROM health_metrics WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        metrics = [
            {
                "metric_name": result[0],
                "metric_value": result[1],
                "recorded_date": result[2],
            }
            for result in results
        ]
        return metrics

def fetch_investments(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT investment_type, investment_value, investment_date FROM investments WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        investments = [
            {
                "investment_type": result[0],
                "investment_value": result[1],
                "investment_date": result[2],
            }
            for result in results
        ]
        return investments

def fetch_retirement_accounts(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT account_type, account_value, institution FROM retirement_accounts WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        accounts = [
            {
                "account_type": result[0],
                "account_value": result[1],
                "institution": result[2],
            }
            for result in results
        ]
        return accounts

def fetch_tax_information(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT tax_year, filing_status, taxable_income FROM tax_information WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        taxes = [
            {
                "tax_year": result[0],
                "filing_status": result[1],
                "taxable_income": result[2],
            }
            for result in results
        ]
        return taxes

def fetch_expense_tracking(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT expense_category, expense_amount, expense_date FROM expense_tracking WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        expenses = [
            {
                "expense_category": result[0],
                "expense_amount": result[1],
                "expense_date": result[2],
            }
            for result in results
        ]
        return expenses

def fetch_professional_info(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT employment_history, current_job, skills_certifications FROM professional_info WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {
                "employment_history": result[0],
                "current_job": result[1],
                "skills_certifications": result[2],
            }
        else:
            return {}

def fetch_educational_data(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT degrees, courses, languages FROM educational_data WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {"degrees": result[0], "courses": result[1], "languages": result[2]}
        else:
            return {}

def fetch_preferences_interests(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT hobbies, food_preferences, travel_preferences, entertainment FROM preferences_interests WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {
                "hobbies": result[0],
                "food_preferences": result[1],
                "travel_preferences": result[2],
                "entertainment": result[3],
            }
        else:
            return {}

def fetch_social_connections(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT family_members, friends, social_media_accounts FROM social_connections WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {
                "family_members": result[0],
                "friends": result[1],
                "social_media_accounts": result[2],
            }
        else:
            return {}

def fetch_security_info(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT passwords, security_questions FROM security_info WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {"passwords": result[0], "security_questions": result[1]}
        else:
            return {}

def fetch_miscellaneous_info(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT vehicle_info, property_info, subscriptions, shopping_history FROM miscellaneous_info WHERE user_id = %s",
            (user_id,),
        )
        result = cursor.fetchone()
        if result:
            return {
                "vehicle_info": result[0],
                "property_info": result[1],
                "subscriptions": result[2],
                "shopping_history": result[3],
            }
        else:
            return {}

def fetch_cards(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT card_type, card_number, expiry_date, cvv FROM cards WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        cards = [
            {
                "card_type": result[0],
                "card_number": result[1],
                "expiry_date": result[2],
                "cvv": result[3],
            }
            for result in results
        ]
        return cards

def fetch_bank_accounts(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT bank_name, account_number, routing_number FROM bank_accounts WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        bank_accounts = [
            {
                "bank_name": result[0],
                "account_number": result[1],
                "routing_number": result[2],
            }
            for result in results
        ]
        return bank_accounts

def fetch_loans(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT loan_type, loan_amount, loan_date, due_date FROM loans WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        loans = [
            {
                "loan_type": result[0],
                "loan_amount": result[1],
                "loan_date": result[2],
                "due_date": result[3],
            }
            for result in results
        ]
        return loans

def fetch_salaries(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT salary_amount, salary_date FROM salaries WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        salaries = [
            {"salary_amount": result[0], "salary_date": result[1]} for result in results
        ]
        return salaries

def fetch_debts(user_id, conn):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT debt_type, debt_amount, debt_date FROM debts WHERE user_id = %s",
            (user_id,),
        )
        results = cursor.fetchall()
        debts = [
            {"debt_type": result[0], "debt_amount": result[1], "debt_date": result[2]}
            for result in results
        ]
        return debts

def fetch_request_changes(user_id, table, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"SELECT request_changes FROM {table} WHERE user_id = %s", (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return True
    except Exception as e:
        print(f"Error fetching request_changes from {table}: {e}")
        return True

def update_request_changes(user_id, table, status, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                f"UPDATE {table} SET request_changes = %s WHERE user_id = %s",
                (status, user_id),
            )
            conn.commit()
    except Exception as e:
        print(f"Error updating request_changes in {table}: {e}")

def add_user(user_id, name, email, phone, birthday, conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO users (user_id, name, email, phone, birthday)
                VALUES (%s, %s, %s, %s, %s)
            """,
                (user_id, name, email, phone, birthday),
            )
            conn.commit()
    except Exception as e:
        print(f"Error adding user: {e}")
