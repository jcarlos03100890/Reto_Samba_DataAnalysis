# %%
"""
Created on Fri Feb  9 21:59:04 2024

@author: juan_
"""

# %%
"""
# Tema 2. Conceptos de estadística y probabilidad usando Python

## 1. Objetivo

Ahora que se ha integrado la data de Oilst, el equipo de `Brasil BI Consulting` 
puede analizar de los retrazos las órdenes de los cliente, así el objetivo de esta 
sección será comenzar dicho análisis incorporando elementos de estadística y probabilidad usando Python.
"""

# %%
"""
## 2. Librerías de trabajo
"""

# %%

import warnings

from funciones import read_data

# Libreria de visualización
import matplotlib.pyplot as plt


warnings.filterwarnings('ignore')


# %%
"""
## 3. Lectura de datos

 Leeremos los datos, usando una funcion previamente definida
 
"""

oilst = read_data("results/1")


# %%
"""
En este análisis únicamente nos interesarán las órdenes completadas, 
así que tenemos que obtener el subconjunto de datos correspondiente. 
"""

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered = oilst.query("order_status  == 'delivered'")

delivered.info()
# %%
"""
C.Programa que construya el histograma de frecuencias de la variable `total_sales`, 
junto con la el promedio intervalos que define la regla empírica débil para encontrar el 88.88% 
de los datos alrededor del promedio, restringiendo el análisis las órdenes que tienen status completo.
 El resultado de este script deberá ser una figura denominada `histogram_sales_long_delay.png`.
"""


# %%

"""

## ¿Qué es un histograma de frecuencias?
Un histograma de frecuencias es una representación gráfica de un conjunto de datos que muestra 
la frecuencia con la que se presenta cada valor.

Este gráfico está formada por barras verticales construidas sobre una línea recta base (normalmente horizontal) 
delimitada por los intervalos de la variable evaluada. Los intervalos o clases corresponden a los de una 
tabla de distribución de frecuencias. La altura de cada barra es proporcional al número de observaciones 
que hay en ese intervalo.

¿Cómo hacer un histograma de frecuencias?
Ya sea que quieras realizar un histograma a mano o utilizando alguna herramienta informática, es importante conocer los pasos que debes seguir para elaborarlos:

* Determinar el número de intervalos o clases.
* Calcular la amplitud del intervalo.
* Calcular el número total de ocurrencias para intervalo / rango.
* Dibujar los ejes de intervalos y de frecuencias.
* Trazar las barras.

Mendez, A. (2022, April 20). Histograma de Frecuencias – La guía completa. Plan De Mejora. 
Retrieved February 11, 2024, from https://www.plandemejora.com/histograma-de-frecuencias/


Tomando como base la definicion de Mendez(2022), para realizar un histograma de frecuencias, 
primero necesitamos deteminar:
    * Determinar el número de intervalos o clases.
    * Calcular la amplitud del intervalo.

"""

# %%
"""
Paso 1: Determinar el número de intervalos o clases

Para determinar el número de intervalos o clases usaremos la raiz cuadrada de los datos
"""
# %%
# Obtenemos eltotal de datos
tota_datos=delivered['order_id'].count()

# Ahora calculamos la raiz cuadrada
from math import sqrt

intervalos = sqrt(tota_datos)

print("Intervalos:",round(intervalos,0))

# %%
"""
Paso 2: Calcular la amplitud del intervalo.
Una vez determinada la cantidad de intervalos, calculamos la amplitud del intervalo (w) con la siguiente expresión:
         (Numero Mayor - Numero Menor)
   W=   --------------------------------
              Numero de intervalos

Ya que deseamos saber el hitogramas de total_sales, es decir del total de ventas usaremos esta columna    
"""

# %%
#Valor maximo de ventas
delivered['total_sales'].max()
#Valor minimo de ventas
delivered['total_sales'].min()

#Calculamos la amplitud del intervalo

w = (delivered['total_sales'].max() - delivered['total_sales'].min()) / intervalos

print("La amplitud del intervalo es:",w)

# %%
"""
Otra manera de determinar los intervalos asi como la amplitud es usar numpy
"""

# %%
import numpy as np
# Calculate the optimal number of bins using the Freedman-Diaconis rule

bins = np.histogram_bin_edges(delivered['total_sales'], 'auto')



# %%
# figura y eje de la figura
fig, ax = plt.subplots(figsize=(10, 5))

# numero de intervalos para conteos
n_bins = 310

# creacion del objeto historgama
n, bins, patches = ax.hist(
    delivered['total_sales'], 
    n_bins
)

ax.set_title('Fig.1 Histograma de frequencias de la variable total_sales')
ax.set_xlabel('Relacion entre el numero de ventas y el total vendido')
ax.set_ylabel('Frecuencia')

fig.savefig('results/2/histogram_sales_long_delay_A.png')

# plt.show()


# %%
# figura y eje de la figura
fig, ax = plt.subplots(figsize=(10, 5))

# numero de intervalos para conteos
n_bins = 310

# creacion del objeto historgama
n, bins, patches = ax.hist(
    delivered['total_sales'],
    n_bins
)

ax.set_title(
    'Fig.2 Histograma de frequencias de total_sales y regla empírica débil')
ax.set_xlabel('Relacion entre el numero de ventas y el total vendido')
ax.set_ylabel('Frecuencia')

# Agrega la media y las regiones de la regla empírica débil
# Linea para la media
plt.axvline(
    oilst['total_sales'].mean(),
    color='r',
    linestyle='dashed',
    linewidth=3)

# Linea para la media + 3 veces la desv. estandar
plt.axvline(
    oilst['total_sales'].mean() + 3*oilst['total_sales'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

# Linea para la media - 3 veces la desv. estandar
plt.axvline(
    oilst['total_sales'].mean() - 3*oilst['total_sales'].std(),
    color='y',
    linestyle='dashed',
    linewidth=2)

# limites de la figura
min_ylim, max_ylim = plt.ylim()

# Etiquetas
plt.text(
    delivered['total_sales'].mean()*1.1,
    max_ylim*0.9,
    'Promedio: {:.2f}'.format(oilst['total_sales'].mean())
)

fig.savefig('results/2/histogram_sales_long_delay.png')

# plt.show()
