#!/usr/bin/env python3
"""
generate_data.py - Generate dummy HR data for:
    employees.csv, managers.csv, performance_reviews.csv,
    training_records.csv, turnover.csv
Uses Faker library.
"""

import csv
import random
from datetime import datetime, timedelta, date
from faker import Faker

fake = Faker()
Faker.seed(42)
random.seed(42)

# Configuration
NUM_EMPLOYEES = 200
START_DATE = datetime(2015, 1, 1)
END_DATE = datetime(2025, 6, 1)

# Departments
DEPARTMENTS = ["HR", "Engineering", "Sales", "Marketing", "Finance", "Customer Support"]
TRAINING_COURSES = [
    "Leadership 101", "Python Basics", "Sales Negotiation", "Customer Service Excellence",
    "Financial Analysis", "DEI Workshop", "Project Management", "Data Privacy"
]
TURNOVER_REASONS = [
    "Better offer", "Relocation", "Career change", "Retirement", "Layoff",
    "Personal reasons", "Performance issues", "End of contract"
]

def random_date(start, end):
    # Convert date objects to datetime if needed
    if isinstance(start, date) and not isinstance(start, datetime):
        start = datetime(start.year, start.month, start.day)
    if isinstance(end, date) and not isinstance(end, datetime):
        end = datetime(end.year, end.month, end.day)
    delta = end - start
    random_days = random.randint(0, delta.days)
    return (start + timedelta(days=random_days)).date()

def random_rating():
    return round(random.uniform(1.0, 5.0), 1)

def random_score():
    # 20% chance of NULL (no score)
    if random.random() < 0.2:
        return None
    return random.randint(60, 100)

