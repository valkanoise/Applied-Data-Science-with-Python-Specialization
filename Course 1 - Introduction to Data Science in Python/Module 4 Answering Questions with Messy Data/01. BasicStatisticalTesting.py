#!/usr/bin/env python
# coding: utf-8

# In this lecture we're going to review some of the basics of statistical testing in python. We're going to
# talk about hypothesis testing, statistical significance, and using scipy to run student's t-tests.

# In[1]:


# We use statistics in a lot of different ways in data science, and on this lecture, I want to refresh your
# knowledge of hypothesis testing, which is a core data analysis activity behind experimentation. The goal of
# hypothesis testing is to determine if, for instance, the two different conditions we have in an experiment 
# have resulted in different impacts

# Let's import our usual numpy and pandas libraries
import numpy as np
import pandas as pd

# Now let's bring in some new libraries from scipy
from scipy import stats


# In[2]:


# Now, scipy is an interesting collection of libraries for data science and you'll use most or perpahs all of
# these libraries. It includes numpy and pandas, but also plotting libraries such as matplotlib, and a
# number of scientific library functions as well


# In[48]:


# When we do hypothesis testing, we actually have two statements of interest: the first is our actual
# explanation, which we call the alternative hypothesis, and the second is that the explanation we have is not
# sufficient, and we call this the null hypothesis. Our actual testing method is to determine whether the null
# hypothesis is true or not. If we find that there is a difference between groups, then we can reject the null
# hypothesis and we accept our alternative.

# Let's see an example of this; we're going to use some grade data
df=pd.read_csv ('datasets/grades.csv')
df.head()


# In[4]:


# If we take a look at the data frame inside, we see we have six different assignments. Lets look at some
# summary statistics for this DataFrame

# Con .format()
print("There are {} rows and {} columns".format(df.shape[0], df.shape[1]))

# Con f'strings
print(f"There are {df.shape[0]} rows and {df.shape[1]} columns")


# In[5]:


# Vamos a explorar fechas del assignment 1:
df_fechas =  df['assignment1_submission']

# Convierto las fechas a to_datetime()
df_fechas_to_datetime = pd.to_datetime(df_fechas)

print(f'Sin datetime() Max= {df_fechas.max()} Min= {df_fechas.min()}')
print(f'Con datetime() Max= {df_fechas_to_datetime.max()} Min= {df_fechas_to_datetime.min()}')

# Se puede ver que Pandas ya detectó las fechas sin utilizar to_datetime()


# In[7]:


# For the purpose of this lecture, let's segment this population into two pieces. Let's say those who finish
# the first assignment by the end of December 2015, we'll call them early finishers, and those who finish it 
# sometime after that, we'll call them late finishers.

early_finishers=df[df['assignment1_submission'] < '2016']

print(len(early_finishers))

early_finishers.head()


# In[8]:


# So, you have lots of skills now with pandas, how would you go about getting the late_finishers dataframe?
# Why don't you pause the video and give it a try.


# In[9]:


# Pruebo con mi solución

df_late_finishers = df[pd.to_datetime(df['assignment1_submission']) >= '2016']

print(len(df_late_finishers))
print('Total= early_finishers + late_finishers =', len(df_late_finishers)+ len(early_finishers))

df_late_finishers.head()


# In[35]:


# Here's my solution. First, the dataframe df and the early_finishers share index values, so I really just
# want everything in the df which is not in early_finishers


# El símbolo "~" lo que hace es cambiar los True->False y los False->True
# Es una forma rápida de invertir la selección
# Por ende está invirtiendo los resultados, cambia los index de early_finishers de True->False y todos los demás índices,
# o sea, aquellos que terminaron después los cambia de False->True
# Como resultado se obtienen los late_finishers a partir de elegir todos los demás índices que son pertenecen a la 
# df early_finishers
late_finishers=df[~df.index.isin(early_finishers.index)]
late_finishers.head()


# In[8]:


# There are lots of other ways to do this. For instance, you could just copy and paste the first projection
# and change the sign from less than to greater than or equal to. This is ok, but if you decide you want to
# change the date down the road you have to remember to change it in two places. You could also do a join of
# the dataframe df with early_finishers - if you do a left join you only keep the items in the left dataframe,
# so this would have been a good answer. You also could have written a function that determines if someone is
# early or late, and then called .apply() on the dataframe and added a new column to the dataframe. This is a
# pretty reasonable answer as well.


