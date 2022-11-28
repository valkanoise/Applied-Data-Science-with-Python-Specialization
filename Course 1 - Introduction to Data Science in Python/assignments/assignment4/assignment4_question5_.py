import pandas as pd
import numpy as np
import scipy.stats as stats
import re

nhl_df=pd.read_csv("assets/nhl.csv")
nba_df=pd.read_csv("assets/nba.csv")
mlb_df=pd.read_csv("assets/mlb.csv")
nfl_df=pd.read_csv("assets/nfl.csv")
cities=pd.read_html("assets/wikipedia_data.html")[1]
cities=cities.iloc[:-1,[0,3,5,6,7,8]]


# Genero 4 funciones que limpian los dataframes y agrupan a los deportes
# según sus áreas metropolitanas

def NHL_groups_df():
    '''Función que limpia las dataframes cities y nhl_df, luego hace un merge
    entre ambas y agrupa a los equipos según área metropolitana.
    Como resultado devuelve una dataframe que incluye: áreas (grupos como index,
    y las columnas W/L rate, Population y Nr. of teams para cada grupo'''
    
    global nhl_df
    global cities
    
    # Limpio cities['NHL']
    # Hago copia para no modificar la df original que es usada por el resto de las
    # funciones
    
    cities1 = cities.copy()
    cities1["NHL"] = cities1["NHL"].apply(lambda x: re.sub("\[.+\]|\—", "", x))
    cities1["NHL"] = cities1["NHL"].apply(lambda x: re.findall('[A-Z][a-z]+', x))
    cities1 = cities1.explode("NHL")
    
    # Limpio nhl_df dataframe
    nhl_df = nhl_df[nhl_df["year"] == 2018]
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.replace("*", ""))
    nhl_df["team"] = nhl_df["team"].apply(lambda x: x.split(" ")[-1])
    
    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nhl_df, how='inner', left_on="NHL", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)
    
    # Agrupo a los equipos según su ciudad y calculo: WL_ratio, poblacion y nro. equipos 
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})
    group_df['League'] = 'NHL'
    
    return group_df


def NBA_groups_df():
    '''Función que limpia las dataframes cities y nba_df, luego hace un merge
    entre ambas y agrupa a los equipos según área metropolitana.
    Como resultado devuelve una dataframe que incluye: áreas (grupos como index,
    y las columnas W/L rate, Population y Nr. of teams para cada grupo'''
    
    global nba_df
    global cities
    
    # Limpio cities dataframe
    cities1 = cities.copy()
    cities1["NBA"] = cities1["NBA"].apply(lambda x: re.sub("\[.+\]|\—", "", x))
    cities1["NBA"] = cities1["NBA"].apply(lambda x: re.findall('[A-Z][a-z]+|[\d]+[a-z]+', x))
    cities1 = cities1.explode("NBA")
    
    # Limpio nhl_df dataframe
    nba_df = nba_df[nba_df["year"] == 2018]
    nba_df["team"] = nba_df["team"].apply(lambda x: re.sub("\(\d+\)", "", x))
    nba_df["team"] = nba_df["team"].apply(lambda x: x.replace('*', ""))
    nba_df["team"] = nba_df["team"].apply(lambda x: x.split(" ")[-1].strip())
    
    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nba_df, how='inner', left_on="NBA", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)
    
    # Agrupo a los equipos según su ciudad y calculo: WL_ratio, poblacion y nro. equipos 
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})
    group_df['League'] = 'NBA'
    
    return group_df


def MLB_groups_df():
    '''Función que limpia las dataframes cities y mlb_df, luego hace un merge
    entre ambas y agrupa a los equipos según área metropolitana.
    Como resultado devuelve una dataframe que incluye: áreas (grupos como index,
    y las columnas W/L rate, Population y Nr. of teams para cada grupo'''
    
    global mlb_df
    global cities
        
    #Limpio cities dataframe
    cities1 = cities.copy()
    cities1["MLB"] = cities1["MLB"].str.replace("\[.+\]|\—", "", regex = True)
    cities1["MLB"] = cities1["MLB"].apply(lambda x : x.strip())
    cities1["MLB"] = cities1["MLB"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))
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
                continue

    mlb_df = mlb_df.apply(extraer_equipos, axis = 'columns')

    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, mlb_df, how='inner', left_on="MLB", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)

    # Agrupo a los equipos según su ciudad y calculo: WL_ratio, poblacion y nro. equipos 
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})
    group_df['League'] = 'MLB'
    
    return group_df