# ---------- 1. Generate employees ----------
print("Generating employee data...")
employees = []
for emp_id in range(1, NUM_EMPLOYEES + 1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = f"{first_name.lower()}.{last_name.lower()}@company.com"
    hire_date = random_date(START_DATE, END_DATE)
    department = random.choice(DEPARTMENTS)
    employees.append([emp_id, first_name, last_name, hire_date, department, email])
    if emp_id % 50 == 0:
        print(f"  Generated {emp_id}/{NUM_EMPLOYEES} employees...")

print(f"✓ Generated {NUM_EMPLOYEES} employees")

# Write employees.csv
print("Writing employees.csv...")
with open("employees.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["employee_id", "first_name", "last_name", "hire_date", "department", "email"])
    writer.writerows(employees)
print("✓ Saved employees.csv")

# ---------- 2. Generate managers (subset of employees, ~20%) ----------
print("\nGenerating manager assignments...")
manager_emp_ids = random.sample(range(1, NUM_EMPLOYEES + 1), k=int(NUM_EMPLOYEES * 0.2))
managers = []
for idx, emp_id in enumerate(manager_emp_ids, start=1):
    # Find employee's department
    emp_department = next(e[4] for e in employees if e[0] == emp_id)
    # Manager start date is at least hire_date + random days
    hire_date = next(e[3] for e in employees if e[0] == emp_id)
    # Start management role sometime after hire (0 to 2 years later)
    start_offset = random.randint(0, 730)  # days
    start_date = hire_date + timedelta(days=start_offset)
    if start_date > END_DATE.date():
        start_date = END_DATE.date()
    managers.append([idx, emp_id, emp_department, start_date])
    if idx % 10 == 0:
        print(f"  Assigned {idx} managers...")

print(f"✓ Generated {len(managers)} manager assignments ({len(managers)/NUM_EMPLOYEES*100:.1f}% of workforce)")

print("Writing managers.csv...")
with open("managers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["manager_id", "employee_id", "department", "start_date"])
    writer.writerows(managers)
print("✓ Saved managers.csv")

# ---------- 3. Performance reviews (1-3 per employee) ----------
print("\nGenerating performance reviews...")
performance_reviews = []
review_id = 1
for emp_idx, emp in enumerate(employees, start=1):
    emp_id = emp[0]
    hire_date = emp[3]
    num_reviews = random.randint(1, 3)
    # generate reviews after hire date
    for _ in range(num_reviews):
        review_date = random_date(
            max(hire_date, START_DATE.date()),
            END_DATE.date()
        )
        rating = random_rating()
        comments = fake.sentence() if random.random() > 0.3 else ""
        performance_reviews.append([review_id, emp_id, review_date, rating, comments])
        review_id += 1
    if emp_idx % 50 == 0:
        print(f"  Generated reviews for {emp_idx}/{NUM_EMPLOYEES} employees...")

print(f"✓ Generated {len(performance_reviews)} performance reviews (avg {len(performance_reviews)/NUM_EMPLOYEES:.1f} per employee)")

print("Writing performance_reviews.csv...")
with open("performance_reviews.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["review_id", "employee_id", "review_date", "rating", "comments"])
    writer.writerows(performance_reviews)
print("✓ Saved performance_reviews.csv")

# ---------- 4. Training records (0-4 per employee) ----------
print("\nGenerating training records...")
training_records = []
record_id = 1
for emp_idx, emp in enumerate(employees, start=1):
    emp_id = emp[0]
    hire_date = emp[3]
    num_trainings = random.randint(0, 4)
    courses = random.sample(TRAINING_COURSES, min(num_trainings, len(TRAINING_COURSES)))
    for course in courses:
        completion_date = random_date(
            max(hire_date, START_DATE.date()),
            END_DATE.date()
        )
        score = random_score()
        training_records.append([record_id, emp_id, course, completion_date, score])
        record_id += 1
    if emp_idx % 50 == 0:
        print(f"  Generated training records for {emp_idx}/{NUM_EMPLOYEES} employees...")

null_count = sum(1 for record in training_records if record[4] is None)
print(f"✓ Generated {len(training_records)} training records ({null_count} without scores)")

print("Writing training_records.csv...")
with open("training_records.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["record_id", "employee_id", "training_name", "completion_date", "score"])
    writer.writerows(training_records)
print("✓ Saved training_records.csv")

# ---------- 5. Turnover (15% of employees left) ----------
print("\nGenerating turnover records...")
turnover_employees = random.sample(employees, k=int(NUM_EMPLOYEES * 0.15))
turnover_records = []
turnover_id = 1
for emp in turnover_employees:
    emp_id = emp[0]
    hire_date = emp[3]
    # termination date after hire, before or on END_DATE
    max_term = END_DATE.date()
    term_date = random_date(max(hire_date, START_DATE.date()), max_term)
    if term_date > END_DATE.date():
        term_date = END_DATE.date()
    reason = random.choice(TURNOVER_REASONS)
    turnover_records.append([turnover_id, emp_id, term_date, reason])
    turnover_id += 1

print(f"✓ Generated {len(turnover_records)} turnover events ({len(turnover_records)/NUM_EMPLOYEES*100:.1f}% attrition)")

# Analyze turnover reasons
reason_counts = {}
for record in turnover_records:
    reason = record[3]
    reason_counts[reason] = reason_counts.get(reason, 0) + 1

print("\nTurnover breakdown by reason:")
for reason, count in sorted(reason_counts.items(), key=lambda x: x[1], reverse=True):
    print(f"  - {reason}: {count} ({count/len(turnover_records)*100:.1f}%)")

print("Writing turnover.csv...")
with open("turnover.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["turnover_id", "employee_id", "termination_date", "reason"])
    writer.writerows(turnover_records)
print("✓ Saved turnover.csv")

print("\n" + "="*60)
print("HR DATA GENERATION COMPLETE")
print("="*60)
print("\nGenerated Files:")
print("  ✓ employees.csv")
print("  ✓ managers.csv")
print("  ✓ performance_reviews.csv")
print("  ✓ training_records.csv")
print("  ✓ turnover.csv")

print(f"\nData Summary:")
print(f"  Total Employees: {NUM_EMPLOYEES}")
print(f"  Manager Count: {len(managers)} ({len(managers)/NUM_EMPLOYEES*100:.1f}% of workforce)")
print(f"  Performance Reviews: {len(performance_reviews)} (avg {len(performance_reviews)/NUM_EMPLOYEES:.2f} per employee)")
print(f"  Training Records: {len(training_records)} (avg {len(training_records)/NUM_EMPLOYEES:.2f} per employee)")
print(f"  Turnover Events: {len(turnover_records)} ({len(turnover_records)/NUM_EMPLOYEES*100:.1f}% attrition)")

print(f"\nDepartments Represented:")
dept_counts = {}
for emp in employees:
    dept = emp[4]
    dept_counts[dept] = dept_counts.get(dept, 0) + 1
for dept in sorted(dept_counts.keys()):
    count = dept_counts[dept]
    print(f"  - {dept}: {count} employees")

print(f"\nPerformance Rating Distribution:")
rating_buckets = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
for review in performance_reviews:
    rating = int(review[3])
    rating_buckets[rating] += 1
for rating in sorted(rating_buckets.keys()):
    count = rating_buckets[rating]
    print(f"  - {rating} stars: {count} reviews ({count/len(performance_reviews)*100:.1f}%)")

print(f"\nTraining Score Statistics:")
training_scores = [record[4] for record in training_records if record[4] is not None]
if training_scores:
    avg_score = sum(training_scores) / len(training_scores)
    min_score = min(training_scores)
    max_score = max(training_scores)
    print(f"  - Average Score: {avg_score:.1f}")
    print(f"  - Min Score: {min_score}")
    print(f"  - Max Score: {max_score}")
    print(f"  - Completed Trainings: {len(training_scores)} ({len(training_scores)/len(training_records)*100:.1f}%)")
    print(f"  - Pending Scores: {len(training_records) - len(training_scores)}")

print("\n" + "="*60)
print("Next Steps:")
print("  1. Load CSV files into PostgreSQL database")
print("  2. Configure Metabase dashboards")
print("  3. Set up n8n workflows for data refresh")
print("="*60)