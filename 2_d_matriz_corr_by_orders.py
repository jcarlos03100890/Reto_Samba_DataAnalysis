# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 23:23:53 2024

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

import warnings

from funciones import read_data

# Libreria de visualización
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns

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

delivered.info()

# %%
"""
# Calcula la matriz de correlación entre las variables `total_sales`, `total_products`, `delta_days` y 
`distance_distribution_center` para órdenes completadas que cuya fecha de entrega sobrepasa 
los 10 días de la fecha estimada para la entrega.

"""

# %%
"""
### Análsis de correlación lineal

La correlación lineal es una herramienta que se utiliza para analizar la relación lineal entre varias variables. En esencia, lo que hace es medir cuánto se parecen dos variables y cuánto se influyen mutuamente.

Formalmente, se denomina **Coeficiente de correlación de Pearson** y se calcula como un coeficiente entre dos variables numéricas, que oscila entre entre -1 y 1, donde -1 significa que las dos variables están completamente inversamente relacionadas (si una aumenta, la otra disminuye) y 1 significa que las dos variables están completamente relacionadas (si una aumenta, la otra también lo hace). En el caso cercano a cero, esto significa que no hay correlacion de tipo lineal entre estas

Si queremos detectar que una variable tiene correlación lineal con otrra, su coeficiente de correlación debe aproximarse lo más posible a -1 o 1. 

Debemos mencionar que la existenciade correlación lineal entre dos variables no implica que una cause a la otra; por ejemplo, la cantidad de helados que se venden en verano aumenta a la vez que la cantidad de quemaduras en la piel en la misma época, sin que alguna de ellas sea la causa de la otra. Sin embargo la correlación alta es un elemento deseable en cualquier análisis exploratorio para comenzar a indagar como es que un fenómeno cambia ante diversos factores. 


"""

# %%
"""
Ahora veremos como cambia la distancia de los domicilios de los clientes a su centro de distribución más cercano (`distance_distribution_center`) con respecto al estatus del tiempo de entrega. Primero, podemos revisar los estadísticos básicos:
"""

# %%
delivered.groupby(['delay_status'])['distance_distribution_center'].describe()

# %%
"""
Ahora usaremos el métod `.corr` de pandas sobre las variables numéricas `total_sales`, `total_products`, `distance_distribution_center`y `delta_days`.
"""

# %%
delivered[
    ['total_sales', 'total_products', 'distance_distribution_center', 'delta_days']
    ].corr().round(4)

# %%
delivered.describe()

# %%
"""
En esta tabla no se aprecia correlación entre las variables. 
Repitamos los cálculos pero en el caso de que ordenes entregas, que presentaron retrazos prolongados. 

Script que calcula la matriz de correlación entre las variables `total_sales`, `total_products`, 
`delta_days` y `distance_distribution_center` para órdenes completadas que cuya fecha 
de entrega sobrepasa los 10 días de la fecha estimada para la entrega
"""

# %%
# Completa el codigo provisto
filter = 'delta_days > 10' # filtro para definir ordenes con retraso prolongado

# lista de variables numericas de ventas, productos, retrasos y distancia al centro de distribucion
numerical_variables = ['total_sales', 'total_products', 'distance_distribution_center', 'delta_days']

# calculo de matriz de correlacion
data=delivered.query(filter)[
    numerical_variables
    ].corr().round(4)

print(data)

data.to_csv(
    # nombre del archivo
    'results/2/matriz_corr_by_orders.csv',
    # flag para no escribir el indice del dataframe al csv
    index=False
)

# %%

# Especifica el tamaño de la figura
plt.figure(figsize = (15,10))

svm = sns.heatmap(
    data,
    cmap="coolwarm",
    annot=True).set(
        title='Matriz de correlación para órdenes completadas con retrazo mayor a 10 dias'
        )

plt.savefig('results/2/matriz_corr_by_orders.png',dpi=600)

#plt.show()

# %%

fig = px.imshow(data,text_auto=True,color_continuous_scale='RdBu_r')

# Establecer el titulo
fig.update_layout(title="Matriz de correlación para órdenes completadas con retrazo mayor a 10 dias")

# Guardar el plot
fig.write_html("results/2/matriz_corr_by_orders.html")

# Display the plot
#fig.show()