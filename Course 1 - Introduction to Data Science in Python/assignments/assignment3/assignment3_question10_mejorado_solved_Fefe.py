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

#%% Ejercicio 10

# Busco la mediana de '% Renewable' para los Top15 países
# Para eso selecciono los top15 paises según rank y selecciono col % Renewable y calculo la mediana
Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]

median_Top15 = np.median(Top15['% Renewable'])

# Genero función para que vaya fila(serie) por serie comparando la mediana y
# agregando 1 o 0 si es mayor o menor
def above_median(row):
    if row['% Renewable']>= median_Top15:
        row['HighRenew'] = 1
    else:
        row['HighRenew'] = 0
    return row

# Aplico la función y agrega una columna más "Above Median Top 15"
Top15 = Top15.apply(above_median, axis="columns")

# Ordeno la dataframe por orden alfabético
Top15.sort_values(by=['Rank'], ascending=True, inplace= True)

Top15 = Top15.set_index('Country')

# Creo serie que devuelve Países ordenados por rank y sus valores de 
# 'HighRenew'
resultado = Top15['HighRenew']


print(resultado)


#%% Respuesta

def answer_ten():
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

    ### Ejercicio 10

    Top15 = interseccion_dataframes[interseccion_dataframes['Rank']<=15]
    median_Top15 = np.median(Top15['% Renewable'])
    def above_median(row):
        if row['% Renewable']>= median_Top15:
            row['HighRenew'] = 1
        else:
            row['HighRenew'] = 0
        return row

    Top15 = Top15.apply(above_median, axis="columns")
    Top15.sort_values(by=['Rank'], ascending=True, inplace= True)
    Top15 = Top15.set_index('Country')

    return Top15['HighRenew']


print(answer_ten())