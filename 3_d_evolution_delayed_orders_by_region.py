# %%
"""
Created on Sun Feb 11 11:27:55 2024

@author: juan_
"""

# %%
"""
# Tema 5. Conocimientos sobre librerías de visualización interactiva

## 1. Objetivo

Con el objeto de ampliar el análisis de Oilst y más interactivo hacia el público al que va dirigido, el equipo de `Brasil BI Consulting` decidió crear visualizaciones interactiva, es decir que incluyen animaciones o filtros interactivos, a partir de los datos de las órdenes de los clientes y algunos datos geográficos.

Con ello en mente, el objetivo de la presente sección será trabajar con el módulo `Plotly Express` de la librería `Plotly` de Python (https://plotly.com/python/). Ésta es una librería para realizar gráficos interactivos en Python de amplio espectro.

"""

# %%
"""
## 2. Librerias de trabajo
"""

# %%

import pandas as pd


# Libreria de visualización
import plotly.express as px

from funciones import get_data_region, read_data

import warnings
warnings.filterwarnings('ignore')


# %%
"""
## 3. Lectura de datos

 Leeremos los datos, usando una funcion previamente definida
 
"""

# %%


oilst = read_data("results/1")

# %%
"""
Ya que en este sctipt realizaremos un analysis por region, debemos agrear la region a los datos procesados de Olist
"""

# %%

regions = get_data_region("inputs")

# Agregamos la columna de región para los estadios de Brasil
oilst = oilst.merge(regions[['abbreviation', 'region']],
                    on='abbreviation', how='left')

oilst.info()

# %%
"""
A su vez transformaremos el nombre de la ciudades a un formato de título, es decir, las primeras letras de las palabras estarán en mayúsculas.
"""

# %%

oilst['geolocation_city'] = oilst['geolocation_city'].str.title()

# %%
"""
En este análisis únicamente nos interesarán las órdenes completadas, 
así que tenemos que obtener el subconjunto de datos correspondiente. 
"""

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)

delivered = oilst.query("order_status  == 'delivered'")

# %%
"""
Programa que cree una visualización interactiva de un gráfico de barras que por cada mes y años, 
donde la altura de cada barra cuente la cantidad de órdenes con retraso prolongado que sucedieron 
en dicho periodo. Además, dentro cada barra se deberá tener un desglose de 
la cantidad de órdenes que tuvieron retraso en cada uno de los periodos.

**Hints:** 
1) Primero realize conteo agrupados de las órdenes completadas mediante las variables 
`delay_status`,`year_month` y `geolocation_state`, 
2) después explore la documentación de la utilidad `.bar` de Plotly para construir la visualización.
"""

# %%
# Calcula la cantidad de ordenes en el tiempo por region
orders_time_delay_status = delivered.groupby(
    ['year_month', 'delay_status', 'region']).aggregate(
        {'order_id': 'count', }
).reset_index().rename(
    columns={'order_id': 'orders', }
)

# Crea una variable temporal en texto para graficar
orders_time_delay_status['period'] = orders_time_delay_status['year_month'].astype(
    str)

# Convertir a date el año y mes
orders_time_delay_status['year_month'] = pd.to_datetime(
    orders_time_delay_status['year_month'])

# Order por año y mes para graficar
orders_time_delay_status = orders_time_delay_status.sort_values(
    by='year_month')

# %%
# Crea la visualizacion
fig = px.bar(
    orders_time_delay_status.query(
        "delay_status == 'long_delay'"
    ),
    x="period",
    y="orders",
    color='region',
    text_auto=True,
    facet_row="delay_status",
    title='Evolicion del Número de órdenes con retraso prolongado por Region'
)
# Guardar la figura en un archivo html
fig.write_html(
    "results/3/3_d_evolution_delayed_orders_by_region.html")
# Muestra la figura
#fig.show()
