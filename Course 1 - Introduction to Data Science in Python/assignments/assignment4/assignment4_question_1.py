#%% Abro dataframes

import pandas as pd
import numpy as np
import scipy.stats as stats
import re

cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]

nhl_df=pd.read_csv("assets/nhl.csv")

#%% Lets clean the team names cities['NHL']

# Delete notes at the end, ex: [note 7]
cities["NHL"] = cities["NHL"].replace(to_replace="\[.+\]", value = "", regex = True)

# Extracting the teams:
# The columns ['NHL'] has several teams like TeamTeamTeam and some teams with 2
# words like Maple Leafs
cities["NHL"] = cities["NHL"].apply(lambda x: re.findall('.+ .+|[A-Z][a-z]+', x))


# Elijo las columnas de interés y hago una copia
cities1 = cities.iloc[:,[0,1,-1]].copy()
# Agrego filas donde había varios equipos por fila
# Ahora cada equipo es una nueva fila y replica los datos de las otras columnas
cities1 = cities1.explode("NHL")
#%% Limpio nhl_df dataframe

# Filtro los datos solo del año 2018
nhl_df = nhl_df[nhl_df["year"] == 2018]

# Saco los asteristoc al final de algunos team
nhl_df["team"] = nhl_df["team"].apply(lambda x: x.replace("*", ""))


# Lets clean the Team names in nhl_df because they contain they regions
# ex: Tampa Bay Lightning and we want Lightning

# Create a list of NHL teams
nhl_teams = [x for x in cities1.NHL if x is not np.nan]
# Define function that replaces the Region+Team with only the Team
def limpiar(item):
    for team in nhl_teams:
        if team in item:
            item = team
    return item

nhl_df["team"] = nhl_df["team"].apply(limpiar)

#%% Hago inner merge de los dataframes

# Busco la intersección(inner) sobre las columnas con los nombres de los 
#equipos en cada merge_df
merge_df = pd.merge(cities1, nhl_df, how='inner', left_on="NHL", right_on="team")

# Calculo el WL_Ratio de cada equipo
merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))

# Convierto la col Pop a int para poder hacer próximo paso
merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)

# Agrupo a los equipos según su ciudad y calculo el promedio de WL_ratio 
# de la ciudad, agrego la población y la cantidad de equipos agrupados
group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})

# Cambio nombres de las columnas a [W/L rate, Population, Nr. of teams]
group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})

#%% # Correlación de pearson

population_by_region = group_df['Population']
win_loss_by_region = group_df['W/L rate']

assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"

correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)

print(f'Coeficiente de correlación = {correlacion:.1} y su p-valor= {p_valor:.2}')

#%% 

def nhl_correlation():
    import pandas as pd
    import numpy as np
    import scipy.stats as stats
    import re
    
    nhl_df=pd.read_csv("assets/nhl.csv")
    cities=pd.read_html("assets/wikipedia_data.html")[1]
    cities=cities.iloc[:-1,[0,3,5,6,7,8]]
    
    # Limpio cities dataframe
    cities["NHL"] = cities["NHL"].replace(to_replace="\[.+\]", value = "", regex = True)
    cities["NHL"] = cities["NHL"].apply(lambda x: re.findall('.+ .+|[A-Z][a-z]+', x))
    cities1 = cities.iloc[:,[0,1,-1]].copy()
    cities1 = cities1.explode("NHL")
    
    # Limpio nhl_df dataframe
    nhl_df = nhl_df[nhl_df["year"] == 2018]
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.replace("*", ""))
    nhl_teams = [x for x in cities1.NHL if x is not np.nan]
    def limpiar(item):
        for team in nhl_teams:
            if team in item:
                item = team
        return item
    nhl_df["team"] = nhl_df["team"].apply(limpiar)
    
    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nhl_df, how='inner', left_on="NHL", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("int")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)
    
    # Agrupo por 'Metropolitan Area'
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})
    
    
    # Correlación de pearson
    population_by_region = group_df['Population']
    win_loss_by_region = group_df['W/L rate']
    
    assert len(population_by_region) == len(win_loss_by_region), "Q1: Your lists must be the same length"
    assert len(population_by_region) == 28, "Q1: There should be 28 teams being analysed for NHL"
    
    correlacion, p_valor = stats.pearsonr(population_by_region, win_loss_by_region)
    
    return correlacion

print(nhl_correlation())
