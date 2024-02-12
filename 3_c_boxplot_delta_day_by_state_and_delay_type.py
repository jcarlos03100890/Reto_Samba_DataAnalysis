# -*- coding: utf-8 -*-
"""
Created on Sat Feb 10 14:24:47 2024

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


# Libreria de visualización


import warnings
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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
"""

# %%
# Condicion  lógica para filtrar (solo ordenes entregadas)
delivered_filter = "order_status  == 'delivered'"

delivered = oilst.query(delivered_filter)

# %%
"""
C. Script que construya una visualización los diferentes diagramas de cajas de la `delta_days` 
a lo largo de los estados de Brasil. Dicha visualización deberá segmentarse o aperturarse de 
forma que permita revisar en una misma figura como varian los diagramas de caja también para 
órdenes que tuvieron diferentes valores del campo `delay_status` a lo largo de los estados brasileños. 
Dicho script se llamarán `3_c_boxplot_delta_day_by_state_and_delay_type.py` y la figura resultante 
del mismo se denominará `3_c_boxplot_delta_day_by_state_and_delay_type.png`. 

Hint: Revisar la documentación de `.catplot`
"""

# %%
"""
En esta sección se mostrarán visualizaciones de los tiempos promedios por entrega en cada estado. 
Para ello se estimará el valor medio de los retrazos.
"""
# %%

# %%
g = sns.catplot(
    data=delivered.sort_values(['state_name']),
    x="delta_days", y='delay_status',
    kind="box",
    col='state_name', palette="Set1",
    orient="h", sharex=False, margin_titles=True,
    height=2, aspect=4, col_wrap=3
)

g.set(xlabel="Delta Days", ylabel="")

g.set_titles(col_template="\nEstado: {col_name}")

for ax in g.axes.flat:
    ax.xaxis.set_major_formatter('{x:.0f}')

g.fig.subplots_adjust(top=0.95, bottom=0.1, hspace=0.75, wspace=0.125)

# add title to the whole plot
g.fig.suptitle(
    'Diagrama de cajas de delta days por delay status de cada estado ')

g.savefig(
    'results/3/3_c_boxplot_delta_day_by_state_and_delay_type.png', dpi=600)



# %%
states = delivered['state_name'].dropna().unique()

i = 1
ii=1
jj=1
fig = make_subplots(rows=10, cols=3)

for state in states:

    print(i, "-", state)

    current_state = delivered[delivered['state_name'] == state]
    
    fig.append_trace(go.Box(x=current_state['delta_days'],
                            y=current_state['delay_status'],
                            name=state, 
                            ), row=ii, col=jj)

    i = i+1
    jj = jj+1
    
    if i == 4:
        ii= 2
        jj=1
    if i == 7:
        ii= 3
        jj=1
    if i == 10:
        ii= 4
        jj=1
    if i == 13:
        ii= 5
        jj=1
    if i == 16:
        ii= 6
        jj=1
    if i == 19:
        ii= 7
        jj=1
    if i == 22:
        ii= 8
        jj=1
    if i == 25:
        ii= 9
        jj=1
    
fig.update_layout(
    
    boxmode='group',title="Diagrama de cajas de delta days por delay status de cada estado",height=3000
)


fig.update_traces(orientation='h')  # horizontal box plots

fig.write_html(
    "results/3/3_c_boxplot_delta_day_by_state_and_delay_type.html")

#fig.show()
