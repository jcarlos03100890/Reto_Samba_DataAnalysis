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


import pandas as pd
import warnings
from funciones import read_data
warnings.filterwarnings('ignore')

# Libreria de visualización
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
# %%
"""
## 3. Lectura de datos

 Leeremos los datos, usando una funcion previamente definida
"""

oilst = read_data("results/1")

oilst.info()

# %%
"""
En este análisis únicamente nos interesarán las órdenes completadas, 
así que tenemos que obtener el subconjunto de datos correspondiente
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
En este análisis únicamente nos interesa identificar la cantidad conteos, 
cuantas órdenes que existieron por cantidad de productos dentro de la orden 
y el tipo de retraso de las categorías `delay_status`.
"""

# %%

results = pd.crosstab(
    oilst['total_products'],
    oilst['delay_status'],
    margins=True
).sort_values(['long_delay'])


results.to_csv(
    # nombre del archivo
    'results/2/count_orders_basket_size_by_delay_status.csv')

print(results)

# %%
"""
Despues de analizar la cantidad de ordenes por cantidad de productos por tipo de retrazo, 
una tabla no nos dice mucho, asi que creamos esta grafica con los primeros resultados
Donde observamos que la mayoria de las ordenes consisten uno o dos productos
"""
# %%

orders_basket_size_by_delay_status = delivered.groupby(
    ['total_products', 'delay_status']).aggregate(
        {'order_id': 'count', }
).reset_index().rename(
    columns={'order_id': 'orders', }
)

orders_basket_size_by_delay_status

# %%

ax=sns.barplot(data = orders_basket_size_by_delay_status.query("total_products < 7"),
                 x = "total_products", 
                 y = "orders", 
                 hue = "delay_status")
ax.set_title('Conteo de ordenes por cantidad de productos por tipo de retrazo')
ax.set_xlabel('Total de Productos')
ax.set_ylabel('Numero de Ordenes')
plt.savefig('results/2/count_orders_basket_size_by_delay_status.png')
#plt.show()


# %%
# Create the grouped bar chart
fig = px.bar(orders_basket_size_by_delay_status.query("total_products < 7"), 
             x="total_products", 
             y="orders", 
             color="delay_status", 
             barmode='group',
             labels={'total_products':'Total de Productos','orders':'Numero de Ordenes','delay_status':'Tipo de Retrazo'})

fig.update_layout(title="Conteo de ordenes por cantidad de productos por tipo de retrazo")

fig.write_html("results/2/count_orders_basket_size_by_delay_status.html")

#fig.show()