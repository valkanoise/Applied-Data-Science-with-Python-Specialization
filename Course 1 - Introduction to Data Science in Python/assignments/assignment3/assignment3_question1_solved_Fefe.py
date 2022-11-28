import pandas as pd
import numpy as np


#%%
# Abrir el excel, descartar filas y columnas, renombrar columnas,
# reemplazar el '...' por Nan y generar dataframe llamado "Energy"

Energy = pd.read_excel("assets/Energy Indicators.xls", 
                       header= None,
                       na_values = '...',
                       skiprows=18, skipfooter=38,
                       names= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], 
                       usecols= "C:F")


#%% Convertir la columna 'Energy Supply' a gigajoules 
Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000

#%%
# Sacar números y paréntesis al final de los nombres de los países

# Primero saco nros que están detras de algunos países, 
# para ello uso extract(regex) para buscar elementos que no sean digitos 
# con \D. Se debe generar un (grupo) a extraer
Energy['Country'] = Energy['Country'].str.extract("(\D+)")
# Saco los paréntesis y su contenido por nada ("")
Energy['Country'] = Energy['Country'].str.replace(r" \(.*\)","", regex=True)
# Por si acaso le aplico un stri() para sacar espacios y demases
Energy['Country'] = Energy['Country'].str.strip()
# Cambiar nombres de algunos paises
Energy['Country'].replace(to_replace= {"Republic of Korea": "South Korea",
                          "United States of America": "United States",
                          "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                          "China, Hong Kong Special Administrative Region": "Hong Kong"},
                          inplace=True)


#%% Abrir segundo data frame a partir de un .csv

GDP = pd.read_csv('assets/world_bank.csv', skiprows = 4)



# Cambiar nombres de algunos paises
GDP['Country Name'].replace(to_replace= {"Korea, Rep.": "South Korea", 
                                         "Iran, Islamic Rep.": "Iran",
                                         "Hong Kong SAR, China": "Hong Kong"},
                            inplace=True)

# Le cambio el nombre a la columna "Country Name" a "Country"
# para que todas las df tengan misma columna
GDP = GDP.rename(columns= {'Country Name':'Country'})

#%% Abrir tercer dataframe a partir de un .xlxs
ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

#%% Merge de las 3 dataframes

# Selecciono columnas de GDP: 'Country' y 10 años
columnas_GDP = ['Country','2006', '2007', '2008', '2009', '2010', '2011', 
                '2012', '2013','2014', '2015']

# Hago la intersección de las 3 dataframes en base a la columna "Country"
# Notese que primero hago merge de ScimEn+Enegy y a esa df le sumo GDP
# únicamente con columnas de interés de esa df
interseccion_dataframes = (pd.merge(GDP[columnas_GDP], Energy, how= 'inner', left_on= 'Country', right_on= 'Country')
                           .merge(ScimEn, how= 'inner', left_on= 'Country', right_on= 'Country'))

# Ordeno las columnas según el enunciado
interseccion_dataframes = interseccion_dataframes[['Country','Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations', 'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita', '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']]


#%%
#### one #####

# Defino como index la columna 'Country'.
interseccion_dataframes = interseccion_dataframes.set_index('Country')
# Selecciono los primeros 15 países según la columna 'Rank'
Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]
# Ordeno de manera ascendente según su valor de 'Rank'
Top15 = Top15.sort_values('Rank', axis=0, ascending=True, inplace=False)


#%% Respuesta 

def answer_one():
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

    #### one #####
    interseccion_dataframes = interseccion_dataframes.set_index('Country')
    Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]
    Top15 = Top15.sort_values('Rank', axis=0, ascending=True, inplace=False)

    return Top15