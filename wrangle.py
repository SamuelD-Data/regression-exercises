import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import acquire
import env
import os
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings("ignore")

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


# Using function from exercise guide, also adding to wrangle file
from sklearn.preprocessing import MinMaxScaler

# creating function with 3 parameters, one for each dataset (train, validate, test)
def minmax_scaler(train, validate, test):
    '''
    Function takes in train, validate and test data frames then returns them after scaling them from 0 to 1 
    '''
    # creating minmax scaler object
    scaler = MinMaxScaler()
    
    # fitting scaler to each column in the train data set
    # transforming data in train data set
    train[['monthly_charges', 'tenure' ,'total_charges']] = scaler.fit_transform(train[['monthly_charges', 'tenure', 'total_charges']])
    # transforming data in validate and test data sets while scaler fitted to train values
    validate[['monthly_charges', 'tenure', 'total_charges']] = scaler.transform(validate[['monthly_charges', 'tenure', 'total_charges']])
    test[['monthly_charges', 'tenure', 'total_charges']] = scaler.transform(test[['monthly_charges', 'tenure', 'total_charges']])
    # returning scaled data sets
    return train, validate, test

def wrangle_grades():
    grades = pd.read_csv("student_grades.csv")
    grades.drop(columns="student_id", inplace=True)
    grades.replace(r"^\s*$", np.nan, regex=True, inplace=True)
    df = grades.dropna().astype("int")
    return df

# creating function to split data into train, validate and test DFs
def train_valid_test(df):
    train_validate, test = train_test_split(df, test_size = .2, random_state = 123)
    train, validate = train_test_split(train_validate, test_size = .3, random_state = 123)
    return train, validate, test