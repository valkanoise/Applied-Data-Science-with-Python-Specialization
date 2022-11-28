import pandas as pd
import numpy as np

Energy = pd.read_excel("assets/Energy Indicators.xls", 
                       header= None,
                       na_values = '...',
                       skiprows=18, skipfooter=38,
                       names= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], 
                       usecols= "C:F")
Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
Energy['Country'] = Energy['Country'].str.extract("(\D+)")
Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","", regex=True)
Energy['Country'] = Energy['Country'].str.strip()
Energy['Country'].replace(to_replace= {"Republic of Korea": "South Korea",
                          "United States of America": "United States",
                          "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                          "China, Hong Kong Special Administrative Region": "Hong Kong"},
                          inplace=True)

GDP = pd.read_csv('assets/world_bank.csv', skiprows = 4)
GDP['Country Name'].replace(to_replace= {"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}, inplace=True)
GDP = GDP.rename(columns= {'Country Name':'Country'})

ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

#Merge de las 3 dataframes
columnas_GDP = ['Country','2006', '2007', '2008', '2009', '2010', '2011', 
                '2012', '2013','2014', '2015']
interseccion_dataframes = (pd.merge(GDP[columnas_GDP], Energy, how= 'inner', left_on= 'Country', right_on= 'Country')
                           .merge(ScimEn, how= 'inner', left_on= 'Country', right_on= 'Country'))
interseccion_dataframes = interseccion_dataframes[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

#%%
#### two #####
# Hay que hacer outter merge - inner merge de los 3 dfs
outter_dataframes = (pd.merge(GDP[columnas_GDP], Energy, how= 'outer', left_on= 'Country', right_on= 'Country')
                           .merge(ScimEn, how= 'outer', left_on= 'Country', right_on= 'Country'))

lost_entries = len(outter_dataframes) - len(interseccion_dataframes)

#%% Respuesta
 
def answer_two():
    import pandas as pd
    import numpy as np

    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                           header= None,
                           na_values = '...',
                           skiprows=18, skipfooter=38,
                           names= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], 
                           usecols= "C:F")
    Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
    Energy['Country'] = Energy['Country'].str.extract("(\D+)")
    Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","", regex=True)
    Energy['Country'] = Energy['Country'].str.strip()
    Energy['Country'].replace(to_replace= {"Republic of Korea": "South Korea",
                              "United States of America": "United States",
                              "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                              "China, Hong Kong Special Administrative Region": "Hong Kong"},
                              inplace=True)

    GDP = pd.read_csv('assets/world_bank.csv', skiprows = 4)
    GDP['Country Name'].replace(to_replace= {"Korea, Rep.": "South Korea", "Iran, Islamic Rep.": "Iran", "Hong Kong SAR, China": "Hong Kong"}, inplace=True)
    GDP = GDP.rename(columns= {'Country Name':'Country'})

    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    #Merge de las 3 dataframes
    columnas_GDP = ['Country','2006', '2007', '2008', '2009', '2010', '2011', 
                    '2012', '2013','2014', '2015']
    interseccion_dataframes = (pd.merge(GDP[columnas_GDP], Energy, how= 'inner', left_on= 'Country', right_on= 'Country')
                               .merge(ScimEn, how= 'inner', left_on= 'Country', right_on= 'Country'))
    interseccion_dataframes = interseccion_dataframes[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]

    #### two #####
    # Hay que hacer outter merge - inner merge de los 3 dfs
    outter_dataframes = (pd.merge(GDP[columnas_GDP], Energy, how= 'outer', left_on= 'Country', right_on= 'Country')
                               .merge(ScimEn, how= 'outer', left_on= 'Country', right_on= 'Country'))

    lost_entries = len(outter_dataframes) - len(interseccion_dataframes)

    return lost_entries
    
print(f'The number of lost entries is: {answer_two()}')
    
    