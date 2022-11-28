#!/usr/bin/env python
# coding: utf-8

# Sometimes we want to select data based on groups and understand aggregated data on a group level. We have
# seen that even though Pandas allows us to iterate over every row in a dataframe, it is geneally very slow to
# do so. Fortunately Pandas has a groupby() function to speed up such task. The idea behind the groupby()
# function is  that it takes some dataframe, splits it into chunks based on some key values, applies
# computation on those  chunks, then combines the results back together into another dataframe. In pandas this
# is refered to as the split-apply-combine pattern.

# # Splitting

# In[2]:


# Let's look at an example. First, we'll bring in our pandas and numpy libraries
import pandas as pd
import numpy as np


# In[157]:


# Let's look at some US census data
df = pd.read_csv('datasets/census.csv')
# And exclude state level summarizations, which have sum level value of 40
df = df[df['SUMLEV']==50]
df.head()


# In[3]:


# In the first example for groupby() I want to use the census date. Let's get a list of the unique states,
# then we can iterate over all the states and for each state we reduce the data frame and calculate the
# average.

# Let's run such task for 3 times and time it. For this we'll use the cell magic function %%timeit


# In[3]:


get_ipython().run_cell_magic('timeit', '-n 3', "\n# código del curso que es más lento\n\nfor state in df['STNAME'].unique():\n    # We'll just calculate the average using numpy for this particular state\n    avg = np.average(df.where(df['STNAME']==state).dropna()['CENSUS2010POP'])\n    # And we'll print it to the screen\n    print('Counties in state ' + state + \n          ' have an average population of ' + str(avg))")


# In[ ]:


# Se ve que tarda 2,27 segundos

# If you scroll down to the bottom of that output you can see it takes a fair bit of time to finish.
# Now let's try another approach using groupby()


# In[15]:


get_ipython().run_cell_magic('timeit', '-n 3', "\n# Ahora hago mi código, scando where() y drop()\n\n\nfor state in df['STNAME'].unique():\n    # We'll just calculate the average using numpy for this particular state\n    # df['col'].unique() devuelve valores únicos dentro de la Serie\n    \n    # Primero AGRUPAMOS por Estado y extraemos la serie con la columna que no interesa, que incluye info de \n    # todas las ciudades de un estado en particular para cada iteración\n    serie = df[df['STNAME']==state]['CENSUS2010POP']\n    \n        \n    # En segundo lugar APLICAMOS un procesamiento (apply)\n    avg = np.average(serie)\n    \n    # And we'll print it to the screen\n    print('Counties in state ' + state + \n          ' have an average population of ' + str(avg))")


# In[5]:


# Demoró 55 ms
# Esta versión ya fue más rápida que la anterior!


# In[16]:


get_ipython().run_cell_magic('timeit', '-n 3', '\n# Ahora vamos a probar con la función groupby()\n\n# For this method, we start by telling pandas we\'re interested in grouping by state name, this is the "split"\n\nfor group, frame in df.groupby(\'STNAME\'):\n    # You\'ll notice there are two values we set here. groupby() returns a tuple, where the first value is the\n    # value of the key we were trying to group by, in this case a specific state name, and the second one is\n    # projected dataframe that was found for that group\n    \n    # Now we include our logic in the "apply" step, which is to calculate an average of the census2010pop\n    avg = np.average(frame[\'CENSUS2010POP\'])\n    # And print the results\n    print(\'Counties in state \' + group + \n          \' have an average population of \' + str(avg))\n# And we don\'t have to worry about the combine step in this case, because all of our data transformation is\n# actually printing out results.')


# In[7]:


# Demoró 22 ms, menos que mi código

# Wow, what a huge difference in speed. An improve by roughly by two factors!


# In[158]:


# Now, 99% of the time, you'll use group by on one or more columns. But you can also provide a function to
# group by and use that to segment your data.

# This is a bit of a fabricated example but lets say that you have a big batch job with lots of processing and
# you want to work on only a third or so of the states at a given time. We could create some function which
# returns a number between zero and two based on the first character of the state name. Then we can tell group
# by to use this function to split up our data frame. It's important to note that in order to do this you need
# to set the index of the data frame to be the column that you want to group by first.

