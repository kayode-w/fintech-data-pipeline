import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
import os

random.seed(42) # This ensures that the same random values are generated each time the code is run, which is important for testing and debugging purposes. 

DATA_TABLES = "data_tables" # this is the name of the folder where the data will be saved. 
os.makedirs(DATA_TABLES, exist_ok=True) # create the folder if it doesn't exist

fake = Faker()

# Constants for USERS TABLE generation
NUM_OF_USERS = 1800
NUM_OF_TRANSACTIONS = 10000
NUM_OF_EVENTS = 5000


COUNTRIES = ['USA', 'UK', 'Germany', 'France', 'Italy', 'Spain', 'Australia', 'Canada', 'Brazil', 'India', 'Nigeria',
             'Kenya', 'South Africa', 'Egypt', 'Morocco', 'Algeria', 'Tunisia', 'Ghana', 'Uganda',  'Portugal']
COUNTRY_WEIGHTS = [0.18, 0.10, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04, 0.04, 0.07, 0.02, 0.02, 0.02, 0.02,
                   0.02, 0.02, 0.02, 0.02, 0.05]

PLANS = ['basic', 'standard', 'premium']
PLANS_WEIGHTS = [0.50, 0.30, 0.20]

DEVICE_TYPES = ['iOS', 'Android', 'Web']
DEVICE_TYPE_WEIGHTS = [45, 35, 20]

ACCOUNT_STATUSES = ['active', 'churned', 'suspended']
ACCOUNT_STATUS_WEIGHTS = [0.70, 0.20, 0.10]


# Constants for TRANSACTIONS TABLE generation
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

# Constants for APP_EVENTS TABLE generation

EVENT_TYPES = ['login', 'logout', 'check_balance', 'send_money', 'receive_money', 'update_profile', 'kyc_submitted', 'failed_login']
EVENT_TYPE_WEIGHTS = [20, 15, 25, 15, 10, 5, 5, 5]

PLATFORM_TYPES = ['mobile', 'web']
PLATFORM_TYPE_WEIGHTS = [70, 30]

# Define a date range for user account creation and transactions
START_DATE = datetime(2021,1,1,0,0,0)
END_DATE = datetime(2025,10,1,23,59,59)


def random_date(start, end):
    delta = end - start # stores the duration between the start and end date as a timedelta object e.g delta = 365 days, 23:59:59
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
            'country': random.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0], #k returns a list of n items, we want the first element (drop the list)
            'plan': random.choices(PLANS, weights=PLANS_WEIGHTS, k=1)[0],
            'account_status': random.choices(ACCOUNT_STATUSES, weights=ACCOUNT_STATUS_WEIGHTS, k=1)[0],
            'created_at': random_date(START_DATE, END_DATE),
            'kyc_verified': random.choices([True, False], weights=[0.6, 0.4], k=1)[0],
            'device_type': random.choices(DEVICE_TYPES, weights=DEVICE_TYPE_WEIGHTS, k=1)[0]
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


def app_events(users_df: pd.DataFrame)-> pd.DataFrame:
    events = []

    for _ in range(NUM_OF_EVENTS):
       
       user = users_df.sample(1).iloc[0] # again, we need to pick a random user row from the users df to get user_id info 
                                         # for the n times in NUM_OF_EVENTS. The selection can pick the same user multiple times.
       platform = ['mobile' if user['device_type'] in ['iOS', 'Android'] else 'web'][0] # determine the platform type based on the user's device type. If device type is iOS or Android, platform is mobile, otherwise it's web.

       event = {
           'event_id': fake.uuid4(),
           'user_id': user['user_id'], # get a random user id from the users dataframe
           'event_type': random.choices(EVENT_TYPES, weights=EVENT_TYPE_WEIGHTS, k=1)[0],
           'platform_type': platform,
           'event_timestamp': random_date(START_DATE, END_DATE),
           'device_type': user['device_type'] # get the device type of the user from the users dataframe
       }
       events.append(event)
    return pd.DataFrame(events)


def generate_wallet_balance(users_df: pd.DataFrame) -> pd.DataFrame:

    wallets = []
    for _, user in users_df.iterrows(): # iterate through each user in the users dataframe (just using this to get the user_id & country)

        wallet = {
            'wallet_id': fake.uuid4(),
            'user_id': user['user_id'],
            'balance': round(random.uniform(0, 10000), 2),
            'currency': CURRENCY_MAP.get(user['country']),
            'last_updated': random_date(START_DATE, END_DATE)
        }
        wallets.append(wallet)
    return pd.DataFrame(wallets)




# Now we create functions to inject anolamies into the various data tables.

def lower_caps_anomaly(df: pd.DataFrame, idx: list, field: str) -> pd.DataFrame:
    df.loc[idx, field] = df.loc[idx, field].str.lower() # convert the values in the specified field to lowercase for the selected rows. 
    return df

def white_space_anomaly(df: pd.DataFrame, idx: list, field: str) -> pd.DataFrame:
    df.loc[idx, field] = df.loc[idx, field].apply(lambda x: x + ' ' if pd.notnull(x) else x)
    return df

def null_value_anomaly(df: pd.DataFrame, idx: list, field: str) -> pd.DataFrame:
    df.loc[idx, field] = np.nan # set the values in the specified field to null for the selected rows.
    return df

