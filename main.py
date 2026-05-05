from dealer import generate_users, generate_transactions, app_events, generate_wallet_balance, save_to_csv





users = generate_users()
transactions = generate_transactions(users)
events = app_events(users)
wallet_balance = generate_wallet_balance(users)