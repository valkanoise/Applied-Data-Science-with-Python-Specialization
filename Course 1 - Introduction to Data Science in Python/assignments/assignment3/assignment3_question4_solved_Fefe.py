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
#### four ##### trabajando con las intersección de las 3 dfs
    
# Defino como index la columna 'Country'.
interseccion_dataframes = interseccion_dataframes.set_index('Country')

# Selecciono los primeros 15 países según la columna 'Rank'
Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]

# Calculo la media de los últimos 10 años de GDP
years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013','2014', '2015']
Top15['avgGDP'] = Top15[years].apply(lambda x: np.nanmean(x), axis=1)

# Ordeno de manera ascendente según su valor de 'Rank'
Top15 = Top15.sort_values('avgGDP', axis=0, ascending=False, inplace=False)

# Calculo la diferencian entre el años 2015 y 2016 (10 años)
diferencia = Top15.iloc[5]['2015'] - Top15.iloc[5]['2006']


#%% Respuesta 
def answer_four():
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

    #### four ##### 
        
    interseccion_dataframes = interseccion_dataframes.set_index('Country')
    Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]
    years = ['2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013','2014', '2015']
    Top15['avgGDP'] = Top15[years].apply(lambda x: np.nanmean(x), axis=1)
    Top15 = Top15.sort_values('avgGDP', axis=0, ascending=False, inplace=False)
    diferencia = Top15.iloc[5]['2015'] - Top15.iloc[5]['2006']
    
    return diferencia

print(f'The GDP changed over the 10 year span for the country with the 6th largest average GDP in: {answer_four():,.2f}')