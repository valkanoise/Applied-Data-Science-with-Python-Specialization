
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# Lets import .csv files:
# One includes mean temp from 1901-2021
# The other precipitations from 1901-2021
# https://climateknowledgeportal.worldbank.org/download-data

temp_df = pd.read_csv('mean_temp_tas_timeseries_monthly_cru_1901-2021_DEU.csv', skiprows=2)
rain_df = pd.read_csv('precipitations_timeseries_monthly_cru_1901-2021_DEU.csv', skiprows=2)


temp_df.rename(columns={"Unnamed: 0": "year"},inplace=True)
rain_df.rename(columns={"Unnamed: 0": "year"},inplace=True)

# It is proposed that from the 1970's the weather has been changing.
# https://www.nature.com/articles/s41598-021-90854-8
# Lets see what happens in Germany in relationship with temperatures and rainfall

# Rainfall information
# Period 1901-1969
old_rain_means = rain_df[rain_df['year']<=1969].mean()
old_rain_means.drop(['year'], inplace=True)
# Period 1970-2021
new_rain_means = rain_df[rain_df['year']>=1970].mean()
new_rain_means.drop(['year'], inplace=True)


# Temperature information
old_temp_means = temp_df[temp_df['year']<=1969].mean()
old_temp_means.drop(['year'], inplace=True)
# Period 1970-2021
new_temp_means = temp_df[temp_df['year']>=1970].mean()
new_temp_means.drop(['year'], inplace=True)


#%% Lets create a graph with two Y axis

# Lets set labels and amount of x points to simplyfy xticks
labels = list(old_rain_means.index)
x = np.arange(len(labels)) 

fig,ax = plt.subplots()

# First plot: Line plot
x = np.linspace(0,12,12)
ax.bar(x, old_rain_means, color= 'cornflowerblue', alpha= 0.7, width=0.4, label='Rain. 1901-1969')
ax.bar(x+0.4, new_rain_means, color='blue', alpha=0.7, width=0.4, label='Rain. 1969-2021')


# Second plot: Bar plot with second Y axis
ax2=ax.twinx()
ax2.plot(x, old_temp_means,'tomato', label='Temp. 1901-1969')
ax2.plot(x, new_temp_means, 'red', label='Temp. 1969-2021')

# Lets set limits, titles, labels and legends
ax.set_title('Monthly mean rain and temperature in Germany\n before and after 1970', fontsize=14)
ax.set_ylabel("Temperature (ºC)", fontsize=10)
ax.set_xlabel('Months', fontsize=14)
ax2.set_ylabel("Precipitation (mm)",fontsize=10)
ax.set_ylim([0, 150])

# Lets set xticks and their labels
ax.set_xticks(x)
ax.set_xticklabels(labels)


# To get all the labels together in one legend
# ask matplotlib for the plotted objects and their labels
lines, labels = ax.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='center left', bbox_to_anchor=(1.15, 0.5))