# We'll create some new function called set_batch_number and if the first letter of the parameter is a capital
# M we'll return a 0. If it's a capital Q we'll return a 1 and otherwise we'll return a 2. Then we'll pass
# this function to the data frame

# le elimino cualquier indice que tenga
df= df.reset_index()

# le asigno el índice por el que quiero agrupar.
# Para usar funciones con groupby() si o si hay que tener un índice, este lo usaremos para agrupar con la función
# La función que le pasemos a groupby() se aplicará sobre el index!!!!!!

df = df.set_index('STNAME')

df.index


# In[53]:


# Definimos la función para agrupar
# Acá se usa el orden de los caracteres para ordenar:
# El orden de caracteres en Python es A-Z y luego a-z
# Las letras mayúsculas usando chr() tiene valores entre 65-91 y las minúsculas (97,123)

# Está función junto con groupby() ira fila por fila en el df y agrupará por grupos de letras:
# 0 = A-L
# 1 = M-P
# 2 = Q-Z

# Acá item = al index de cada fila
def set_batch_number(item):
    # esta función mirá la primer letra dentro de index = item[0]
    if item[0]<'M':
        return 0
    if item[0]<'Q':
        return 1
    return 2

# The dataframe is supposed to be grouped by according to the batch number And we will loop through each batch
# group
for group, frame in df.groupby(set_batch_number):
    print('There are ' + str(len(frame)) + ' records in group ' + str(group) + ' for processing.')
    # agrego una linea para ver qué letras están en cada grupoa
    print('El grupo', str(group), 'incluye a los estados que comienzan con las letras', set([estado[0] for estado in frame.index.unique()]),'\n')


# In[52]:


# Se puede ver que groupby() en conjunto con la función set_batch_number() realizaron los 3 grupos
# Estos grupos se ordenaron por las letras de los estados.


# In[9]:


# Notice that this time I didn't pass in a column name to groupby(). Instead, I set the index of the dataframe
# to be STNAME, and if no column identifier is passed groupby() will automatically use the index.


# In[3]:


# Otro ejemplo para agrupar usando dos índices



# Let's take one more look at an example of how we might group data. In this example, I want to use a dataset
# of housing from airbnb. In this dataset there are two columns of interest, one is the cancellation_policy
# and the other is the review_scores_value.
import pandas as pd
df=pd.read_csv("datasets/listings.csv")
df.head()


# In[8]:


# Seteamos dos índices

# So, how would I group by both of these columns? A first approach might be to promote them to a multiindex
# and just call groupby()
df=df.set_index(["cancellation_policy","review_scores_value"])


# In[142]:


df.head()


# In[144]:


# Ahora agrupamos usando los dos índices anteriores


# When we have a multiindex we need to pass in the levels we are interested in grouping by
for group, frame in df.groupby(level=(0,1)):
    print(group)


# In[137]:


# Como level también se puede poner el nombre de los índices seleccionados previamente

for group, frame in df.groupby(level=("cancellation_policy","review_scores_value")):
    print('Grupo:',group)
    print('Nro. de opiniones:', len(frame), '\n')


# In[ ]:


# Ahora vamos a agrupar con dos columnas pero con criterio sobre la 2da columna
# Esto es más avanzado

# Agrupar usando dos columnas pero aplicar algún criterio de selección en alguna de las columnas
# Ahora vamos a usar una función para elegir 2 columnas, pero en la segunda queremos elegir por calificación
# En la columna de review_scores_value" queremos agrupar por valor=10 por un lado y todas las demás por otro

# This seems to work ok. But what if we wanted to group by the cancelation policy and review scores, but
# separate out all the 10's from those under ten? In this case, we could use a function to manage the
# grouping


# In[9]:


# Si miramos el index, vemos que están expresados como tuplas
# Recordemos que groupby() funciona sobre los índices, en este caso tuplas
# Por ende cuando creamos la función debemos hacerlo considerando que el index son tuplas 
# index en cada fila = (cancellation_policy,review_scores_value)

# Miremos los valores en los índices de las primeros 5 filas. Están expresados como tuplas
df.index[0:5]


# In[10]:


# Creamos función para agrupar considerando los índices como tuplas

