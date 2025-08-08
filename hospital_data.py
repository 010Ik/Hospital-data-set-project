import pandas as pd
import numpy as np
import random
import subprocess
import sys

# Check if Faker is installed, else prompt the user
try:
    from faker import Faker
except ImportError:
    print("Error: Faker module not found. Please install it using:")
    print("       pip install faker")
    sys.exit(1)

# Generate hospital dataset
def generate_hospital_dataset(n_rows=1000):
    fake = Faker()
    np.random.seed(42)
    random.seed(42)

    departments = ['Cardiology', 'Neurology', 'Orthopedics', 'Pediatrics', 'Oncology', 'Emergency', 'Gastroenterology']
    diagnoses = {
        'Cardiology': ['Heart Disease', 'Hypertension', 'Arrhythmia'],
        'Neurology': ['Stroke', 'Epilepsy', 'Migraine'],
        'Orthopedics': ['Fracture', 'Arthritis', 'Dislocation'],
        'Pediatrics': ['Flu', 'Asthma', 'Infection'],
        'Oncology': ['Lung Cancer', 'Breast Cancer', 'Leukemia'],
        'Emergency': ['Accident', 'Burn', 'Poisoning'],
        'Gastroenterology': ['Ulcer', 'Hepatitis', 'IBS']
    }
    outcomes = ['Recovered', 'Referred', 'Deceased']
    genders = ['Male', 'Female', 'Other']

    data = []
    for i in range(n_rows):
        patient_id = f'P{100000+i}'
        age = np.random.randint(1, 100)
        gender = random.choice(genders)
        department = random.choice(departments)
        diagnosis = random.choice(diagnoses[department])
        admission_date = fake.date_between(start_date='-1y', end_date='today')
        length_of_stay = np.random.poisson(lam=5) + 1
        discharge_date = admission_date + pd.Timedelta(days=length_of_stay)
        treatment_cost = round(np.random.normal(3000, 1000) * (length_of_stay / 5), 2)
        treatment_cost = max(treatment_cost, 100)
        insurance_covered = random.choice(['Yes', 'No'])
        outcome = random.choices(outcomes, weights=[0.85, 0.1, 0.05])[0]

        data.append([
            patient_id, age, gender, department, admission_date, discharge_date,
            diagnosis, treatment_cost, insurance_covered, length_of_stay, outcome
        ])

    columns = [
        'Patient_ID', 'Age', 'Gender', 'Department', 'Admission_Date',
        'Discharge_Date', 'Diagnosis', 'Treatment_Cost', 'Insurance_Covered',
        'Length_of_Stay', 'Outcome'
    ]
    df = pd.DataFrame(data, columns=columns)
    return df

# Git commit and push function
def git_commit_push(commit_message, branch='main'):
    try:
        subprocess.run(["git", "add", "."], check=True)
        print("Staged all changes.")

        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        print(f"Committed changes with message: {commit_message}")

        subprocess.run(["git", "push", "origin", branch], check=True)
        print(f"Pushed changes to remote branch '{branch}'.")
    except subprocess.CalledProcessError as e:
        print("Git error:", e)

def main():
    # Generate and save dataset
    df = generate_hospital_dataset()
    filename = "hospital_dataset.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Dataset saved as '{filename}'")

    # Commit and push to GitHub
    commit_msg = "Add generated hospital dataset"
    git_commit_push(commit_msg)

if __name__ == "__main__":
    main()
