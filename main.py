from dealer import generate_users, generate_transactions, app_events, generate_wallet_balance, inject_transactions_anomalies, inject_users_anomalies, inject_app_event_anomalies, inject_wallet_anomalies, save_to_csv  
from pipeline import table_extraction, name_proper_case, transform_app_events, transform_users, transform_transactions, transform_wallets
from loader import load_sql, engine
from datetime import datetime, timedelta

# Generate the data for the tables

users = generate_users()
transactions = generate_transactions(users)
events = app_events(users)
wallet_balance = generate_wallet_balance(users)


# Inject the anomalies into the generated data
users_2 = inject_users_anomalies(users)
transactions_2 = inject_transactions_anomalies(transactions)
events_2 = inject_app_event_anomalies(users, events)
wallet_balance_2 = inject_wallet_anomalies(wallet_balance)
# print(transactions_2.loc[transactions_2['amount'].apply(lambda x: isinstance(x, str()))].head())

# Export the generated data to CSV files

save_to_csv(users_2, 'users')
save_to_csv(transactions_2, 'transactions')
save_to_csv(events_2, 'app_events')
save_to_csv(wallet_balance_2, 'wallet_balances')

# Extract the data from the CSV files and load it into pandas DataFrames

users_df = table_extraction('users')
transactions_df = table_extraction('transactions')
events_df = table_extraction('app_events')
wallet_balance_df = table_extraction('wallet_balances')


users_df = transform_users(users_df)
transactions_df = transform_transactions(transactions_df, users_df )
wallets_df = transform_wallets(wallet_balance_df, users_df)
app_events_df = transform_app_events(events_df, users_df)


D_TABLES = {
    'users':  users_df,
    'transactions': transactions_df,
    'events': app_events_df,
    'wallet_balance': wallets_df
}

for table_name, df in D_TABLES.items():
    load_sql(df, table_name, engine)



# print(app_events_df.head(10))

# print(wallets_df.loc[wallets_df['currency'].isnull()])

# print(users_df.loc[users_df['country'].isnull(), 'country'])



