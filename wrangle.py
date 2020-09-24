import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import acquire
import env
import os

# creating function that returns a path that can be used to connect to SQL database
def get_connection(db, user=env.user, host=env.host, password=env.password):
    '''This function returns a url that can be used to access the DS database'''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

def new_telco_data():
    '''This function reads the telco customer data from the Codeup db into a df, writes it to a csv file and returns the df'''
    sql_query = 'select customer_id, monthly_charges, tenure, total_charges from customers where contract_type_id = 3'
    df = pd.read_sql(sql_query, get_connection('telco_churn'))
    df.to_csv('telco_df.csv')
    return df

def get_telco_data(cached=False):
    '''This function reads in mall customer data from Codeup database if cached == False or if cached == True reads in mall customer df from a csv file, returns df'''
    if cached or os.path.isfile('telco_df.csv') == False:
        df = new_telco_data()
    else:
        df = pd.read_csv('telco_df.csv', index_col = 0)
    return df
    
def wrangle_telco():
    '''This function prepares the data for exploration via replacing white space values with 0s and converting total_charges to float'''
    # using get_telco_data() function to retrieve data
    tdf = get_telco_data()
    # replacing white space values with 0
    tdf['total_charges'] = tdf.total_charges.where((tdf.tenure != 0),0)
    # converting data type to float since we couldnt when there were white space values
    tdf['total_charges'] = tdf.total_charges.astype(float)
    return tdf
