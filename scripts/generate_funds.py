import os
from dotenv import load_dotenv
import random
import psycopg2
from psycopg2.extras import RealDictCursor
import ollama
from faker import Faker
import time

OLLAMA_MODEL = "llama3.2:1b"

UNIT_TYPE_WEIGHTS = {
    "chancellor": 1,
    "college": 3,
    "department": 6
}

CAPACITY_TIERS = [5000, 10000, 25000, 100000, 500000, 1000000]

FUND_NAME_TEMPLATES = [
    "The {last_name} Family Fund",
    "The {last_name} Family Fund for {subpurpose}",
    "The {last_name} Endowment",
    "The {last_name} Endowment for {subpurpose}"
]

load_dotenv()
def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
    )

def fetch_units(conn):
    # with statement automatically closes cur after the block,
    # guaranteeing resource cleanup and prevent memory leaks/file corruption
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, path, unit_type FROM units")
        return cur.fetchall()
    
def fetch_subpurposes(conn):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("SELECT id, name, path FROM subpurposes")
        return cur.fetchall()

def pick_combo(units, subpurposes):
    weights = [UNIT_TYPE_WEIGHTS[u["unit_type"]] for u in units]
    unit = random.choices(units, weights=weights, k=1)[0]
    subpurpose = random.choice(subpurposes)
    return unit, subpurpose

def generate_capacity_min():
    return random.choice(CAPACITY_TIERS)

def generate_fund_name(subpurpose_name, faker):
    template = random.choice(FUND_NAME_TEMPLATES)
    return template.format(last_name=faker.last_name(), subpurpose=subpurpose_name)

def generate_fund_terms(fund_name, unit_name, subpurpose_name, capacity_min):
    prompt = (
        f"Write a 2-3 sentence mission description for a university gift fund. \n"
        f"Fund name: {fund_name}\n"
        f"Unit: {unit_name}\n"
        f"Purpose: {subpurpose_name}\n"
        f"Minimum gift amount: ${capacity_min:,}\n\n"
        "Only use the facts give above. Do not invent additional dollar amounts, "
        "dates, or donor details. Write in a formal, mission-statement tone."
    )

    result = ollama.generate(model=OLLAMA_MODEL, prompt=prompt)
    return result["response"].strip()

def insert_fund(conn, fund_name, unit_id, subpurpose_id, capacity_min, fund_terms):
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO funds (fund_name, unit_id, subpurpose_id, capacity_min, fund_terms)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (fund_name, unit_id, subpurpose_id, capacity_min, fund_terms),
        )

def main():
    conn = get_connection()
    units = fetch_units(conn)
    subpurposes = fetch_subpurposes(conn)
    faker = Faker()
    start_time = time.time()

    print("Fund generation started.")

    total_funds = 5000
    for i in range(total_funds):
        unit, subpurpose = pick_combo(units, subpurposes)
        capacity_min = generate_capacity_min()
        fund_name = generate_fund_name(subpurpose["name"], faker)
        fund_terms = generate_fund_terms(fund_name, unit["name"], subpurpose["name"], capacity_min)
        insert_fund(conn, fund_name, unit["id"], subpurpose["id"], capacity_min, fund_terms)

        if (i+1)%10 == 0:
            conn.commit()
            elapsed_time = time.time() - start_time
            elapsed_minutes = int(elapsed_time // 60)
            elapsed_seconds = int(elapsed_time % 60)
            print(f"{i+1}/{total_funds} funds generated. {elapsed_minutes}:{elapsed_seconds} elapsed.")

    conn.commit()
    conn.close()
    print(f"Done. {total_funds} funds generated.")

if __name__ == "__main__":
    main()