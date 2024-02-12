# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 12:47:36 2024

@author: juan_
"""

# %%
"""
# 4 Conocimientos sobre librerías de visualización estática

## 1. Objetivo

Para enriquecer el análisis de Oilst y hacerlo más accesible al público no especializado, el equipo de `Brasil BI Consulting` decidió crear visualizaciones estáticas, es decir sin animaciones o filtros interactivos, a partir de los datos de las órdenes de los clientes.

Con ello en mente, el objetivo de la presente sección será trabajar con la librería `Seaborn` de Python (https://seaborn.pydata.org) para abundar en el análisis correspondiente. Seaborn es una librería para implementar gráficos estadísticos en Python, que se basa en `matplotlib` y se integra estrechamente con las estructuras de datos de `pandas`.

## 2. Librerias de trabajo
"""

# %%


import warnings

# Libreria de visualización
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

from funciones import read_data


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
La utilidad de pandas que no servirá para dicho propósito es `.query()` 
(https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.query.html). 
En su interior debemos espeficar como texto una cadena lógica que indique que 
valor de una columna queremos obtener (`"order_status  == 'delivered' "`)
"""

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered_filter = "order_status  == 'delivered'"

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

delivered.info()

# %%
"""
Realizar un script que construya una visualización que permita comparar los histogramas de las ventas 
de órdenes completas que tuvieron retrazos moderados y prolongados.
"""

# %%
### 4.2 Uso de la variable `hue`

"""
Como se ha mencionado antes, las implementaciones de Seaborn son muy flexibles y permite añadir segmentaciones de una visualización usando los mismos códigos que antes, pero segmentando por una variable categórica especificada en la variable `hue='nombre_variable_categórica'`.

A continuación se presentan algunos ejemplos de visualizaciones ya implementadas:

**Histogramas**
"""

# %%

# Especifica el tamaño de la figura
plt.figure(figsize = (15,6))

# Genera el histograma
sns.histplot(
    data=delivered.query("delay_status != 'on_time'"),
    x="total_sales",
    hue="delay_status",
    bins="auto"    
    ).set(
        title='Histograma de frecuencias de la diferencia de la variable total_sales \n por órdenes completas que tuvieron retrazos moderados y prolongados',
        xlabel='Total de Ventas', 
        ylabel='Frecuencia'
        )

# Save the plot
plt.savefig('results/3/3_a_histogram_sales_short_long_delays.png')

# Display the plot
#plt.show()

# %%

# Genera el histograma
fig = px.histogram(
    delivered.query("delay_status != 'on_time'"), 
    x="total_sales", 
    color="delay_status", 
    labels={'delay_status':'Tipo de Retrazo','total_sales':'Total de Ventas','count':'# Ocurrencias'},
    nbins=310)

# Establecer el titulo
fig.update_layout(title="Histograma de frecuencias de la diferencia de la variable total_sales por órdenes completas que tuvieron retrazos moderados y prolongados")

# Update the xaxis label
fig.update_xaxes(title='Total de Ventas')

# Update the xaxis label
fig.update_yaxes(title='# Ocurrencias')


# Guardar el histograma
fig.write_html("results/3/3_a_histogram_sales_short_long_delays.html")

# Display the plot
#fig.show()