def inject_string_anomaly(df: pd.DataFrame, idx: list, field: str) -> pd.DataFrame:
    df[field] = df[field].astype(object) # convert the field to object type to allow for string values
    df.loc[idx, field] = df.loc[idx, field].apply(lambda x: str(x))
    return df

def inject_users_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    user_tbl = df.copy()
    
    #I need a way to collect the indexes of rows i want to inject the anomalies into. Stores them into a list.
    lower_caps_idx = user_tbl.sample(frac=0.18, random_state=42).index # randomly select 10% of the rows to inject anomalies into. Setting random state to ensure reproducibility.
    white_space_idx = user_tbl.sample(frac=0.11, random_state=7).index # randomly select 11% of the rows to inject anomalies into. Setting random state to ensure reproducibility. 
    null_value_idx = user_tbl.sample(frac= 0.08, random_state = 10).index # randomly select 8% of the rows to inject anomalies into. Setting random state to ensure reproducibility.

    user_tbl = lower_caps_anomaly(user_tbl, lower_caps_idx, 'country')
    # user_tbl = user_tbl.iloc[idx, 'country'] = user_tbl.iloc[idx]['country'].str.lower() # without he helper function
    user_tbl = white_space_anomaly(user_tbl, white_space_idx, 'email')
    user_tbl = null_value_anomaly(user_tbl, null_value_idx, 'email')
    user_tbl = null_value_anomaly(user_tbl, null_value_idx, 'plan')
    user_tbl = null_value_anomaly(user_tbl, null_value_idx, 'country')
    user_tbl = white_space_anomaly(user_tbl, white_space_idx, 'first_name')
    user_tbl = lower_caps_anomaly(user_tbl, lower_caps_idx, 'last_name')
    user_tbl = null_value_anomaly(user_tbl, null_value_idx, 'last_name')

    print(f"Anomalies successfully injected into: {user_tbl.shape[0]} rows.")
    return user_tbl

def inject_transactions_anomalies(df: pd.DataFrame) -> pd.DataFrame:

    txn_tbl = df.copy() 

    convert_str_idx = txn_tbl.sample(frac= 0.25, random_state=15).index
    null_values_idx = txn_tbl.sample(frac=0.18, random_state=25).index

    txn_tbl = inject_string_anomaly(txn_tbl, convert_str_idx, 'amount')
    txn_tbl = null_value_anomaly(txn_tbl, null_values_idx, 'currency_rate')
    txn_tbl = null_value_anomaly(txn_tbl, null_values_idx, 'transaction_status')

    print(f"Anomalies successfully injected into: {txn_tbl.shape[0]} rows.")
    return txn_tbl


def inject_app_event_anomalies(users_tbl: pd.DataFrame, events_tbl: pd.DataFrame) -> pd.DataFrame:
    evnt_tbl = events_tbl.copy()

    # need to merge to bring in created_at so that I can compare with timestamp.
    evnt_tbl = evnt_tbl.merge(users_tbl[['user_id', 'created_at']], on = 'user_id', how = 'left') 

    # We get random rows reom the table we want to infect
    null_platform_idx = evnt_tbl.sample(frac= 0.22, random_state=35).index
    irreg_time_stamp_idx = evnt_tbl.sample(frac=0.15, random_state=45).index

    # we get random numbers in plac of days we would subtract reom event_timestamp
    rndm_days = [random.randint(1, 30) for _ in range(len(irreg_time_stamp_idx))] # generate random number of days to add to the created_at date to create irregular timestamps.

    # for all the dates picked, replace them with a subtraction of random days that we created. Thois would create irregular timestamps that are before the user's created_at date.
    evnt_tbl.loc[irreg_time_stamp_idx, 'event_timestamp'] = evnt_tbl.loc[irreg_time_stamp_idx, 'created_at'] - pd.to_timedelta(rndm_days, unit = 'D') 

    # drop the created_at column as we no longer need it after creating the irregular timestamps.
    evnt_tbl = evnt_tbl.drop(columns=['created_at']) 

    # now to apply the null platform type anomaly to the selected rows.
    evnt_tbl = null_value_anomaly(evnt_tbl, null_platform_idx, 'platform_type')
    print(f"Anomalies successfully injected into: {evnt_tbl.shape[0]} rows.")

    return evnt_tbl


def inject_wallet_anomalies(df: pd.DataFrame) -> pd.DataFrame:
    wallet_tb = df.copy()

    negative_balance_idx = wallet_tb.sample(frac=0.34, random_state=55).index
    null_currencies_idx = wallet_tb.sample(frac=0.20, random_state=65).index

    # make the balance negative for the selected rows.
    wallet_tb.loc[negative_balance_idx, 'balance'] = wallet_tb.loc[negative_balance_idx, 'balance'] * -1 # make the balance negative for the selected rows.

    # inject null currency anomaly for the selected rows.
    wallet_tb = null_value_anomaly(wallet_tb, null_currencies_idx, 'currency')
    print(f"Anomalies successfully injected into: {wallet_tb.shape[0]} rows.")
    return wallet_tb



def save_to_csv(df: pd.DataFrame, tbl_name: str) -> None:
   data_tbl_export = os.path.join(DATA_TABLES, f'{tbl_name}.csv') # this will create a path to save the data. E.g data_tables/users.csv
   df.to_csv(data_tbl_export, index=False)
   print(f"'{tbl_name}' saved successfully to {data_tbl_export}")
