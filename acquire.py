# importing pandas
import pandas as pd
# importing env for access to user, host and password
import env
# importing os
import os

# creating function that returns a path that can be used to connect to SQL database
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'
    
###### ACQUIRE MALL CUSTOMERS DATA ############

def new_mall_data():
    '''This function reads the mall customer data from the Codeup db into a df, writes it to a csv file and returns the df'''
    sql_query = 'SELECT * FROM customers'
    df = pd.read_sql(sql_query, get_connection('mall_customers'))
    df.to_csv('mall_customers_df.csv')
    return df

def get_mall_data(cached=False):
    '''This function reads in mall customer data from Codeup database if cached == False or if cached == True reads in mall customer df from a csv file, returns df'''

    if cached or os.path.isfile('mall_customers_df.csv') == False:
        df = new_mall_data()
    else:
        df = pd.read_csv('mall_customers_df.csv', index_col = 0)
    return df

# creating function that returns a path that can be used to connect to SQL database
def get_connection(db, user=env.user, host=env.host, password=env.password):
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'

# creating function that creates a variable call filename that holds the name of a current, or soon to be created file
def get_telco_data():
    filename = "telco.csv"
    # if a file is found with a name that matches filename (titanic.csv), the function will return the data as a dataframe
    if os.path.isfile(filename):
        return pd.read_csv(filename)
    # if no file with the specified name can be found the else statement is ran
    else:
        # creating sql query and using get_connection function to connect to titanic database and create
        # dataframe using data in passengers table
        df = pd.read_sql('SELECT * FROM customers', get_connection('telco_churn'))

        # writing dataframe to csv file
        df.to_csv(filename, index = False)

        # return the dataframe
        return df 