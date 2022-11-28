import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#%% Limpio cities dataframe

# Saco las [notas] final o el  símbolo "—" de la columna MLB
# con series.str.replace() reemplazo el REGEX que busca [notas] por ""
cities["NFL"] = cities["NFL"].str.replace("\[.+\]|\—", "", regex = True)
# Por si acaso aplico strip a los nombres, por si hay espacios ocultos antes o después
cities["NFL"] = cities["NFL"].apply(lambda x : x.strip())

# La columna ['NFL'] tiene varios equipos en formato: EquipoMismo Equipo
# Separo los equipos dentro de una lista con re seleccionado con Mayus
# En algunas filas hay equipos con nombres separados por espacio "EquipoRed Sox"
# Separo primero por equipos con nombres que tienen "espacios" y luego por Mayus (al revés NO funciona, el orden de búsqueda importa!!)
# También agrego la posibilidad que elijo equipos que empiecen con nros como los 76ers
cities["NFL"] = cities["NFL"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))


# Elijo las columnas de interés y hago una copia
cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','NFL']].copy()
# Agrego filas donde había varios equipos por fila
# Ahora cada equipo es una nueva fila y replica los datos de las otras columnas
cities1 = cities1.explode("NFL")

#%% Limpio mlb_df dataframe

# Filtro los datos solo del año 2018
nfl_df = nfl_df[nfl_df["year"] == 2018]

# Saco de la columna team símbolos que hay al final de los nombres (por ej * y +)
nfl_df["team"] = nfl_df["team"].replace("\W", "", regex=True)

# Extraigo los equipos dado que están unidos a su ciudad: CiudadEquipo
# Uso REGEX para extraer patrones que teminen con Equipo | Nros y letras (ej: 79ers)
nfl_df["team"] = nfl_df["team"].str.findall('[A-Z][a-z]+|[\d]+[a-z]+')
# Junto la listas en un string
nfl_df["team"] = nfl_df["team"].apply(lambda x: ' '.join(x))


# Create a list of NBA teams
nfl_teams = [x for x in cities1.NFL if x is not np.nan]
# Define function that replaces the Region+Team with only the Team
def limpiar(item):
    ''' Función que saca la ciudad que antecede al nombre de los equipos
    Se debe ingresar la columna con las Zonas+Equipos'''
    # Create a list of NBA teams
    nfl_teams = [x for x in cities1.NFL if x is not np.nan]
    for team in nfl_teams:
        if team in item:
            item = team
    return item

nfl_df["team"] = nfl_df["team"].apply(limpiar)


#%% Hago inner merge de los dataframes

# Busco la intersección(inner) sobre las columnas con los nombres de los 
#equipos en cada merge_df
merge_df = pd.merge(cities1, nfl_df, how='inner', left_on="NFL", right_on="team")

# Calculo el WL_Ratio de cada equipo
merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))

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

assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)

print(f'Coeficiente de correlación = {correlacion:.2} y su p-valor= {p_valor:.2}')

#%% Respuesta 4

def nfl_correlation(): 
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import re

    nfl_df=pd.read_csv("assets/nfl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    
    # Limpio cities dataframe
    cities["NFL"] = cities["NFL"].str.replace("\[.+\]|\—", "", regex = True)
    cities["NFL"] = cities["NFL"].apply(lambda x : x.strip())
    cities["NFL"] = cities["NFL"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))
    cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','NFL']].copy()
    cities1 = cities1.explode("NFL")

    # Limpio nfl_df dataframe
    nfl_df = nfl_df[nfl_df["year"] == 2018]
    nfl_df["team"] = nfl_df["team"].replace("\W", "", regex=True)
    nfl_df["team"] = nfl_df["team"].str.findall('[A-Z][a-z]+|[\d]+[a-z]+')
    nfl_df["team"] = nfl_df["team"].apply(lambda x: ' '.join(x))
    def limpiar(item):
        ''' Función que saca la ciudad que antecede al nombre de los equipos
        Se debe ingresar la columna con las Zonas+Equipos'''
        # Create a list of NBA teams
        nfl_teams = [x for x in cities1.NFL if x is not np.nan]
        for team in nfl_teams:
            if team in item:
                item = team
        return item
    nfl_df["team"] = nfl_df["team"].apply(limpiar)

    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nfl_df, how='inner', left_on="NFL", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean})
    group_df.rename(inplace= True, columns = {'WL_ratio':'WL_ratio_mean', 'Population (2016 est.)[8]':'Population'})

    # Correlación de pearson
    population_by_region = group_df['Population']
    win_loss_by_region = group_df['WL_ratio_mean']

    assert len(population_by_region) == len(win_loss_by_region), "Q4: Your lists must be the same length"
    assert len(population_by_region) == 29, "Q4: There should be 29 teams being analysed for NFL"

    correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)
    return correlacion


print(f'Coeficiente de correlación = {nfl_correlation():.2}')

