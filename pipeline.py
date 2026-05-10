import os
import pandas as pd

from dealer import DATA_TABLES, CURRENCY_MAP, CURRENCY_RATES


def table_extraction(table_name: str) -> pd.DataFrame:
    """
    Extracts data from a CSV file and returns it as a pandas DataFrame.
    
    Args:
        table_name (str): The name of the table to be extracted.
    Returns:
        pd.DataFrame: The extracted data as a pandas DataFrame.
    """
    file_path = os.path.join(DATA_TABLES, f'{table_name}.csv')
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'The {table_name} file does not exist in this location: {DATA_TABLES}')
    
    try:
        df = pd.read_csv(file_path)

        return df
    except Exception as e:
        raise Exception(f'An error occurred while reading the {table_name} file: {str(e)}')
    

def name_proper_case(df: pd.DataFrame, column_name: str | list) -> pd.DataFrame:
    """
    Converts the values in a specified column of a DataFrame to proper case.
    
    Args:
        df (pd.DataFrame): The input DataFrame.
        column_name (str): The name of the column to be converted to proper case.
    Returns:
        pd.DataFrame: The DataFrame with the specified column converted to proper case.
    """
    if isinstance(column_name, str):
        if column_name in df.columns: # check if the column exists in the DataFrame
            try:
                df[column_name] = df[column_name].apply(lambda x: x.title() if isinstance(x, str) else x)
            except Exception as e:
                raise Exception(f'An error occurred while converting the {column_name} column to proper case: {str(e)}') # eg if there's a problem with parsing
        else: # if the column does not exist in the DataFrame, raise an error
            raise ValueError(f'The specified column "{column_name}" does not exist in the DataFrame.') # eg countryy
        return df
    
    elif isinstance(column_name, list):
        for col in column_name: # loop through the list of column names 
            if col in df.columns: # If the column exists in the DataFrame, convert it to proper case
                try:
                    df[col] = df[col].apply(lambda x: x.title() if isinstance(x, str) else x)
                except Exception as e:
                    raise Exception(f'An error occurred while converting the {col} column to proper case: {str(e)}')
            else:
                raise ValueError(f'The specified column "{col}" does not exist in the DataFrame.')
        return df
      
    else:
        raise ValueError('The column_name parameter must be a string or a list of strings.')
           

 # we need this bc as the table grows, we would probably need to apply different transformation functions to diff columns.
def transform_users(df: pd.DataFrame) -> pd.DataFrame:
     try:
         df = name_proper_case(df, ['first_name', 'last_name', 'country'])
         return df
     except Exception as e:
            raise Exception(f'An error occurred while transforming the users DataFrame: {str(e)}')
     

# Transaction transformation

def unknown_sts(txn_df: pd.DataFrame) -> pd.DataFrame:
    txn_df.loc[txn_df['transaction_status'].isnull(), 'transaction_status'] ='status unknown'
    # or txn_df['transaction_status'] = txn_df['transaction_status'].fillna('status unknown)
    return txn_df


def currency_conversion(df: pd.DataFrame, rate: str, local_amt: str) -> pd.DataFrame:
    if rate  not in df.columns:
        raise ValueError(f'Column {rate} does not exist in the dataframe.')
    
    if local_amt not in df.columns:
        raise ValueError(f'Column {local_amt} does not exist in the dataframe.')

    try:
        df[rate] = pd.to_numeric(df[rate], errors = 'coerce') # use this to 
        df[local_amt] = pd.to_numeric(df[local_amt], errors = 'coerce')
        df['converted_amount'] = df[local_amt] * df[rate]
    except Exception as e:
        raise Exception(f'An error occurred while transforming the users DataFrame: {str(e)}')
    return df


def currency_lookup(txn_df: pd.DataFrame, users_df: pd.DataFrame):
    df = pd.merge(txn_df, users_df[['user_id', 'country']], left_on='sender_id', right_on='user_id', how='left')
    df = df.drop(columns= 'user_id') # either this to drop a column or next style below

    # lookup:  where the currency rate is null, use the country field as a key to look up matching values on the currency_map dict
    df.loc[df['currency'].isnull(), 'currency'] = df.loc[df['currency'].isnull(), 'country'].map(CURRENCY_MAP)
    df.loc[df['currency_rate'].isnull(), 'currency_rate'] = df.loc[df['currency_rate'].isnull(), 'currency'].map(CURRENCY_RATES)

    df.drop(columns= 'country', inplace = True)
    return df


def transform_transactions(txn_df: pd.DataFrame, users_df: pd.DataFrame) -> pd.DataFrame:
    try:
        df = unknown_sts(txn_df)
        df = currency_lookup(df, users_df)
        df = currency_conversion(df, 'currency_rate', 'amount')
        return df
    
    except Exception as e:
        raise Exception(f'An error occurred while transforming the transactions DataFrame: {str(e)}')





        


