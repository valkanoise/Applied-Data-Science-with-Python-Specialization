import pandas as pd
import numpy as np
import assignment3_question1_solved_Fefe

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

    
Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)

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

#%% Ejercicio 10

# Busco la mediana de '% Renewable' para los Top15 países
# Para eso uso la función answer_one() que devuelve df con Top15 y calculo median()
Top15 = assignment3_question1_solved_Fefe.answer_one()
median_Top15 = Top15['% Renewable'].median(skipna=True)

#%% Genero función para que vaya fila(serie) por serie comparando la mediana y
# agregando 1 o 0 si es mayor o menor
def above_median(row):
    if row['% Renewable']>= median_Top15:
        row['Above Median Top 15'] = 1
    else:
        row['Above Median Top 15'] = 0
    return row

# Aplico la función y agrega una columna más "Above Median Top 15"
interseccion_dataframes = interseccion_dataframes.apply(above_median, axis="columns")

# Ordeno la dataframe por rank
interseccion_dataframes.sort_values(by=['Rank'], ascending=True, inplace= True)

# Creo serie que devuelve Países ordenados por rank y sus valores de 
# Above Median Top 15"
HighRenew = pd.Series(list(interseccion_dataframes['Above Median Top 15']), index= interseccion_dataframes['Country'])


#%% Respuesta

def answer_ten():
    import pandas as pd
    import numpy as np
    #import answer_one()
    import assignment3_question1_solved_Fefe
    
    # Abro y limpio primera df
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                           header= None,
                           na_values = '...',
                           skiprows=18, skipfooter=38,
                           names= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], 
                           usecols= "C:F")

    Energy['Energy Supply'] = Energy['Energy Supply'].apply(lambda x: x*1000000)
    Energy['Country'] = Energy['Country'].str.extract("(\D+)")
    # Saco paréntesis del final de los países mediante función
    def limpiar_parentesis(item):
        if ' (' in item:
            return item[:item.find(' (')]
        else:
            return item

    Energy['Country'] = Energy['Country'].apply(limpiar_parentesis)
    Energy['Country'].replace(to_replace= {"Republic of Korea": "South Korea",
                              "United States of America": "United States",
                              "United Kingdom of Great Britain and Northern Ireland": "United Kingdom",
                              "China, Hong Kong Special Administrative Region": "Hong Kong"},
                              inplace=True)
    
    # Abro y limpio segunda df
    GDP = pd.read_csv('assets/world_bank.csv',
                      skiprows=4)
    # Cambiar nombres de algunos paises
    GDP['Country Name'].replace(to_replace= {"Korea, Rep.": "South Korea", 
                                             "Iran, Islamic Rep.": "Iran",
                                             "Hong Kong SAR, China": "Hong Kong"},
                                inplace=True)

    GDP = GDP.rename(columns= {'Country Name':'Country'})

    #Abrir tercer dataframe a partir de un .xlxs
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    # Inner merge de los 3 df
    interseccion_dataframes = (pd.merge(Energy, GDP, how= 'inner', on= 'Country')
                               .merge(ScimEn, how= 'inner', on='Country'))
    
    # Calculo la mediana de % Renewable de los top15 países
    Top15 = assignment3_question1_solved_Fefe.answer_one()
    #Top15 = answer_one()
    median_Top15 = np.median(Top15['% Renewable'])
    
    #Función para que vaya fila(serie) por serie comparando la mediana y
    # agregando 1 o 0 si es mayor o menor
    def above_median(row):
        if row['% Renewable']>= median_Top15:
            row['Above Median Top 15'] = 1
        else:
            row['Above Median Top 15'] = 0
        return row

    # Aplico la función al df_merge y agrega una columna más "Above Median Top 15"
    interseccion_dataframes = interseccion_dataframes.apply(above_median, axis="columns")

    # Ordeno la dataframe por rank
    interseccion_dataframes.sort_values(by=['Rank'], ascending=True, inplace= True)

    # Creo serie que devuelve Países ordenados por rank y sus valores de 
    # Above Median Top 15"
    HighRenew = pd.Series(list(interseccion_dataframes['Above Median Top 15']), index= interseccion_dataframes['Country'])

    return HighRenew
    