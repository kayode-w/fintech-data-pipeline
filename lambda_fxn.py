from datetime import datetime
from pipeline import table_extraction, transform_app_events, transform_users, transform_transactions, transform_wallets
from loader import load_sql, engine



def lambda_handler(event, context):
    try:
        start_time = datetime.now()

        # Extract the data from the CSV files and load it into pandas DataFrames
        print('Extraction process in progress...\n')
        users_df = table_extraction('users')
        transactions_df = table_extraction('transactions')
        events_df = table_extraction('app_events')
        wallet_balance_df = table_extraction('wallet_balances')

        # Transformation
        print('Extraction successfully completed, commencing transformation process...\n')
        users_df = transform_users(users_df)
        transactions_df = transform_transactions(transactions_df, users_df )
        wallets_df = transform_wallets(wallet_balance_df, users_df)
        app_events_df = transform_app_events(events_df, users_df)


        print('Transformation successfully completed, commencing dataload...\n')
        D_TABLES = {
            'users':  users_df,
            'transactions': transactions_df,
            'events': app_events_df,
            'wallet_balance': wallets_df
        }
        
        # Loading
        for table_name, df in D_TABLES.items():
            load_sql(df, table_name, engine)

        end_time = datetime.now()
        duration = end_time - start_time
        print('Load successfully completed.\n')

        print(f'ETL completed in {duration.seconds // 60}:{duration.seconds % 60}.')
        return {'status': 'success', 'duration': str(duration)}

    except Exception as e:
        return {'status': 'failed', 'error': str(e)}
