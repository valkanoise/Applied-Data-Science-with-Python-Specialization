''' Ejercicio para abrir archivos csv y parsearlos con el modulo csv'''

import csv

#%% Abrir el archivo csv
'''Abro el archivo csv y con el modulo csv y su funcion DictReader se parsea
el archivo y se arma un diccionario para cada linea, donde los keys son
los elementos de la primera fila y sus values son los elementos de cadafila.
Luego con la funcion list se crea una lista de diccionarios porque DictReader
devuelve un objeto del tipo DictReader '''
 
with open('mpg.csv') as csvfile:
    mpg = csv.DictReader(csvfile) # 
    mpg = list(mpg) # crea una lista con todos los diccionarios creados antes
    

#%% Calculo consumo galones promedio en ciudad

# 1ro con list comprehension creo lista con todos los valores de 'cty' en los distintos diccionarios
# estos valores están como strings por lo que hay que hacerlos float
lista_consumos_ciudad = [float(dic['cty']) for dic in mpg]

# Luego se suman los consumos
suma_consumos_ciudad = sum(lista_consumos_ciudad)

# Luego Calculo el promedio dividiendo la suma por la cantidad de autos
promedio_consumos_ciudad = suma_consumos_ciudad / len(mpg)

# Todo en una sola linea
consumo_promedio_ciudad = sum([float(dic['cty']) for dic in mpg]) / len(mpg)

#%% Calculo consumo galones promedio en highway
consumo_promedio_autopista = sum([float(dic['hwy']) for dic in mpg]) / len(mpg)

#%% Número de cilindros en los autos

cilindros = set([dic['cyl'] for dic in mpg])

#%% Consumo promedio de galones en ciudad según nro de cilindros

Con_prom_ciudad_cil = []

for cil in cilindros:
    consumo = 0
    cantidad = 0
    for dic in mpg:
        if dic['cyl'] == cil: #ojo que acá ambos valores son strings! Sino no se pueden comparar
            consumo += float(dic['cty'])
            cantidad += 1
    Con_prom_ciudad_cil.append((cil, consumo/cantidad))

# Ordenado por nro ascendiente de cilindros pero sorted no muta la lista, la ordena
print('Consumo segun nro de cilindros:' ,sorted(Con_prom_ciudad_cil, reverse=False))
print()  
#%% Highway mpg segun la clase

clases = set([dic['class'] for dic in mpg])
# print(clases)

Con_prom_autopista_clase = []

for cla in clases:
    consumo = 0
    cantidad = 0
    for dic in mpg:
        if dic['class'] == cla: #ojo que acá ambos valores son strings! Sino no se pueden comparar
            consumo += float(dic['hwy'])
            cantidad += 1
    Con_prom_autopista_clase.append((cla, consumo/cantidad))

# Las ordenamos según sus consumos y no por clase usando sort y como key una expresión lambda.
# La expresion lambda toma la tupla y ordena según el segundo elemento de la tupla
# el metodo sort MUTA la lista
Con_prom_autopista_clase.sort(key= lambda x: x[1])

print('Consumos según clase:', Con_prom_autopista_clase)