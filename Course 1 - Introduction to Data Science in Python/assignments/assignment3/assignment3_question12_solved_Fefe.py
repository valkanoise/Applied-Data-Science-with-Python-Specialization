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

# Calculo la población

interseccion_dataframes['PopEst'] = interseccion_dataframes['Energy Supply'] / interseccion_dataframes['Energy Supply per Capita']

#%% Agregar a qué continente pertenece cada país:

# Forma 1: usando función pandas.Series.map()
# Map values of Series according to an input mapping or function.
# Used for substituting each value in a Series with another value, that may be derived from a function, a dict or a Series.

# Tenemos un dic con pais:continente    
ContinentDict  = {'China':'Asia', 
                  'United States':'North America', 
                  'Japan':'Asia', 
                  'United Kingdom':'Europe', 
                  'Russian Federation':'Europe', 
                  'Canada':'North America', 
                  'Germany':'Europe', 
                  'India':'Asia',
                  'France':'Europe', 
                  'South Korea':'Asia', 
                  'Italy':'Europe', 
                  'Spain':'Europe', 
                  'Iran':'Asia',
                  'Australia':'Australia', 
                  'Brazil':'South America'}

# interseccion_dataframes['Continente'] = interseccion_dataframes['Country'].map(ContinentDict)

# Forma 2
# Usando una función y es la que se me ocurrió a mi

def asignar_continente(row):
    '''Esta función toma una serie. Dentro de la serie controla si el país
    que se encuentra en la columna 'Country' está en el diccionario ContinentDict,
    si está, crea una nueva columna 'Continent' y le agrega el valor del continente
    explicitado en el dic'''
    
    if row['Country'] in ContinentDict:
        row['Continent'] = ContinentDict[row['Country']]
    else:
        row['Continent'] = np.nan
    return row

interseccion_dataframes = interseccion_dataframes.apply(asignar_continente, axis='columns')

#%% Agrupar a los países de acuerdo a su continente



# Agrupamos por continente
continentes = interseccion_dataframes.groupby('Continent')

# Creo una df con la función agg() y creo columnas con la siguiente
# información: nro de paises por continente y sum, mean, y std deviation 
# para la población estimada de cada continente(usando los países del grupo).
resumen = continentes.agg({'Continent':len, 'PopEst':(sum, np.mean, np.std)})

# Le cambio el nombre a las columnas por lo nombres que yo quiero: 
# ['size', 'sum', 'mean', 'std']
resumen.columns = ['size', 'sum', 'mean', 'std']

#%% Respuesta 

def answer_eleven():
    import pandas as pd
    import numpy as np
    # Primer df
    Energy = pd.read_excel("assets/Energy Indicators.xls", 
                           header= None,
                           na_values = '...',
                           skiprows=18, skipfooter=38,
                           names= ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable'], 
                           usecols= "C:F")
       
    Energy['Energy Supply'] = Energy['Energy Supply'] * 1000000
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

    # Abrir segundo df
    GDP = pd.read_csv('assets/world_bank.csv',
                      skiprows=4)
    GDP['Country Name'].replace(to_replace= {"Korea, Rep.": "South Korea", 
                                             "Iran, Islamic Rep.": "Iran",
                                             "Hong Kong SAR, China": "Hong Kong"},
                                inplace=True)
    GDP = GDP.rename(columns= {'Country Name':'Country'})

    # Abrir tercer df
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    #Merge de las 3 dataframes
    interseccion_dataframes = (pd.merge(Energy, GDP, how= 'inner', on= 'Country')
                               .merge(ScimEn, how= 'inner', on='Country'))
    # Ordeno por Rank
    interseccion_dataframes.sort_values(by=['Rank'], ascending=True, inplace= True)

    # Calculo la población
    interseccion_dataframes['PopEst'] = interseccion_dataframes['Energy Supply'] / interseccion_dataframes['Energy Supply per Capita']

    # Agregar a qué continente pertenece cada país:
    ContinentDict  = {'China':'Asia', 
                      'United States':'North America', 
                      'Japan':'Asia', 
                      'United Kingdom':'Europe', 
                      'Russian Federation':'Europe', 
                      'Canada':'North America', 
                      'Germany':'Europe', 
                      'India':'Asia',
                      'France':'Europe', 
                      'South Korea':'Asia', 
                      'Italy':'Europe', 
                      'Spain':'Europe', 
                      'Iran':'Asia',
                      'Australia':'Australia', 
                      'Brazil':'South America'}

    def asignar_continente(row):
        '''Esta función toma una serie. Dentro de la serie controla si el país
        que se encuentra en la columna 'Country' está en el diccionario ContinentDict,
        si está, crea una nueva columna 'Continent' y le agrega el valor del continente
        explicitado en el dic'''
        
        if row['Country'] in ContinentDict:
            row['Continent'] = ContinentDict[row['Country']]
        else:
            row['Continent'] = np.nan
        return row

    interseccion_dataframes = interseccion_dataframes.apply(asignar_continente, axis='columns')

    # Agrupar a los países de acuerdo a su continente
    continentes = interseccion_dataframes.groupby('Continent')
    resumen = continentes.agg({'Continent':len, 'PopEst':(sum, np.mean, np.std)})

    # Le cambio el nombre a las columnas por lo nombres que yo quiero: 
    resumen.columns = ['size', 'sum', 'mean', 'std']
    
    return resumen

print(answer_eleven())