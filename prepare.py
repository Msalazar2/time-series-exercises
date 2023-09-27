import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from env import get_connection
from IPython.display import HTML, display
from datetime import timedelta, datetime

def store_data():
    
    filename = 'stores.csv'
    
    if os.path.isfile(filename):
        
        print('Found Data')
        
        return pd.read_csv(filename)
    
    else:
    
        print('Retrieving Data')

        query = '''
                SELECT sale_date, sale_amount,
                item_brand, item_name, item_price,
                store_address, store_zipcode,
                store_city, store_state 
                FROM sales
                LEFT JOIN items USING (item_id)
                LEFT JOIN stores USING(store_id)
                '''
        url = get_connection('tsa_item_demand')

        df = pd.read_sql(query, url)

        df.to_csv(filename, index = 0)

        return df
    
def prep_store():
    
    df = store_data()

    df.sale_date = pd.to_datetime(df.sale_date)

    df = df.set_index('sale_date').sort_index()

    df['month'] = df.index.month_name()

    df['day'] = df.index.day_name()

    df['sales_total'] = df.sale_amount * df.item_price
    
    return df

def date_index(df):
    
    df.columns = df.columns.str.lower()
    df.columns = df.columns.str.replace('+', '_')
    
    for col in df.columns:

        try:
            # Attempt to convert each value to datetime
            df[col] = pd.to_datetime(df[col])

            df = df.set_index(col).sort_index()

            df['month'] = df.index.month_name()

            df['day'] = df.index.day_name()
            
            df['year'] = df.index.year

            # Check for consistent date format (adjust the format as needed)
            return df

        except ValueError:

            return False
        
def plt_dist(df, feats, loop = False):
    
    if loop:
        
        for col in df.columns:

            plt.hist(df[col], bins = 50)

            plt.xlabel(f'{col.replace("_", " ").title()}')

            plt.ylabel('Count')

            plt.title(f'Distribution of {col.replace("_", " ").title()}')

            plt.show()
            
    else: 
        
        plt.hist(df[feats], bins = 50)

        plt.xlabel(f'{feats.replace("_", " ").title()}')

        plt.ylabel('Count')

        plt.title(f'Distribution of {feats.replace("_", " ").title()}')

        plt.show()
        
def summarize(df):
    
    text = 'Shape & Date Range:'
    bold_text = f'<b>{text}</b>'
    display(HTML(bold_text))
    print('Shape', df.shape)
    print('Date Range', df.index.min(), 'to', df.index.max())
    print('')
    print('_________________________________________________')
    print('')
    
    text = 'Time Series Gaps:'
    bold_text = f'<b>{text}</b>'
    display(HTML(bold_text))
    print('Number of rows:', df.index.nunique())
    n_days = df.index.max() - df.index.min() + pd.Timedelta('1d')
    print(f"Number of days between first and last day:", n_days)
    print('')
    print('_________________________________________________')
    print('')
    
    text = 'Info:'
    bold_text = f'<b>{text}</b>'
    display(HTML(bold_text))
    df.info()
    print('')
    print('_________________________________________________')
    print('')
    
    text = 'Null Values:'
    bold_text = f'<b>{text}</b>'
    display(HTML(bold_text))
    print('')
    print(df.isna().sum())
    print('')
    print('_________________________________________________')
    print('')
    
    for col in df.columns.values:
        text = f'Value Count for {col}:'
        bold_text = f'<b>{text}</b>'
        display(HTML(bold_text))

        print('')
        vc = df[col].value_counts()
        print(vc)
        print('')
        print('_________________________________________________')
        print('')