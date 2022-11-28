# -*- coding: utf-8 -*-
"""
Created on Mon Aug 22 12:37:53 2022

@author: FEFe
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math


# Generates a dataframe with 4 series (4 years9
# Each one has 3650 data points randomly generated with a normal distribution
np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])


#%% Calculate Confidence interval of 95% for each year
# https://www.omnicalculator.com/statistics/confidence-interval#95percent-confidence-interval-formula

# Calculates the mean,std and CI for each row/year
# Creates Series with 4 elements and the year as index
means = df.T.describe().loc['mean']
stds = df.T.describe().loc['std']
CI_95 = 1.96 * (stds / math.sqrt(len(df.columns)))



#%% Simple graph with error bar showing CI_95

# fig, ax = plt.subplots()
# x = [str(x) for x in df.index]
# y = means
# ax.bar(list(x), y, yerr = CI_95 )
# ax.axhline(y=42000, zorder=10, linestyle="--", color="red")
# plt.show()


#%% Easiest option: 

# Lets define a fixed value
fixed_value = 42000

# Function to define the color of each bar
# It compares de fixed value with the CI of each bar
def color_barra(mean, confidence_interval, threshold):
    ''' Function that defines the color of each bar. 
    - If the fixed_value is bigger than the CI it turns the bar blue.
    - If the fixed_value is in between the CI it turns the bar white.
    - If the fixed_value is smaller than the CI it turns the bar red.
    
    Each call of the funcion requires three arguments: mean, CI and threshold
    '''
    
    ci_superior = mean + confidence_interval
    ci_inferior = mean - confidence_interval
    
    if ci_superior < fixed_value:
        return 'blue'
    if ci_inferior <= fixed_value and ci_superior >= fixed_value:
        return 'white'
    if ci_inferior >= fixed_value:
        return 'red'
    

# Lets graph
fig, ax = plt.subplots()
x = [str(x) for x in df.index]
y = means
lista_colores = [color_barra(means.iloc[i], CI_95.iloc[i], fixed_value) for i in range(len(df.index))]  

ax.bar(list(x), y, yerr = CI_95, color=lista_colores, edgecolor='black')
ax.axhline(y=fixed_value, zorder=10, linestyle="--", color="red")

ax.set_title('Easiest option', fontsize=18)
plt.xlabel('Year')
plt.ylabel('Mean and Confidence interval')
plt.show()