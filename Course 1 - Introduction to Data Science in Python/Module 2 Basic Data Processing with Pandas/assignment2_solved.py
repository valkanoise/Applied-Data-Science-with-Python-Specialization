import pandas as pd


df= pd.read_csv("NISPUF17.csv")

#%%

diccionario = {}

diccionario["less than high school"] = len(df[df['EDUC1']==1]) / len(df)
diccionario["high school"] = len(df[df['EDUC1']==2]) / len(df)
diccionario["more than high school but not college"] = len(df[df['EDUC1']==3])/ len(df)
diccionario["college"] = len(df[df['EDUC1']==4]) / len(df)

#%% Question 1
def proportion_of_education():
    import pandas as pd
    df= pd.read_csv("NISPUF17.csv")
    
    diccionario = {}

    diccionario["less than high school"] = len(df[df['EDUC1']==1]) / len(df)
    diccionario["high school"] = len(df[df['EDUC1']==2]) / len(df)
    diccionario["more than high school but not college"] = len(df[df['EDUC1']==3]) / len(df)
    diccionario["college"] = len(df[df['EDUC1']==4]) / len(df)
    
    return diccionario    
    
    
    raise NotImplementedError()
    
#%% Question 2:

# CBF_01: brestfeded 1 = yes | 2 = no
# P_NUMFLU: total number of seasonal influenza doses

def average_influenza_doses():
    import pandas as pd
    df= pd.read_csv("assets/NISPUF17.csv")
    
    # Promedio de vacunas de influenza para los brestfeded
    yes = df[df['CBF_01']==1]['P_NUMFLU'].dropna().mean()
    # # Promedio de vacunas de influenza para los NO brestfeded
    no = df[df['CBF_01']==2]['P_NUMFLU'].dropna().mean()
    
    return (yes, no)
    raise NotImplementedError()

#%% Question 3

'''Calculate the ratio of the number of children who contracted chickenpox 
but were vaccinated against it (at least one varicella dose) versus those who 
were vaccinated but did not contract chicken pox. Return results by sex.'''

# HAD_CPOX: had chickenpox 1= yes | 2 = no
# P_NUMVRC: number of varicella vaccine shots
# SEX: 1 = male | 2 = female

# Filtro los vacunados
df[df['P_NUMVRC']>=1]


### Vacunados que contrajeron chickenpox
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==1]
# varones
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==1][df['SEX']==1]
# mujeres
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==1][df['SEX']==2]

### Vacunados que no contrajeron chickenpox
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==2]
# varones
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==2][df['SEX']==1]
# mujeres
df[df['P_NUMVRC']>=1][df['HAD_CPOX']==2][df['SEX']==2]

#%%

def chickenpox_by_sex():
    import pandas as pd
    df= pd.read_csv("assets/NISPUF17.csv")
    
    diccionario = {}
    varones_enfermos = len(df[df['P_NUMVRC']>=1][df['HAD_CPOX']==1][df['SEX']==1])
    varones_no_enfermos = len(df[df['P_NUMVRC']>=1][df['HAD_CPOX']==2][df['SEX']==1])
    mujeres_enfermas = len(df[df['P_NUMVRC']>=1][df['HAD_CPOX']==1][df['SEX']==2])
    mujeres_no_enfermas = len(df[df['P_NUMVRC']>=1][df['HAD_CPOX']==2][df['SEX']==2])
    ratio_hombres = varones_enfermos / varones_no_enfermos
    ratio_mujeres = mujeres_enfermas / mujeres_no_enfermas
    diccionario['male'] = ratio_hombres
    diccionario['female'] = ratio_mujeres
    return diccionario
        
    raise NotImplementedError()
    
#%% Question 4
import scipy.stats as stats
import pandas as pd

# Me quedo con las filas de quienes tuvieron o no tuvieron chickenpox
# y además con aquellos que recibieron 0 o más dosis.
filtrados = df[(df['HAD_CPOX']==1) | (df['HAD_CPOX']==2)] [df['P_NUMVRC']>=0]

# Elijo la columna con los datos de si tuvieron o no chickenpox
had_chickenpox_column= filtrados['HAD_CPOX']

# Selecciono la columna con las dosis de la vacuna. 
num_chickenpox_vaccine_column= filtrados['P_NUMVRC']

corr, pval=stats.pearsonr(had_chickenpox_column,num_chickenpox_vaccine_column)

#%%

def corr_chickenpox():
    import scipy.stats as stats
    import pandas as pd
    df= pd.read_csv("assets/NISPUF17.csv")
    
    filtrados = df[(df['HAD_CPOX']==1) | (df['HAD_CPOX']==2)] [df['P_NUMVRC']>=0]
    had_chickenpox_column= filtrados['HAD_CPOX']
    num_chickenpox_vaccine_column= filtrados['P_NUMVRC']
    corr, pval = stats.pearsonr(had_chickenpox_column,num_chickenpox_vaccine_column)
    
    return corr

    raise NotImplementedError()

