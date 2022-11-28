import pandas as pd
from assignment3_question1_solved_Fefe import answer_one

Top15 = answer_one() # llamo a la función answer_one porque importe el modulo
ContinentDict = {'China': 'Asia',
                 'United States': 'North America',
                 'Japan': 'Asia',
                 'United Kingdom': 'Europe',
                 'Russian Federation': 'Europe',
                 'Canada': 'North America',
                 'Germany': 'Europe',
                 'India': 'Asia',
                 'France': 'Europe',
                 'South Korea': 'Asia',
                 'Italy': 'Europe',
                 'Spain': 'Europe',
                 'Iran': 'Asia',
                 'Australia': 'Australia',
                 'Brazil': 'South America'
                 }

# reseteo el index
Top15 = Top15.reset_index()

# Aplico el continente a cada país
Top15['Continent'] = Top15['Country'].apply(lambda country: ContinentDict[country])

# Genero los grupos/bins
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html
# Use cut when you need to segment and sort data values into bins. 
# This function is also useful for going from a continuous variable to a 
# categorical variable.
# A la columna % Renewable le cambio los % por su grupo de pertenencia (bin)
Top15['% Renewable'] = pd.cut(Top15['% Renewable'], 5)


# Aplico metodo del objeto groupby.size()
#Compute group sizes.
resultado = Top15.groupby(['Continent', '% Renewable']).size()
# Saco de la serie aquellos grupos que no tienen países con bool mask sobre la serie
resultado1 = resultado[resultado>=1]

#%% Respuesta

def answer_twelve():
    Top15 = answer_one() # llamo a la función answer_one porque importe el modulo
    ContinentDict = {'China': 'Asia',
                     'United States': 'North America',
                     'Japan': 'Asia',
                     'United Kingdom': 'Europe',
                     'Russian Federation': 'Europe',
                     'Canada': 'North America',
                     'Germany': 'Europe',
                     'India': 'Asia',
                     'France': 'Europe',
                     'South Korea': 'Asia',
                     'Italy': 'Europe',
                     'Spain': 'Europe',
                     'Iran': 'Asia',
                     'Australia': 'Australia',
                     'Brazil': 'South America'
                     }

    # reseteo el index
    Top15 = Top15.reset_index()

    # Aplico el continente a cada país
    Top15['Continent'] = Top15['Country'].apply(lambda country: ContinentDict[country])

    # Genero los grupos/bins
    # https://pandas.pydata.org/pandas-docs/stable/generated/pandas.cut.html
    # Use cut when you need to segment and sort data values into bins. 
    # This function is also useful for going from a continuous variable to a 
    # categorical variable.
    Top15['% Renewable'] = pd.cut(Top15['% Renewable'], 5)


    resultado = Top15.groupby(['Continent', '% Renewable']).size()
    # Fitro grupos sin países
    resultado = resultado[resultado>=1]
    return resultado

