# %%
"""
Created on Sun Feb 11 13:00:09 2024

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

# Libreria de visualización
import plotly.express as px
from funciones import read_data, get_geo_data

import warnings
warnings.filterwarnings('ignore')


# %%
"""
## 3. Lectura de datos

 Leeremos los datos, usando una funcion previamente definida
 
"""

oilst = read_data("results/1")

# %%
"""
Además de la data procesada, leeremos el archivo **brasil_geodata.json**, 
el cual es información geográfica de los estados de Brasil que será útil para nuestro análisis. 
Dicho archivo es una versión procesada del archivo `Brasil.json` de Kaggle 
(https://www.kaggle.com/code/kerneler/starter-brazil-states-geojson-ca176cdb-a).
"""

# %%

geojson = get_geo_data("inputs")

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
### Visualizaciones Geográficas

Uno de lo puntos más interesantes de Ploty es la posibilidad de realizar gráficos completos usando data de 
otros sistemas, como los de origen geográfico.

En esta sección se mostrarán visualizaciones de casos de órdenes con retrazos prolongados que ocurrieron en cada estado. 
Para ello se contaran las ordenes por tipo de retrazo, para despues filtrar los retrazos prolongados.

"""

# %%
"""
E. Script que construya un mapa interactivo que indique con una escala de colores a la cantidad 
de casos de órdenes con retrazos prolongados que ocurrieron en cada estado. 
Dicho script se llamará `3_e_map_long_delays_by_state.py` y la imagen interactiva deberá tener 
el nombre `3_e_map_long_delays_by_state.html`.
"""

# %%

# Calcula el numero de ordenes con retrazos en el estado

delay_by_state = delivered.groupby(
    ['state_name', 'geolocation_state', 'delay_status']).aggregate(
        {'order_id': 'count', }
).reset_index().rename(
    columns={'order_id': 'orders', }
)


delay_by_state = delay_by_state.sort_values(['orders'], ascending=False)

# %%
"""
Esta información se puede pasar a la función `.choropleth` de Plotly para construir un mapa. 
Cabe destaca que el archivo `geojson` es un archivo externo que contiene información de 
un sistema cartográfico que `Ploty` puede leer e interpretar para cronstruir la visualización:
"""

# %%

# Crear figura con el mapa de Brasil y el choropleth
fig = px.choropleth(
    data_frame=delay_by_state.query(
        "delay_status == 'long_delay'"
    ),
    geojson=geojson,
    featureidkey='properties.UF',
    locations='geolocation_state',
    color='orders',
    color_continuous_scale="Reds",
    scope='south america',
    labels={'orders': 'Ordenes',
            'geolocation_state':'Estado',
            'delay_status':'Tipo de Retrazo'},
    width=800,
    height=800,
    title="Mapa de ordenes con retrazo prolongado a nivel estatal",
    hover_name='state_name',
    hover_data=['delay_status']
)

# Actualizar diseño de la figura
fig.update_geos(
    showcountries=False,
    showcoastlines=True,
    showland=True,
    fitbounds='locations',
    visible=True
)


# Guardar la figura en un archivo html
fig.write_html(
    "results/3/3_e_map_long_delays_by_state.html")

# Mostrar figura
#fig.show()
