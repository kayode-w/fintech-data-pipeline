import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

NUM_OF_USERS = 1800

NUM_OF_TRANSACTIONS = 10000

COUNTRIES = ['USA', 'UK', 'Germany', 'France', 'Italy', 'Spain', 'Australia', 'Canada', 'Brazil', 'India', 'Nigeria',
             'Kenya', 'South Africa', 'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Ghana', 'Uganda',  'Portugal']
COUNTRY_WEIGHTS = [0.18, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.07, 0.02, 0.02, 0.02, 0.02,
                   0.02, 0.02, 0.02, 0.02, 0.05]

PLANS = ['basic', 'standard', 'premium']
PLANS_WEIGHTS = [0.50, 0.30, 0.20]

ACCOUNT_STATUSES = ['active', 'churned', 'suspended']
ACCOUNT_STATUS_WEIGHTS = [0.70, 0.20, 0.10]

TRANSACTION_TYPES = ['send', 'receive', 'deposit', 'withdrawal']
TRANSACTION_TYPE_WEIGHTS = [0.35, 0.35, 0.20, 0.10]

TRANSACTION_STATUSES = ['completed', 'failed', 'pending', 'reversed']
TRANSACTION_STATUS_WEIGHTS = [0.75, 0.12, 0.08, 0.05]

CURRENCY_MAP = {
    'USA': 'USD', 'UK': 'GBP', 'Germany': 'EUR', 'France': 'EUR',
    'Italy': 'EUR', 'Spain': 'EUR', 'Portugal': 'EUR', 'Australia': 'AUD',
    'Canada': 'CAD', 'Brazil': 'BRL', 'India': 'INR', 'Nigeria': 'NGN',
    'Kenya': 'KES', 'South Africa': 'ZAR', 'Egypt': 'EGP', 'Morocco': 'MAD',
    'Algeria': 'DZD', 'Tunisia': 'TND', 'Ghana': 'GHS', 'Ethiopia': 'ETB',
    'Uganda': 'UGX'
}
CURRENCY_RATES = {
    'USD': 1.0, 'GBP': 1.27, 'EUR': 1.08, 'AUD': 0.65,
    'CAD': 0.74, 'BRL': 0.20, 'INR': 0.012, 'NGN': 0.00065,
    'KES': 0.0077, 'ZAR': 0.055, 'EGP': 0.021, 'MAD': 0.10,
    'DZD': 0.0074, 'TND': 0.32, 'GHS': 0.069, 'ETB': 0.018,
    'UGX': 0.00027
}

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


def generate_transactions(users_df: pd.DataFrame)-> pd.DataFrame:
    transactions = []
    for _ in range(NUM_OF_TRANSACTIONS):
        sender = users_df.sample(1).iloc[0] # gets a random user from the users dataframe to be the sender of the transaction. Iloc[0] to get the result as a series.
        receiver = users_df.sample(1).iloc[0]

        while sender['user_id'] == receiver['user_id']:
            receiver = users_df.sample(1).iloc[0] # while the sender and receiver are the same, keep picking a random user until we get a different one

        currency = CURRENCY_MAP.get(sender['country']) # get sender's country and use it to look up the corresponding currency.
        rate = CURRENCY_RATES[currency] 
        local_amount = round(random.uniform(5, 5000), 2)
        
        transaction = {
            'transaction_id': fake.uuid4(),
            'sender_id': sender['user_id'],
            'receiver_id': receiver['user_id'],
            'currency': currency,
            'amount': local_amount,
            'currency_rate': rate,
            'transaction_status': random.choices(TRANSACTION_STATUSES, weights=TRANSACTION_STATUS_WEIGHTS, k=1)[0],
            'transaction_type': random.choices(TRANSACTION_TYPES, weights=TRANSACTION_TYPE_WEIGHTS, k=1)[0],
            'transaction_date': random_date(sender.get('created_at'), END_DATE)
        }
        transactions.append(transaction)
    return pd.DataFrame(transactions)