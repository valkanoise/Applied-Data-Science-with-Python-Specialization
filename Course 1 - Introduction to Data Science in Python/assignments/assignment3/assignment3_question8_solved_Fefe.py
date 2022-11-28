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


#%% Estimar población
Energy['Estimated Population'] = Energy['Energy Supply'] / Energy['Energy Supply per Capita']

# País más habitado
pais = Energy.set_index('Country')['Estimated Population'].idxmax()

#%% Respuesta 

def answer_eight():
   import pandas as pd
   import numpy as np

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
   
   # Estimo la poblacion
   Energy['Estimated Population'] = Energy['Energy Supply'] / Energy['Energy Supply per Capita']

   # País más habitado
   pais = Energy.set_index('Country')['Estimated Population'].idxmax()
   
   return pais

print(f'El país más habitado es {answer_eight()}')