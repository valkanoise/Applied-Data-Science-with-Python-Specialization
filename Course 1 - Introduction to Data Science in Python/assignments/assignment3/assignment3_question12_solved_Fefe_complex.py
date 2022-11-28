# Esta respuesta es compleja

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
        row['Continent'] = 'Another Continent'
    return row

interseccion_dataframes = interseccion_dataframes.apply(asignar_continente, axis='columns')

#%%
# Genero matriz con los Top15 paises y seteamos dos índices

Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15].set_index(['Continent','% Renewable'])


#%% Agrupamos de acuerdo al continente y a 5 rangos/bins de % Renewable
# el '% Renewable max es de 69.64803 y el min es 2.279353

# Calculo los rangos
rango = (Top15.index.max()[1] - Top15.index.min()[1]) / 5

# Creo una lista que contiene los límites de los rangos
lista = [Top15.index.min()[1]]
for i in range(5):
    lista.append(lista[-1]+rango)

# Esta lista la uso para imprimir lindo la nueva columna % Renewable
# Es la lista de arriba pero redondeando sus valores con 2 decimales para
# poner lo nombres lindos en la proxima función
lista2= list(map(lambda x: round(x,2), lista))

# Creo una función que cambiará el index %Renewable de valor numérico a categórico
# y le asignará un bin
def grouping_fun(item):
    if item[1] >= lista[0] and item[1] < lista[1]:
        return (item[0],f'{lista2[0]}-{lista2[1]}') # acá la función no modifica los índices
    if item[1] >= lista[1] and item[1] < lista[2]:
        return (item[0],f'{lista2[1]}-{lista2[2]}')
    if item[1] >= lista[2] and item[1] < lista[3]:
        return (item[0],f'{lista2[2]}-{lista2[3]}')
    if item[1] >= lista[3] and item[1] < lista[4]:
        return (item[0],f'{lista2[3]}-{lista2[4]}')
    else:
        return (item[0],f'{lista2[4]}-{lista2[5]}')
    
grupos = Top15.groupby(by= grouping_fun)

# print(grupos.size())

#%% Crear serie MultiIndex (Continent y bins for % Renewable) y su cantidad 
# de paises en cada una (valores de la serie)

continentes = []
bins = []
paises = []
for group, frame in grupos:
    continentes.append(group[0])
    bins.append(group[1])
    paises.append(len(frame))
    
resultado = pd.Series(paises, index=[continentes, bins])
    

#%% Respuesta

def answer_twelve():
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


    #Abrir segundo data frame a partir de un .csv

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

    # Abrir tercer dataframe a partir de un .xlxs
    ScimEn = pd.read_excel("assets/scimagojr-3.xlsx")

    # Merge de las 3 dataframes


    interseccion_dataframes = (pd.merge(Energy, GDP, how= 'inner', on= 'Country')
                               .merge(ScimEn, how= 'inner', on='Country'))

    # Ordeno por Rank
    interseccion_dataframes.sort_values(by=['Rank'], ascending=True, inplace= True)

    # Calculo la población

    interseccion_dataframes['PopEst'] = interseccion_dataframes['Energy Supply'] / interseccion_dataframes['Energy Supply per Capita']

    # Agregar a qué continente pertenece cada país:
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

    def asignar_continente(row):
        '''Esta función toma una serie. Dentro de la serie controla si el país
        que se encuentra en la columna 'Country' está en el diccionario ContinentDict,
        si está, crea una nueva columna 'Continent' y le agrega el valor del continente
        explicitado en el dic'''
        
        if row['Country'] in ContinentDict:
            row['Continent'] = ContinentDict[row['Country']]
        else:
            row['Continent'] = 'Another Continent'
        return row

    interseccion_dataframes = interseccion_dataframes.apply(asignar_continente, axis='columns')

    # Genero matriz con los Top15 paises y seteamos dos índices
    # Acá se podría haber usado answer_one()
    Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15].set_index(['Continent','% Renewable'])


    #Agrupamos de acuerdo al continente y a 5 rangos/bins de % Renewable

    # Calculo los rangos
    # el '% Renewable max es de 69.64803 y el min es 2.279353
    rango = (Top15.index.max()[1] - Top15.index.min()[1]) / 5

    # Creo una lista que contiene los límites de los rangos para poder generar
    # los límites de los 5 bins
    lista = [Top15.index.min()[1]]
    for i in range(5):
        lista.append(lista[-1]+rango)
    # lista = [2.279353, 15.753088400000001, 29.226823800000002, 42.7005592, 56.1742946, 69.64803]

    # Esta lista la uso para imprimir lindo la nueva columna % Renewable
    # Es la lista de arriba pero redondeando sus valores con 2 decimales para
    # poner lo nombres lindos en la proxima función
    lista2= list(map(lambda x: round(x,2), lista))
    # lista2 = [2.28, 15.75, 29.23, 42.7, 56.17, 69.65]

    # Creo una función que cambiará el index %Renewable de valor numérico a categórico
    # y le asignará un bin
    def grouping_fun(index):
        ''' This function modifies the second index by creating a categorical
        index taking into account the range of 5 bins'''
        if index[1] >= lista[0] and index[1] < lista[1]:
            return (index[0],f'{lista2[0]}-{lista2[1]}') # acá la función no modifica los índices
        if index[1] >= lista[1] and index[1] < lista[2]:
            return (index[0],f'{lista2[1]}-{lista2[2]}')
        if index[1] >= lista[2] and index[1] < lista[3]:
            return (index[0],f'{lista2[2]}-{lista2[3]}')
        if index[1] >= lista[3] and index[1] < lista[4]:
            return (index[0],f'{lista2[3]}-{lista2[4]}')
        else:
            return (index[0],f'{lista2[4]}-{lista2[5]}')
        
    # Genero elemento groupby() con la función anterior
    # Agrupará por continente (index[0]) y por cada uno de los 5 bins categóricos (index[1])
    grupos = Top15.groupby(by= grouping_fun)


    # Crear serie MultiIndex:Continent y bins for % Renewable y su cantidad de paises
    # en cada una
    continentes = []
    bins = []
    paises = []
    for group, frame in grupos:
        continentes.append(group[0])
        bins.append(group[1])
        paises.append(len(frame))
        
    resultado = pd.Series(paises, index=[continentes, bins])
    return resultado
    