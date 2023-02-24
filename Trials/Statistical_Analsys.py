# This file is to create some statistical analysis on the data to see what transforming I should do

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
from scipy.stats import linregress

# Load the data from the CSV file
data = pd.read_csv('transformed_data.csv', encoding='ISO-8859-1')

# Create value ranges for certain columns.
def add_decimal(val, name):
    if name == 'profundidade':
        if val > 50000:
            return val / 100
        elif val < 100000 and val > 10000:
            return val / 10
        elif val < 0:
            max(val, 0)
        else:
            return val
    elif name == 'porosidade':
        if val > 100:
            return val / 100
        return max(min(val, 1), 0)
    elif name == 'densidade':
        if val > 200:
            return val / 100
        else:
            return val
    return val

def check_boundaries(val, name):
    # Define upper and lower bounds for each column
    bounds = {
        'profundidade': {'lower': 0, 'upper': 50000},
        'porosidade': {'lower': 0, 'upper': 100},
        'densidade': {'lower': 0, 'upper': 200},
        'permeabilidade_long': {'lower': 0, 'upper': 10000},
        'pressao_conf': {'lower': 0, 'upper': 10000},
        'pressao': {'lower': 0, 'upper': 500},
        'saturacao': {'lower': 0, 'upper': 100},
        'coeficiente_cimentacao': {'lower': 0, 'upper': 100},
        'expoente_saturacao': {'lower': 0, 'upper': 10},
        'fluxo_fracionario': {'lower': 0, 'upper': 100},
        'permeabilidade_fluido_deslocado': {'lower': 0, 'upper': 10000},
        'kg_abs': {'lower': 0, 'upper': 1500},
        'saturacao_agua': {'lower': 0, 'upper': 100}
    }
    # Check if value is out of bounds and correct it if necessary
    if val < bounds[name]['lower']:
        print(f"The value has changed to {val} because it is less than 0")
        return abs(val)
    elif val > bounds[name]['upper']:
        new_bound = bounds[name]['upper']
        old_val = val
        val = add_decimal(val, name)
        print(f"The value has changed to {val} from {old_val} because it is greater than {new_bound}")
        return val
    else:
        return val

# Select the columns for the box plot
columns = ['profundidade', 'porosidade', 'densidade', 'permeabilidade_long', 'pressao_conf', 'pressao', 'saturacao', 'coeficiente_cimentacao', 'expoente_saturacao', 'fluxo_fracionario', 'permeabilidade_fluido_deslocado', 'kg_abs', 'saturacao_agua']

# Convert the columns to float, excluding non-numeric values
data[columns] = data[columns].apply(pd.to_numeric, errors='coerce')

# Convert multiple columns
# Convert the columns to float

def find_global_anomalies(column_name):
    '''
    Returns the global anomalies that are greater than 3 standard deviations

            Parameters:
                    column_name (str): The name of the column in the datafrae

            Returns:
                    anomalies (series): A pandas series with the anomalis indexed
    '''
    # Calculate the mean and standard deviation of your data
    mean = data[column_name].mean()
    std = data[column_name].std()

    # Create a boolean mask to select the values that are more than three standard deviations away from the mean
    mask = (data[column_name] > mean + 3*std) | (data[column_name] < mean - 3*std)

    # Use the boolean mask to select the rows with anomalous values
    anomalies = data[mask]

def find_local_anomalies(column_name):
    '''
    Returns the local anomalies that are greater than 3 standard deviations for each poco in the given column

            Parameters:
                    column_name (str): The name of the column in the dataframe

            Returns:
                    anomalies (dataframe): A pandas dataframe with the anomalous values and their respective pocos indexed
    '''
    # Group the data by "poco" and calculate the mean and standard deviation for each group
    grouped_data = data.groupby('poco')[column_name].agg(['mean', 'std']).reset_index()

    # Merge the grouped data back into the original data frame
    data_with_means = data.merge(grouped_data, on='poco', suffixes=('', '_group'))

    # Create a boolean mask to select the values that are more than three standard deviations away from the group means
    mask = (data_with_means[column_name] > data_with_means['mean'] + 
        3*data_with_means['std']) | (data_with_means[column_name] < data_with_means['mean'] - 3*data_with_means['std'])

    # Use the boolean mask to select the rows with anomalous values and return a dataframe with the anomalous values and their respective pocos indexed
    anomalies = data_with_means[mask][['poco', column_name]].set_index('poco')
    return anomalies


# Group data by 'poco'
# grouped_data = data.groupby('poco')

# Define a function to apply the regression average
def apply_regression_average(group):
    # Calculate the regression average of 'profundidade'
    #print(group)
    slope, intercept, r_value, p_value, std_err = linregress(group['profundidade'], group.index)
    regression_average = (0 - intercept) / slope
    
    # Replace 0 with the regression average
    group.loc[group['profundidade'] == 0, 'profundidade'] = regression_average
    return group

# Apply the regression average to the data
#data_with_regression_average = grouped_data.apply(apply_regression_average)

# Apply the regression average to the data

#print(find_local_anomalies('profundidade'))

for df_c in columns:
    data[df_c] = data[df_c].apply(check_boundaries, name = df_c)
#data_with_regression_average = data[['profundidade', 'poco']].apply(apply_regression_average)


data[columns] = data[columns].astype(float)

# Iterate through each column (except "poco") and create a boxplot
for name in columns:
    if name != 'poco':
        mask = data[name].notna()
        filtered_df = data.loc[mask]
        filtered_df.boxplot(column=name, by='poco')

# Show the plot
plt.show()