import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('data/C2A2_data/BinnedCsvs_d400/fb441.csv')



#%% Initial cleaning of the main dataframe

# I generate from 'Date' the columns 'Year' and 'Month-Day'
df['Year'] = df['Date'].apply(lambda x : x.split('-')[0])
df['Month-Day'] = df['Date'].str.extract('\d+-(\d+-\d+)')
# I take out leap days that contain '02-29'
df = df[~df['Date'].str.contains('02-29')]

# I organize the dates by 'Year' and 'Month-Day'
df = df.sort_values(['Year','Month-Day'], axis=0, ascending=True)
# I generate a columns with the name of the months
df['Month'] = pd.DatetimeIndex(df['Date']).month_name()


#%% For the period 2005-2014
# I generate 2 dataframes, grouping by Month-Date to find the MAX or MIN
# temperatures between all the stations. As a result each dataframe contains
# the highest or lowest temperature registered for every day along a 10 year
# period.

group_10years_tmax = df[(df['Element']=='TMAX') & (df['Year']<'2015')].groupby("Month-Day", sort=True).agg({'Data_Value': np.max})
# I change the name of the column to clarify during the concatenation
group_10years_tmax.rename(columns = {'Data_Value': 'TMAX_10YEARS'}, inplace = True)

group_10years_tmin = df[(df['Element']=='TMIN') & (df['Year']<'2015')].groupby("Month-Day", sort=True).agg({'Data_Value': np.min})
# I change the name of the column to clarify during the concatenation
group_10years_tmin.rename(columns = {'Data_Value': 'TMIN_10YEARS'}, inplace = True)


#%% For the year 2015
# I generate 2 dataframes grouping by Month-Date to find the MAX or MIN
# between all the stations. As a result each dataframe contains
# the highest or lowest temperature registered for every day along the year 2015

group_2015_tmax = df[(df['Element']=='TMAX') & (df['Year']=='2015')].groupby("Month-Day", sort=True).agg({'Data_Value': np.max})

group_2015_tmin = df[(df['Element']=='TMIN') & (df['Year']=='2015')].groupby("Month-Day", sort=True).agg({'Data_Value': np.min})

#%% Lets select those MAX temperatures from the year 2015 that are higher or lower
# than those from the period 2005-2014

records_max = group_2015_tmax[group_2015_tmax['Data_Value'] > group_10years_tmax['TMAX_10YEARS']]
# I change the name of the column to clarify during the concatenation

records_max.rename(columns = {'Data_Value': 'TMAX_2015'}, inplace = True)

records_min = group_2015_tmin[group_2015_tmin['Data_Value'] < group_10years_tmin['TMIN_10YEARS']]
# I change the name of the column to clarify during the concatenation

records_min.rename(columns = {'Data_Value': 'TMIN_2015'}, inplace = True)

#%% Concatenation of all the relevant temperatures:
# ['TMAX_10YEARS', 'TMIN_10YEARS', 'TMAX_2015', 'TMIN_2015']

all_data = pd.concat([group_10years_tmax, group_10years_tmin, records_max, records_min], axis=1)

all_data['Order'] = np.arange(1,366,1)

all_data

#%% Lets make the graph

# I define x axis
eje_x = all_data['Order']

plt.figure(figsize=(6, 4), dpi=100)

# I plot MAX and MIN records along the 10 year period
plt.plot(eje_x, all_data['TMAX_10YEARS'], color='r', alpha=0.4, label= 'Record high 2005-2014')
plt.plot(eje_x, all_data['TMIN_10YEARS'], color='b', alpha=0.4, label= 'Record Low 2005-2014')

# I fill the space between TMAX and TMIN
plt.fill_between(eje_x ,all_data['TMAX_10YEARS'], all_data['TMIN_10YEARS'], alpha= 0.3)

# I scatterplot the MAX and MIN temperatures from the year 2015 than are
# higher or lower than the 2005-2014 period
plt.scatter(eje_x, all_data['TMAX_2015'], color='r', s=10, label='Record high 2015')
plt.scatter(eje_x, all_data['TMIN_2015'], color='b', s=10, label='Record low 2015')

# Lets modify the xticks: their positions and labels
# I generate a list with the months names and add '1' to indicate the first day
months = df['Month'].unique()

# I generate xticks based on the position of the first day of every month ('-01')
# and assign the months as labels
dias = [x for x in all_data.index]
# From the 365 dates I choose those that end with '-01' so that I know where each month starts
index_dia = [dias.index(dia) + 1 for dia in dias if dia.endswith('-01')]
# Changes the xticks from index to Months
plt.xticks(index_dia, months)
# I rotate the labels so they can fit
plt.xticks(rotation=90)

# I set the limits of the x axis
plt.xlim(0, 365)

# I add titles and legend
plt.title('Daily record high and low temperatures for \n Ann Arbor (2005-2015)', alpha=1)
plt.xlabel('Date',alpha=0.6)
plt.ylabel('Temperature (tenths of degrees C)',alpha=0.6)
plt.legend(loc='best', frameon=False, labelspacing= 0.1, fontsize=7)

# I remove some axis to "clean" the visualization
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)


# If we want to save the graph in a file.png
# plt.subplots_adjust(bottom=0.30)
# plt.savefig('Temperatures.png')