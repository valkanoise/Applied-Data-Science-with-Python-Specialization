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
# con \D
Energy['Country'] = Energy['Country'].str.extract("(\D+)")


# Saco paréntesis del final de los países mediante función
def limpiar_parentesis(item):
    if ' (' in item:
        return item[:item.find(' (')]
    else:
        return item

Energy['Country'] = Energy['Country'].apply(limpiar_parentesis)


#%%
# Cambiar nombres de algunos paises
Energy['Country'].replace(to_replace= {"Republic of Korea": "South Korea",
                          "United States of America": "United States",
                          "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                          "China, Hong Kong Special Administrative Region": "Hong Kong"},
                          inplace=True)


#%% Abrir segundo data frame a partir de un .csv

GDP = pd.read_csv('assets/world_bank.csv',
                  skiprows=4)



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


interseccion_dataframes = (pd.merge(Energy, GDP, how= 'inner', on= 'Country')
                           .merge(ScimEn, how= 'inner', on='Country'))
# Ordeno por Rank
interseccion_dataframes.sort_values(by=['Rank'], ascending=True, inplace= True)