# en esta función el item sería el index, y el index está expresado en tuplas, por ende index[0] es el primer índice
# e item[1] es el segundo índice
def grouping_fun(item):
    # Check the "review_scores_value" portion of the index. item is in the format of
    # (cancellation_policy,review_scores_value)
    
    # Queremos seleccionar las calificaciones = 10
    # Hay que definir todos lo grupos, incluso los que no interesan
    if item[1] == 10.0:
        return (item[0],"10.0") # acá la función no modifica los índices
    else:
        return (item[0], "not 10")
    
for group, frame in df.groupby(by=grouping_fun):
    print('Nombre del grupo:',group)
    print('Cantidad filas:', len(frame), '\n')


# # Applying - 2da parte del proceso GROUP-APPLY-COMBINE

# In[14]:


# To this point we have applied very simple processing to our data after splitting, really just outputting
# some print statements to demonstrate how the splitting works. The pandas developers have three broad
# categories of data processing to happen during the apply step, Aggregation of group data, Transformation of
# group data, and Filtration of group data


# ## Aggregation

# In[26]:


# The most straight forward apply step is the aggregation of data, and uses the method agg() on the groupby
# object. Thus far we have only iterated through the groupby object, unpacking it into a label (the group
# name) and a dataframe. But with agg we can pass in a dictionary of the columns we are interested in
# aggregating along with the function we are looking to apply to aggregate.

# Let's reset the index for our airbnb data
df=df.reset_index()

# Now lets group by the cancellation policy and find the average review_scores_value by group
df.groupby("cancellation_policy").agg({"review_scores_value":np.average})

# DA ERRROR porque hay valores NaN


# In[27]:


# Hrm. That didn't seem to work at all. Just a bunch of not a numbers. The issue is actually in the function
# that we sent to aggregate. np.average does not ignore nans! However, there is a function we can use for this

df.groupby("cancellation_policy").agg({"review_scores_value":np.nanmean})


# In[17]:


# We can just extend this dictionary to aggregate by multiple functions or multiple columns.
df.groupby("cancellation_policy").agg({"review_scores_value":(np.nanmean,np.nanstd),
                                      "reviews_per_month":np.nanmean})


# In[18]:


# Take a moment to make sure you understand the previous cell, since it's somewhat complex. First we're doing
# a group by on the dataframe object by the column "cancellation_policy". This creates a new GroupBy object.
# Then we are invoking the agg() function on that object. The agg function is going to apply one or more
# functions we specify to the group dataframes and return a single row per dataframe/group. When we called
# this function we sent it two dictionary entries, each with the key indicating which column we wanted
# functions applied to. For the first column we actually supplied a tuple of two functions. Note that these
# are not function invocations, like np.nanmean(), or function names, like "nanmean" they are references to
# functions which will return single values. The groupby object will recognize the tuple and call each
# function in order on the same column. The results will be in a heirarchical index, but since they are
# columns they don't show as an index per se. Then we indicated another column and a single function we wanted
# to run.


# ## Transformation

# In[19]:


# Transformation is different from aggregation. Where agg() returns a single value per column, so one row per
# group, tranform() returns an object that is the same size as the group. Essentially, it broadcasts the
# function you supply over the grouped dataframe, returning a new dataframe. This makes combining data later
# easy.


# In[28]:


# For instance, suppose we want to include the average rating values in a given group by cancellation policy,
# but preserve the dataframe shape so that we could generate a difference between an individual observation
# and the sum.

# Seleccionamos las columnas de interés
# Una columna será la que usaremos para generar los grupos y en las otra/s se aplicará la transformación
cols=['cancellation_policy','review_scores_value']

# Now lets transform it, I'll store this in its own dataframe
transform_df=df[cols].groupby('cancellation_policy').transform(np.nanmean)
transform_df.head()

# Se puede ver que se calculó la media para cada grupo, y ese valor se puso en la celda de cada fila, por ende los valores
# se repiten en las celdas que pertenecen al mismo grupo 


# In[19]:


# Si miramos la df antes de transformarla pero si agrupada, podemos ver los grupos 
df[cols].groupby('cancellation_policy').head()


# se puede ver que los primeros 4 valores de arriba = 9.307398
# son los mismos porque pertenec al grupo "moderate" (ver abajo)
# O sea, que transform generó una media global para cada grupo, y luego ese valor global lo agregó a cada fila que
# pertenece al grupo "moderate"


