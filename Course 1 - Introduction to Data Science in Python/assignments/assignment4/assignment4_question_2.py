import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nba_df=pd.read_csv("assets/nba.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

#%% Limpio cities dataframe

# Saco las [notas] final o el  símbolo "—" de la columna NBA
# con re.sub() reemplazo el REGEX que busca [notas] por ""
cities["NBA"] = cities["NBA"].apply(lambda x: re.sub("\[.+\]", "", x))

# La columna ['NHL'] tiene varios equipos en formato: EquipoEquipoEquipo
# Separo los equipos dentro de una lista con re seleccionado con Mayus
# También agrego la posibilidad que elijo equipos que empiecen con nros como los 76ers
# También agrego la posibilidad de seleccionar equipos con nombres compuestos por 2 palabras: Trail Blazers
cities["NBA"] = cities["NBA"].apply(lambda x: re.findall('.+ .+|[A-Z][a-z]+|[\d]+[a-z]+', x))

# Elijo las columnas de interés y hago una copia
cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','NBA']].copy()
# Agrego filas donde había varios equipos por fila
# Ahora cada equipo es una nueva fila y replica los datos de las otras columnas
cities1 = cities1.explode("NBA")
#%% Limpio nhl_df dataframe

# Filtro los datos solo del año 2018
nba_df = nba_df[nba_df["year"] == 2018]

# Saco los (X) al final de algunos team
nba_df["team"] = nba_df["team"].apply(lambda x: re.sub("\(\d+\)", "", x))
# Saco los * al final de algunos team
nba_df["team"] = nba_df["team"].apply(lambda x: x.replace('*', ""))

# Lets clean the Team names in nhl_df because they contain they regions
# ex: Portland Trail Blazers and we want Blazers

# Create a list of NBA teams
nba_teams = [x for x in cities1.NBA if x is not np.nan]
# Define function that replaces the Region+Team with only the Team
def limpiar(item):
    for team in nba_teams:
        if team in item:
            item = team
    return item

nba_df["team"] = nba_df["team"].apply(limpiar)

#%% Hago inner merge de los dataframes

# Busco la intersección(inner) sobre las columnas con los nombres de los 
#equipos en cada merge_df
merge_df = pd.merge(cities1, nba_df, how='inner', left_on="NBA", right_on="team")

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

assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)

print(f'Coeficiente de correlación = {correlacion} y su p-valor= {p_valor}')


#%% Respuesta 2

def nba_correlation():
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import re

    nba_df=pd.read_csv("assets/nba.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    
    # Limpio cities dataframe
    cities["NBA"] = cities["NBA"].apply(lambda x: re.sub("\[.+\]", "", x))
    cities["NBA"] = cities["NBA"].apply(lambda x: re.findall('.+ .+|[A-Z][a-z]+|[\d]+[a-z]+', x))
    cities1 = cities[['Metropolitan area','Population (2016 est.)[8]','NBA']].copy()
    cities1 = cities1.explode("NBA")

    # Limpio nba dataframe
    nba_df = nba_df[nba_df["year"] == 2018]
    nba_df["team"] = nba_df["team"].apply(lambda x: re.sub("\(\d+\)", "", x))
    nba_df["team"] = nba_df["team"].apply(lambda x: x.replace('*', ""))
    nba_teams = [x for x in cities1.NBA if x is not np.nan]
    def limpiar(item):
        for team in nba_teams:
            if team in item:
                item = team
        return item
    nba_df["team"] = nba_df["team"].apply(limpiar)
    
    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nba_df, how='inner', left_on="NBA", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("int")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)

    # Agrupo por 'Metropolitan Area'
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})

    # Correlación de pearson
    population_by_region = group_df['Population']
    win_loss_by_region = group_df['W/L rate']

    assert len(population_by_region) == len(win_loss_by_region), "Q2: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q2: There should be 28 teams being analysed for NBA"

    correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return correlacion
    
print(f'Coeficiente de correlación = {nba_correlation()}')