# In[47]:


# Otra forma haciendo un merge

# Creo una merge y le agrega una columna '_merge' que indica de que matriz vienen los datos: 'left_only', 'right_only' o 'both'
late_finishers2 = pd.merge(df, early_finishers, how='left', left_index=True, right_index=True, indicator=True)

# Filtro los datos que solo vienen de la matriz df y excluyo lo de early_finishers
# Además sólo me quedo con las columnas de df porque merge sumó las columnas de early_finishers
late_finishers2 = late_finishers2[late_finishers2["_merge"]=='left_only'].iloc[:,0:13]

# Cambio el nombre de las columnas por sus nombre originales porque el merge les agrego _x
late_finishers2.columns = df.columns

# Corroboro que este método sea igual al del docente
(late_finishers2 == late_finishers).head()


# In[15]:


# As you've seen, the pandas data frame object has a variety of statistical functions associated with it. If
# we call the mean function directly on the data frame, we see that each of the means for the assignments are
# calculated. Let's compare the means for our two populations

print(early_finishers['assignment1_grade'].mean())
print(late_finishers['assignment1_grade'].mean())


# In[50]:


# Ok, these look pretty similar. But, are they the same? What do we mean by similar? This is where the
# students' t-test comes in. It allows us to form the alternative hypothesis ("These are different") as well
# as the null hypothesis ("These are the same") and then test that null hypothesis.

# When doing hypothesis testing, we have to choose a significance level as a threshold for how much of a
# chance we're willing to accept. This significance level is typically called alpha. #For this example, let's
# use a threshold of 0.05 for our alpha or 5%. Now this is a commonly used number but it's really quite
# arbitrary.

# The SciPy library contains a number of different statistical tests and forms a basis for hypothesis testing
# in Python and we're going to use the ttest_ind() function which does an independent t-test (meaning the
# populations are not related to one another). The result of ttest_index() are the t-statistic and a p-value.
# It's this latter value, the probability, which is most important to us, as it indicates the chance (between
# 0 and 1) of our null hypothesis being True.

# Let's bring in our ttest_ind function
from scipy.stats import ttest_ind

# Let's run this function with our two populations, looking at the assignment 1 grades
ttest_ind(early_finishers['assignment1_grade'], late_finishers['assignment1_grade'])


# In[51]:


# So here we see that the probability is 0.18, and this is above our alpha value of 0.05. This means that we
# cannot reject the null hypothesis. The null hypothesis was that the two populations are the same, and we
# don't have enough certainty in our evidence (because it is greater than alpha) to come to a conclusion to
# the contrary. This doesn't mean that we have proven the populations are the same.


# In[52]:


# Why don't we check the other assignment grades?
print(ttest_ind(early_finishers['assignment2_grade'], late_finishers['assignment2_grade']))
print(ttest_ind(early_finishers['assignment3_grade'], late_finishers['assignment3_grade']))
print(ttest_ind(early_finishers['assignment4_grade'], late_finishers['assignment4_grade']))
print(ttest_ind(early_finishers['assignment5_grade'], late_finishers['assignment5_grade']))
print(ttest_ind(early_finishers['assignment6_grade'], late_finishers['assignment6_grade']))


# In[13]:


# Ok, so it looks like in this data we do not have enough evidence to suggest the populations differ with
# respect to grade. Let's take a look at those p-values for a moment though, because they are saying things
# that can inform experimental design down the road. For instance, one of the assignments, assignment 3, has a
# p-value around 0.1. This means that if we accepted a level of chance similarity of 11% this would have been
# considered statistically significant. As a research, this would suggest to me that there is something here
# worth considering following up on. For instance, if we had a small number of participants (we don't) or if
# there was something unique about this assignment as it relates to our experiment (whatever it was) then
# there may be followup experiments we could run.


# In[106]:


# P-values have come under fire recently for being insuficient for telling us enough about the interactions
# which are happening, and two other techniques, confidence intervalues and bayesian analyses, are being used
# more regularly. One issue with p-values is that as you run more tests you are likely to get a value which
# is statistically significant just by chance.

# Lets see a simulation of this. First, lets create a data frame of 100 columns, each with 100 numbers