# In[29]:


# So we can see that the index here is actually the same as the original dataframe. So lets just join this
# in. 

#Le cambiamos el nombre a la columna transformada de la transform_df
transform_df.rename({'review_scores_value':'mean_review_scores'}, axis='columns', inplace=True)



# ahora que la columna transformada tiene su propio nombre, podemos hacer merge de la df original(95cols) 
# y la transform_df (1 col)

df=df.merge(transform_df, left_index=True, right_index=True)
df.head()

# el resultado es un dataframe de 96 columnas que incluye la nueva columna transformada


# In[24]:


# Great, we can see that our new column is in place, the mean_review_scores. So now we could create, for
# instance, the difference between a given row and it's group (the cancellation policy) means.

# Ahora podemos calcular la diferencia entre el valor de una celda y su media (np.absolute devuelve el valor absoluto)
# Para eso creamos una nueva columna en el df y le asignamos la diferencia
df['mean_diff']=np.absolute(df['review_scores_value']-df['mean_review_scores'])
df['mean_diff'].head()


# In[25]:


# Vemos que le agregamos una columna más, por ende un total de 97
print(len(df.columns))


# ## Filtering

# In[23]:


# The GroupBy object has build in support for filtering groups as well. It's often that you'll want to group
# by some feature, then make some transformation to the groups, then drop certain groups as part of your
# cleaning routines. The filter() function takes in a function which it applies to each group dataframe and
# returns either a True or a False, depending upon whether that group should be included in the results.


# In[30]:


# For instance, if we only want those groups which have a mean rating above 9 included in our results
a= df.groupby('cancellation_policy').filter(lambda x: np.nanmean(x['review_scores_value'])>9.2)


# In[34]:


# Se puede ver que la filtración eliminó los grupos que tenian una media <= 9.2. Eliminó los grupos y sus filas.


print('df original tenía los siguientes grupos:', df['cancellation_policy'].unique())
print('matriz filtrada tirnr los siguientes grupos:',a['cancellation_policy'].unique())


# In[36]:


# Quedaron los grupos con media >9.2 y sus filas. Es posible quealgunos de sus elementos tengan review_scores_value
# menores a 9.2 e incluso NaN pero el promedio general es mayor a 9.2

a[['review_scores_value', 'cancellation_policy', 'mean_review_scores']].head(10)


# In[25]:


# Notice that the results are still indexed, but that any of the results which were in a group with a mean
# review score of less than or equal to 9.2 were not copied over.


# ## Applying

# In[26]:


# By far the most common operation I invoke on groupby objects is the apply() function. This allows you to
# apply an arbitrary function to each group, and stitch the results back for each apply() into a single
# dataframe where the index is preserved.

# Lets look at an example using our airbnb data, I'm going to get a clean copy of the dataframe
df=pd.read_csv("datasets/listings.csv")
# And lets just include some of the columns we were interested in previously
df=df[['cancellation_policy','review_scores_value']]
df.head()


# In[27]:


# In previous work we wanted to find the average review score of a listing and its deviation from the group
# mean. This was a two step process, first we used transform() on the groupby object and then we had to
# broadcast to create a new column. With apply() we could wrap this logic in one place
def calc_mean_review_scores(group):
    # group is a dataframe just of whatever we have grouped by, e.g. cancellation policy, so we can treat
    # this as the complete dataframe
    avg=np.nanmean(group["review_scores_value"])
    # now broadcast our formula and create a new column
    group["review_scores_mean"]=np.abs(avg-group["review_scores_value"])
    return group

# Now just apply this to the groups
df.groupby('cancellation_policy').apply(calc_mean_review_scores).head()


# In[28]:


# Using apply can be slower than using some of the specialized functions, especially agg(). But, if your
# dataframes are not huge, it's a solid general purpose approach


# Groupby is a powerful and commonly used tool for data cleaning and data analysis. Once you have grouped the
# data by some category you have a dataframe of just those values and you can conduct aggregated analsyis on
# the segments that you are interested. The groupby() function follows a split-apply-combine approach - first
# the data is split into subgroups, then you can apply some transformation, filtering, or aggregation, then
# the results are combined automatically by pandas for us.
