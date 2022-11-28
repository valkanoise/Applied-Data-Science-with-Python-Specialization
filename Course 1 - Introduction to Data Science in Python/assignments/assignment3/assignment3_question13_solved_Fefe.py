import pandas as pd
import assignment3_question1_solved_Fefe as one

# Importo Top15 países
Top15 =one.answer_one() # llamo a la función answer_one porque importe el modulo

# Calculo la población estimada
Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']

# Transformo PopEst en un string
# https://mkaz.blog/code/python-string-format-cookbook/
Top15['PopEst_string'] = Top15['PopEst'].apply(lambda x : f'{x:,}')

resultado = Top15['PopEst_string']


#%%

def answer_thirteen():
    # Importo Top15 países
    Top15 =one.answer_one() # llamo a la función answer_one porque importe el modulo

    # Calculo la población estimada
    Top15['PopEst'] = Top15['Energy Supply'] / Top15['Energy Supply per Capita']

    # Transformo PopEst en un string
    # https://mkaz.blog/code/python-string-format-cookbook/
    Top15['PopEst_string'] = Top15['PopEst'].apply(lambda x : f'{x:,}')

    return Top15['PopEst_string']
    
    