import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

NUM_OF_USERS = 1800

COUNTRIES = ['USA', 'UK', 'Germany', 'France', 'Italy', 'Spain', 'Australia', 'Canada', 'Brazil', 'India', 'Nigeria',
             'Kenya', 'South Africa', 'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Ghana', 'Uganda',  'Portugal']
COUNTRY_WEIGHTS = [0.18, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.07, 0.02, 0.02, 0.02, 0.02,
                   0.02, 0.02, 0.02, 0.02, 0.05]

PLANS = ['basic', 'standard', 'premium']
PLANS_WEIGHTS = [0.50, 0.30, 0.20]

ACCOUNT_STATUSES = ['active', 'churned', 'suspended']
ACCOUNT_STATUS_WEIGHTS = [0.70, 0.20, 0.10]

START_DATE = datetime(2021,1,1,0,0,0)
END_DATE = datetime(2025,10,1,23,59,59)

def random_date(start, end):
    delta = end - start
    random_days = random.randint(0, delta.days) # picking random days between the duratuion of start and end date
    days = start + timedelta(days=random_days) # land on a random date by adding the random days to the start date
    return days # return the randome date

def generate_users():
    users = []
    for _ in range(NUM_OF_USERS):
        user = {
            'user_id': fake.uuid4(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'country': random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0], #k returns a list of n items, we want the first element
            'plan': random.choices(PLANS, weights=PLANS_WEIGHTS, k=1)[0],
            'account_status': random.choices(ACCOUNT_STATUSES, weights=ACCOUNT_STATUS_WEIGHTS, k=1)[0],
            'created_at': random_date(START_DATE, END_DATE),
            'kyc_verified': random.choices([True, False], weights=[0.6, 0.4], k=1)[0]
        }

        users.append(user)
    return pd.DataFrame(users)