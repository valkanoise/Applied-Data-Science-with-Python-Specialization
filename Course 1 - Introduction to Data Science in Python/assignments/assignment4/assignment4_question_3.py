import pandas as pd
import numpy as np
import scipy.stats as stats
import re

mlb_df=pd.read_csv("assets/mlb.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#%% Limpio cities dataframe

# Saco las [notas] final o el  símbolo "—" de la columna MLB
# con series.str.replace() reemplazo el REGEX que busca [notas] por ""
cities["MLB"] = cities["MLB"].str.replace("\[.+\]", "", regex = True)
# Por si acaso aplico strip a los nombres, por si hay espacios ocultos antes o después
cities["MLB"] = cities["MLB"].apply(lambda x : x.strip())

# La columna ['MLB'] tiene varios equipos en formato: EquipoMismo Equipo
# En algunas filas hay equipos con nombres separados por espacio "CubsWhite Sox"
# Separo primero por equipos con nombres que tienen "espacios" y luego por Mayus (al revés NO funciona, el orden de búsqueda importa!!)
# También agrego la posibilidad que elijo equipos que empiecen con nros como los 76ers
cities["MLB"] = cities["MLB"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))

# Elijo las columnas de interés y hago una copia
cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','MLB']].copy()
# Agrego filas donde había varios equipos por fila
# Ahora cada equipo es una nueva fila y replica los datos de las otras columnas
cities1 = cities1.explode("MLB")
#%% Limpio mlb_df dataframe

# Filtro los datos solo del año 2018
mlb_df = mlb_df[mlb_df["year"] == 2018]


def extraer_equipos(row):
    ''' Función que saca la ciudad que antecede al nombre de los equipos'''
    # creo lista de equipos a partir de cities.MLB sacando los datos nan
    equipos = [x.strip() for x in cities1.MLB if type(x) == str]
    
    # Itero sobre los equipos y si están en una fila, reemplazo la columna
    # mlb_df['team'] por el nombre del equipo sin incluir la ciudad
    for equipo in equipos:
        if equipo in row['team']:
            row['team'] = equipo
            return row
        else:
            pass

# Aplico la función anterior y se obtienen los nombres de los equipos
mlb_df = mlb_df.apply(extraer_equipos, axis = 'columns')

#%% Hago inner merge de los dataframes

# Busco la intersección(inner) sobre las columnas con los nombres de los 
#equipos en cada merge_df
merge_df = pd.merge(cities1, mlb_df, how='inner', left_on="MLB", right_on="team")

# Calculo el WL_Ratio de cada equipo
merge_df['WL_ratio'] = merge_df["W"].astype("int")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))

# Convierto la col Pop a int para poder hacer próximo paso
merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)

# Agrupo a los equipos según su ciudad y calculo el promedio de WL_ratio 
# de la ciudad
group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})

# Cambio nombres de las columnas a [W/L rate, Population, Nr. of teams]
group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})

#%% # Correlación de pearson

population_by_region = group_df['Population']
win_loss_by_region = group_df['W/L rate']

assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)

print(f'Coeficiente de correlación = {correlacion:.2} y su p-valor= {p_valor:.2}')


#%% Respuesta 3

def mlb_correlation():
    
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import re
    
    mlb_df=pd.read_csv("assets/mlb.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
   
    # Limpio cities dataframe
    cities["MLB"] = cities["MLB"].str.replace("\[.+\]", "", regex = True)
    cities["MLB"] = cities["MLB"].apply(lambda x : x.strip())
    cities["MLB"] = cities["MLB"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))
    cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','MLB']].copy()
    cities1 = cities1.explode("MLB")

    # Limpio mlb_df dataframe
    mlb_df = mlb_df[mlb_df["year"] == 2018]
    def extraer_equipos(row):
        ''' Función que saca la ciudad que antecede al nombre de los equipos'''
        equipos = [x.strip() for x in cities1.MLB if type(x) == str]
        for equipo in equipos:
            if equipo in row['team']:
                row['team'] = equipo
                return row
            else:
                pass
    mlb_df = mlb_df.apply(extraer_equipos, axis = 'columns')

    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, mlb_df, how='inner', left_on="MLB", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean})
    group_df.rename(inplace= True, columns = {'WL_ratio':'WL_ratio_mean', 'Population (2016 est.)[8]':'Population'})
    
    # Correlación de pearson
    population_by_region = group_df['Population']
    win_loss_by_region = group_df['WL_ratio_mean']

    assert len(population_by_region) == len(win_loss_by_region), "Q3: Your lists must be the same length"
    assert len(population_by_region) == 26, "Q3: There should be 26 teams being analysed for MLB"

    correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return correlacion

print(f'Coeficiente de correlación = {mlb_correlation()}')
    