# %%
"""
Created on Sat Feb 10 13:44:53 2024

@author: juan_
"""

# %%
"""
# 4 Conocimientos sobre librerías de visualización estática

## 1. Objetivo

Para enriquecer el análisis de Oilst y hacerlo más accesible al público no especializado, el equipo de `Brasil BI Consulting` decidió crear visualizaciones estáticas, es decir sin animaciones o filtros interactivos, a partir de los datos de las órdenes de los clientes.

Con ello en mente, el objetivo de la presente sección será trabajar con la librería `Seaborn` de Python (https://seaborn.pydata.org) para abundar en el análisis correspondiente. Seaborn es una librería para implementar gráficos estadísticos en Python, que se basa en `matplotlib` y se integra estrechamente con las estructuras de datos de `pandas`.

"""

# %%
"""
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

# %%

oilst = read_data("results/1")


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
B. Programa que cree una visualización de la matriz de correlación de `delta_days` 
junto con el resto de variables numéricas, para las órdenes en las que se concretó su entrega. 
Este script se denominará `3_b_correlation_matrix_complete_orders.py` y su resultado será una 
figura llamada `3_b_correlation_matrix_complete_orders.png`.
"""

# %%
"""
### Análsis de correlación lineal

La correlación lineal es una herramienta que se utiliza para analizar la relación lineal entre varias variables. 
En esencia, lo que hace es medir cuánto se parecen dos variables y cuánto se influyen mutuamente.

Formalmente, se denomina **Coeficiente de correlación de Pearson** y se calcula como un coeficiente entre 
dos variables numéricas, que oscila entre entre -1 y 1, donde -1 significa que las dos variables están 
completamente inversamente relacionadas (si una aumenta, la otra disminuye) y 1 significa que las 
dos variables están completamente relacionadas (si una aumenta, la otra también lo hace). En el caso cercano a cero, 
esto significa que no hay correlacion de tipo lineal entre estas


Si queremos detectar que una variable tiene correlación lineal con otrra, su coeficiente de correlación debe 
aproximarse lo más posible a -1 o 1. 

Debemos mencionar que la existenciade correlación lineal entre dos variables no implica que una cause a la otra; 
por ejemplo, la cantidad de helados que se venden en verano aumenta a la vez que la cantidad de quemaduras en 
 piel en la misma época, sin que alguna de ellas sea la causa de la otra. Sin embargo la correlación alta es un 
 elemento deseable en cualquier análisis exploratorio para comenzar a indagar como es que un fenómeno cambia ante 
 diversos factores. 


"""

# %%

# lista de variables numericas de ventas, productos, retrasos y distancia al centro de distribucion
numerical_variables = ['total_sales', 'total_products',
                       'distance_distribution_center', 'delta_days']
# calculo de matriz de correlacion de las ordenes completadas
data = delivered[numerical_variables
                 ].corr().round(4)

print(data)

# %%

# Especifica el tamaño de la figura
plt.figure(figsize=(15, 10))

svm = sns.heatmap(
    data,
    cmap="coolwarm",
    annot=True).set(
        title='Matriz de correlación de las órdenes completadas'
)

plt.savefig('results/3/3_b_correlation_matrix_complete_orders.png', dpi=600)

# plt.show()

# %%

fig = px.imshow(data, text_auto=True, color_continuous_scale='RdBu_r')

# Establecer el titulo
fig.update_layout(
    title="Matriz de correlación de las órdenes completadas")

# Guardar el plot
fig.write_html("results/3/3_b_correlation_matrix_complete_orders.html")

# Display the plot
# fig.show()


# %%

# Filtrar las ordenes con retrazo prolongado
filter = "delay_status == 'long_delay'"

# calculo de matriz de correlacion de las ordenes completadas con retrazos prolongaos
data = delivered.query(filter)[
    numerical_variables
].corr().round(4)

print(data)
# %%

# Especifica el tamaño de la figura
plt.figure(figsize=(15, 10))

svm = sns.heatmap(
    data,
    cmap="coolwarm",
    annot=True).set(
        title='Matriz de correlación de las órdenes completadas con retrazo prolongado'
)

plt.savefig(
    'results/3/3_b_correlation_matrix_complete_orders_long_delay.png', dpi=600)

# plt.show()

# %%

fig = px.imshow(data,
                text_auto=True,
                color_continuous_scale='RdBu_r')

# Establecer el titulo
fig.update_layout(
    title="Matriz de correlación de las órdenes completadas con retrazo prolongado")

# Guardar el plot
fig.write_html(
    "results/3/3_b_correlation_matrix_complete_orders_long_delay.html")

# Display the plot
# fig.show()