# Mediante list comprehension crea 100 arrays con 100 nros al azar con valores entre 0 y 1
# np.random.random(filas) estará definiendo el nro de filas de nuestra dataframe
# range(columnas) estará definiendo el nro de columnas que queremos en nuestra dataframe

## Recordar ## np.random.random() devuelve una distribución normal de los datos
df1=pd.DataFrame([np.random.random(100) for x in range(100)])
df1.head()


# In[107]:


# Pause this and reflect -- do you understand the list comprehension and how I created this DataFrame? You
# don't have to use a list comprehension to do this, but you should be able to read this and figure out how it
# works as this is a commonly used approach on web forums.


# In[108]:


# Ok, let's create a second dataframe
df2=pd.DataFrame([np.random.random(100) for x in range(100)])


# In[109]:


df1.columns


# In[114]:


# Ahora tenemos 2 dataframes de 100x100 con datos al azar

# Qué pasaría si comparamos cada una de las columnas de una df con las mismas cols de la otra data frame?
# Habrá diferencia estadísticamente significativa?
# La teoría dice que al ser datos al azar NO debería existir diferencias esadísticamente significativas, pero por azar
# podría ser que haya.
# Para eso fijamos un valor de alpha, que es hasta cuánto azar nos permitimos tolerar
# Alpha define la posibilidad de falsos positivos


# Are these two DataFrames the same? Maybe a better question is, for a given row inside of df1, is it the same
# as the row inside df2?

# Let's take a look. Let's say our critical value is 0.1, or and alpha of 10%. And we're going to compare each
# column in df1 to the same numbered column in df2. And we'll report when the p-value is less than 10%,
# which means that we have sufficient evidence to say that the columns between df1 and df2 are different.

# Let's write this in a function called test_columns
def test_columns(alpha=0.1):
    # I want to keep track of how many differ
    num_diff=0
    # And now we can just iterate over the columns
    for col in df1.columns:
        # we can run out ttest_ind between the two dataframes
        teststat,pval=ttest_ind(df1[col],df2[col])
        # and we check the pvalue versus the alpha
        if pval<=alpha:
            # And now we'll just print out if they are different and increment the num_diff
            print("Col {} is statistically significantly different at alpha={}, pval={}".format(col,alpha,pval))
            num_diff=num_diff+1
    # and let's print out some summary stats
    print("Total number different was {}, which is {}%".format(num_diff,float(num_diff)/len(df1.columns)*100))

# And now lets actually run this
test_columns()


# In[111]:


# Interesting, so we see that there are a bunch of columns that are different! In fact, that number looks a
# lot like the alpha value we chose. So what's going on - shouldn't all of the columns be the same? Remember
# that all the ttest does is check if two sets are similar given some level of confidence, in our case, 10%.
# The more random comparisons you do, the more will just happen to be the same by chance. In this example, we
# checked 100 columns, so we would expect there to be roughly 10 of them if our alpha was 0.1.

# We can test some other alpha values as well
test_columns(0.05)


# In[112]:


test_columns(0.01)


# In[117]:


# Esto es lo mismo que la linea 112
teststat,pval = ttest_ind(df1,df2,axis=0)
a= pval
a<0.01


# In[104]:


# So, keep this in mind when you are doing statistical tests like the t-test which has a p-value. Understand
# that this p-value isn't magic, that it's a threshold for you when reporting results and trying to answer
# your hypothesis. What's a reasonable threshold? Depends on your question, and you need to engage domain
# experts to better understand what they would consider significant.

# Just for fun, lets recreate that second dataframe using a non-normal distribution, I'll arbitrarily chose
# chi squared
df2=pd.DataFrame([np.random.chisquare(df=1,size=100) for x in range(100)])
test_columns()


# In[20]:


# Now we see that all or most columns test to be statistically significant at the 10% level.


# In this lecture, we've discussed just some of the basics of hypothesis testing in Python. I introduced you
# to the SciPy library, which you can use for the students t test. We've discussed some of the practical
# issues which arise from looking for statistical significance. There's much more to learn about hypothesis
# testing, for instance, there are different tests used, depending on the shape of your data and different
# ways to report results instead of just p-values such as confidence intervals or bayesian analyses. But this
# should give you a basic idea of where to start when comparing two populations for differences, which is a
# common task for data scientists.
