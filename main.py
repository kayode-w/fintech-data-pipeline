from dealer import generate_users, generate_transactions, app_events, generate_wallet_balance, inject_transactions_anomalies, inject_users_anomalies, save_to_csv



users = generate_users()
transactions = generate_transactions(users)
events = app_events(users)
wallet_balance = generate_wallet_balance(users)

users_2 = inject_users_anomalies(users)
transactions_2 = inject_transactions_anomalies(transactions)

print(transactions_2.loc[transactions_2['amount'].apply(lambda x: isinstance(x, str()))].head())