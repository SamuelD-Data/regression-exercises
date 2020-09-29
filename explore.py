import seaborn as sns
import numpy as np
from wrangle import wrangle_telco
import matplotlib.pyplot as plt

# function that creates pairplot using data from provided source

def plot_variable_pairs(df):
    """
    creates pairplots of each combination of variables from a provided data source
    """
    return sns.pairplot(df, kind = 'reg')

# function adds tenure years column which holds the amount of years a customer has been with telco (rounded)
def months_to_years(df):
    """
    adds tenure years column which holds the amount of years a customer has been with telco (rounded)
    """
    df['tenure_years'] = round(df['tenure'] / 12)
    return df

# function creates 3 subplots, violin, box and swarm
def plot_categorical_and_continuous(df, cat, con):
    """
    creates 3 subplots, violin, box and swarm using data supplied along with declared categorical and continuous variables
    """
    plt.rc('figure', figsize = (19,10))
    plt.subplot(221)
    swarmplot = sns.swarmplot(data = df, x = cat, y = con)
    plt.subplot(222)
    violinplot = sns.violinplot(data = df, x = cat, y = con)
    plt.subplot(223)
    boxplot = sns.boxplot(data = df, x = cat, y = con)