def NFL_groups_df():
    '''Función que limpia las dataframes cities y nfl_df, luego hace un merge
    entre ambas y agrupa a los equipos según área metropolitana.
    Como resultado devuelve una dataframe que incluye: áreas (grupos como index,
    y las columnas W/L rate, Population y Nr. of teams para cada grupo'''
    
    global nfl_df
    global cities
    
    # Limpio cities dataframe
    cities1 = cities.copy()
    cities1["NFL"] = cities1["NFL"].str.replace("\[.+\]|\—", "", regex = True)
    cities1["NFL"] = cities1["NFL"].apply(lambda x : x.strip())
    cities1["NFL"] = cities1["NFL"].apply(lambda x: re.findall('[A-Z][a-z]+[ ][A-Z][a-z]+|[A-Z][a-z]+|[\d]+[a-z]+', x))
    cities1 = cities1.explode("NFL")

    # Limpio mlb_df dataframe
    nfl_df = nfl_df[nfl_df["year"] == 2018]
    nfl_df["team"] = nfl_df["team"].replace("\W", "", regex=True)
    nfl_df["team"] = nfl_df["team"].str.findall('[A-Z][a-z]+$|[\d]+[a-z]+$')
    nfl_df["team"] = nfl_df["team"].apply(lambda x : x[0])

    # Hago inner merge de los dataframes
    merge_df = pd.merge(cities1, nfl_df, how='inner', left_on="NFL", right_on="team")
    merge_df['WL_ratio'] = merge_df["W"].astype("float")/(merge_df["W"].astype("int") + merge_df["L"].astype("int"))
    merge_df['Population (2016 est.)[8]'] = merge_df['Population (2016 est.)[8]'].astype(int)

    # Agrupo a los equipos según su ciudad y calculo: WL_ratio, poblacion y nro. equipos 
    group_df = merge_df.groupby('Metropolitan area').agg({'WL_ratio':np.mean, 'Population (2016 est.)[8]': np.mean, 'team':len})
    group_df = group_df. rename(columns= {'WL_ratio':'W/L rate', 'Population (2016 est.)[8]':'Population', 'team': 'Nr. of teams'})
    group_df['League'] = 'NFL'
    return group_df


def get_WLrate_Population(deporte):
    '''Función que toma el deporte y selecciona la función adecuada para
    obtener la dataframe con los datos de WL.
    Las posibilidades'''
    
    if deporte == 'NHL':
        nhl = NHL_groups_df()
        # Acá se filtra por aquellas regiones que tienen más de dos equipos
        # nhl = nhl[nhl['Nr. of teams'].map(nhl['Nr. of teams'].value_counts()) >= 2]
        return nhl
    
    if deporte == 'NBA':
        nba = NBA_groups_df()
        # nba = nba[nba['Nr. of teams'].map(nba['Nr. of teams'].value_counts()) >= 2]
        return nba
    
    if deporte == 'MLB':
        mlb = MLB_groups_df()
        # mlb = mlb[mlb['Nr. of teams'].map(mlb['Nr. of teams'].value_counts()) >= 2]
        return mlb
    
    if deporte == 'NFL':
        nfl = NFL_groups_df()
        # nfl = nfl[nfl['Nr. of teams'].map(nfl['Nr. of teams'].value_counts()) >= 2]
        return nfl

def sports_team_performance():
    
    
    #Crea una matriz de correlación vacía y la llena de valones NaN
    sports = ['NFL', 'NBA', 'NHL', 'MLB']
    p_values = pd.DataFrame({k:np.nan for k in sports}, index=sports)
    
    # Iteración que realiza el ttest para cada par de deportes
    for i in sports:
        for j in sports:
            if i!=j: # evitamos realizar comparaciones de un deportse consigo mismo
                # Se importan las dataframes con W/L rate y population calculadas en los ejercicios anteriores
                Mi=get_WLrate_Population(i)
                Mj=get_WLrate_Population(j)
                # Se extraen las columnas W/L rate para cada par de deportes
                Mi=Mi['W/L rate']
                Mj=Mj['W/L rate']
                # Une los deportes según áreas metropolitanas, quedan sólo
                # aquellas áreas que tienen equipos en ambos deportes
                merge=pd.merge(Mi,Mj,how='inner',left_index=True,right_index=True)
                # Realiza T-test y agrega el p-valor resultante en su posición 
                # dentro de la matriz de correlación
                p_values.loc[i, j]=stats.ttest_rel(merge['W/L rate_x'],merge['W/L rate_y'])[1]
    
    # assert abs(p_values.loc["NBA", "NHL"] - 0.02) <= 1e-2, "The NBA-NHL p-value should be around 0.02"
    # assert abs(p_values.loc["MLB", "NFL"] - 0.80) <= 1e-2, "The MLB-NFL p-value should be around 0.80"
    
    return p_values

p_values = sports_team_performance()
print(p_values)
