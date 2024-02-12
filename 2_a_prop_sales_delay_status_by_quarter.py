# -*- coding: utf-8 -*-
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

## 2. Librerías de trabajo
"""

# %%

import matplotlib.pyplot as plt
import warnings
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from funciones import read_data


warnings.filterwarnings('ignore')


# %%
"""
## 3. Lectura de datos

 Leeremos los datos, indicando a Python donde se encuentra la carpeta que se aloja los datos 
 y los nombres de los archivos relevantes para el análisis.
"""

oilst = read_data("results/1")


# %%
"""
En este análisis únicamente nos interesarán las órdenes completadas, 
así que tenemos que obtener el subconjunto de datos correspondiente. 
La utilidad de pandas que no servirá para dicho propósito es `.query()` 
(https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html). 
En su interior debemos espeficar como texto una cadena lógica que indique que 
valor de una columna queremos obtener (`"order_status  == 'delivered' "`)
"""

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered_filter = "order_status  == 'delivered' "

delivered = oilst.query(delivered_filter)

# %%
"""
Ahora podemos ver una muestra de este nuevo subconjunto de datos:
"""

# %%
delivered.sample(5)

# %%
"""
La cantidad de renglones y columnas totales en este dataframe se puede obtener con el método `.shape`
"""

# %%
delivered.shape

# %%
"""
Script que calcule la proporción que han representado las ventas de órdenes completas de Oilst dentro 
de los categorías de `delay_status` y a los largo de los trimestres de 2016 a 2018. 
El resultado de este script deberá ser un tabla denominada `prop_sales_delay_status_by_quarte.csv`.
"""

# %%
"""
Podemos analizar la proporción de las ventas que provienen de retrasos prolongadosa 
lo largo de los diferentes trimestres. Primero construyamos la pivot tables de ventas 
segmentada por `delay_status` a lo largo de `quarter`
"""

# %%
# Creamos una pivot table con la suma de las ventas agrupadas por tipo retrazo por trimestre, 

data=delivered.pivot_table(
    index='delay_status',
    columns='quarter',
    values='total_sales',
    aggfunc='sum',
    fill_value=0
)

print(data)

# %%
"""
A la tabla anterior, se le puede aplicar un función que calcule las proporciones 
dentro de ventas dentro de cada categoría:
"""

# %%
# Aplica la función lambda x:   x / float(x.sum() sobre
# renglones (axis=0)

data = delivered.pivot_table(
    index='delay_status',
    columns='quarter',
    values='total_sales',
    aggfunc='sum',
    # margins=True,
    fill_value=0
).apply(lambda x:   x / float(x.sum()), axis=0).round(2)

print(data)

data.to_csv(
    # nombre del archivo
    'results/2/prop_sales_delay_status_by_quarter.csv',
    # flag para no escribir el indice del dataframe al csv
    index=False
)



# %%
"""
Hasta aqui completamos el objetivo del presente script, crear una table que 
muestre las proporciones de ventas por tipo de retrazo a lo largo de los trimestres.

Sin embargo, para una mejor lectura, crearemos una visualizacion estatica y una dinamica 
para mostrar los datos de total de ventas por tipo de retrazo a lo largo de los trimestres.
"""
# %%
# Creamos una pivot table con la suma de las ventas agrupadas por tipo retrazo por trimestre, 

data=delivered.pivot_table(
    index='delay_status',
    columns='quarter',
    values='total_sales',
    aggfunc='sum',
    fill_value=0
)

print(data)


# %%

#Creamos una visualziacion estatica
# show data
fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(10, 10))

# unpack all the axes subplots
axe = axs.ravel()

for i, col in enumerate(data.columns):
    data[col].plot.pie(ax=axe[i], label="")
    axe[i].set_title(col)

plt.tight_layout()
plt.savefig('results/2/2_a_Pie-prop_sales_delay_status_by_quarter.png')
#plt.show()

# %%
"""
Auqnue podemos ver la informacion, no queda muy claro ni la proporcion ni el toal de ventas,
por esto creamos una visualizacion dinamica que muestre un poco mas de esta informacion
"""

# %%

# Pie chart using px

fig = make_subplots(rows=3, cols=3, specs=[[{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
                                           [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}],
                                           [{"type": "pie"}, {"type": "pie"}, {"type": "pie"}]])

ii=1
jj=1
    

labels=['Long Delay','On time','Short Delay']
for i, col in enumerate(data.columns):
    
    if i==3:
        ii= 1
        jj=2
    if i==6:
        ii= 1
        jj=3
  
    fig.add_trace(go.Pie(
        labels=labels,
        values=data[col],
        marker=dict(colors=['red', 'green', 'blue']),
        title=col,
        hole=0.5), row=jj, col=ii)
    
    ii=ii+1

fig.update_layout(title="Proporción de ventas por `delay_status` por quarter")

fig.write_html("results/2/2_a_Pie-prop_sales_delay_status_by_quarter.html")
