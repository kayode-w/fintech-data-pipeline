from dealer import generate_users, generate_transactions, app_events, generate_wallet_balance, inject_transactions_anomalies, inject_users_anomalies, inject_app_event_anomalies, inject_wallet_anomalies, save_to_csv



users = generate_users()
transactions = generate_transactions(users)
events = app_events(users)
wallet_balance = generate_wallet_balance(users)

users_2 = inject_users_anomalies(users)
transactions_2 = inject_transactions_anomalies(transactions)
# print(transactions_2.loc[transactions_2['amount'].apply(lambda x: isinstance(x, str()))].head())
events_2 = inject_app_event_anomalies(users, events)
wallet_balance_2 = inject_wallet_anomalies(wallet_balance)


save_to_csv(users_2, 'users.csv')
save_to_csv(transactions_2, 'transactions.csv')
save_to_csv(events_2, 'app_events.csv')
save_to_csv(wallet_balance_2, 'wallet_balances.csv')