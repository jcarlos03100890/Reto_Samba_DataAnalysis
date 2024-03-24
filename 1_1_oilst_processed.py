# %%
"""
Created on Sun Jan 28 21:02:51 2024

@author: juan_
"""

# %%
"""
# Tema 1: Conocimientos sobre Pandas

## 1. Objetivo

Procesar en Python la información entregada por el equipo de Ingeniería de datos de Oilst de forma funcional para el análisis de los retrasos en las órdenes de los clientes.
"""

# %%
"""
Este documento se desarrollarán scripts en Python que permitan procesar la  la información de Oilst
para realizar posteriormente el análisis de sus datos
"""

# %%
"""
## 2. Librerias de trabajo.

Utilizaremos las siguientes librerias de python para procesar los archivos y crear un archivo con datos consolidados
"""

# %%

import warnings
import pandas as pd
import numpy as np
import os
from funciones import set_data_path,check_results_folder
warnings.filterwarnings('ignore')

# %%
"""
## 3. Lectura de datos

Primero nos encargaremos de leer los datos, indicando a Python donde se encuentra
la carpeta que contiene los datos y los nombres de los archivos relevantes para el análisis.
"""

# %%
#  Indicamos la ruta a la carpeta de los archivos a procesarse de los datos del E-commerce

# Ya que los archivos se encuentran en el mismo folder solo en la carpeta inputs,
# utilizamos la funcion set_data_path para identificar la carpeta donde estan los archivos a trabajar

# Set the file path
DATA_PATH = set_data_path("inputs")


# %%
"""
Ahora procederemos a definir variables que indiquen el nombre de los archivos junto con
su extensión (por ejemplo, `.csv`, `.json` u otra).
"""

# %%
FILE_CUSTOMERS = 'olist_customers_dataset.xlsx'
FILE_GEOLOCATIONS = 'olist_geolocation_dataset.csv'

# completa los nombres del resto de los archivos con su extesion (ejemplo .csv) ...
FILE_ITEMS = 'olist_order_items_dataset.csv'
FILE_PAYMENTS = 'olist_order_payments_dataset.csv'
FILE_ORDERS = 'olist_orders_dataset.csv'
FILE_STATES_ABBREVIATIONS = 'states_abbreviations.json'

# %%
"""
USaremos de la utilidad `os.path.join` de Python que indicar la ruta de
 donde se ubican archivos, así Pandas encontrá los archivos de datos.
"""

# %%
# Leemos con pandas FILE_GEOLOCATIONS
geolocations = pd.read_csv(
    os.path.join(DATA_PATH, FILE_GEOLOCATIONS),
    dtype={'geolocation_zip_code_prefix': 'str'}
)

# %%
"""
### 3.1 Archivo olist_customers_dataset
"""

# %%

# Leemos los datos de los clientes
customers = pd.read_excel(
    os.path.join(DATA_PATH, FILE_CUSTOMERS),
    # Especificar el tipo de dato de customer_zip_code_prefix
    dtype={'customer_zip_code_prefix': 'str'}
)


# %%
"""
### 3.2 Archivo olist_order_items_dataset
"""

# %%
items = pd.read_csv(
    # Completa la ubicacion usando os.path.join, DATA_PATH y
    # el nombre del archivo FILE_ITEMS
    os.path.join(DATA_PATH, FILE_ITEMS))

# %%
"""
Como sabemos, este conjunto contiene datos de los productos que contiene cada orden. Por ello, para el análisis nos interesará saber cual es la cantidad de productos en cada orden y el precio total de las mismas.

Esto se puede calcular mediante agregaciones de Pandas (https://pandas.pydata.org/pandas-docs/version/0.23/generated/pandas.core.groupby.DataFrameGroupBy.agg.html), que basicamente nos permite hacer cálculos para un grupo en especial. En el ejemplo de inferior se muestra para cada `order_id` se cuenta la cantidad de productos (items) y el precio agregado de todos los artículos en las órdenes:
"""

# %%
items_agg = items.groupby(
    ['order_id']).agg(
        # conteo de producto
        {'order_item_id': 'count',
         # suma de los precios de los artículos
         'price': 'sum'}
).reset_index()

# %%
items_agg.head()

# %%
"""
Vamos a renombrar las columnas anteriores, para que sea más intuitivo su significado.
"""

# %%
# Nota: el parámetro inplace sobre escribe los cambios
# en el dataframe
items_agg.rename(
    columns={'order_item_id': 'total_products', 'price': 'total_sales'},
    inplace=True
)

# %%
items_agg

# %%
"""
Vamos a coninuar leyendo los archivos:
"""

# %%
"""
### 3.3 olist_order_payments_dataset
"""

# %%
payments = pd.read_csv(
    # Completa la ubicacion usando os.path.join, DATA_PATH y
    # el nombre del archivo correspondiente a los pagos
    os.path.join(DATA_PATH, FILE_PAYMENTS)
)

# %%
"""
### 3.4 states_abbreviations
"""

# %%
states_abbreviations = pd.read_json(
    # Completa la ubicacion usando os.path.join, DATA_PATH y
    # el nombre del archivo correspondiente a las abreviaciones de los estados
    os.path.join(DATA_PATH, FILE_STATES_ABBREVIATIONS)
)

# %%
"""
### 3.5 olist_orders_dataset
"""

# %%
orders = pd.read_csv(
    # Completa la ubicacion usando os.path.join, DATA_PATH y
    # el nombre del archivo correspondiente a las ordenes de Oislt
    os.path.join(DATA_PATH, FILE_ORDERS)
)

# %%
# Convierte a formato fecha completando los campos apropiados

# convierte order_purchase_timestamp
orders['order_purchase_timestamp'] = pd.to_datetime(
    orders['order_purchase_timestamp'], errors='coerce')
# order_approved_at
orders['order_approved_at'] = pd.to_datetime(
    orders['order_approved_at'], errors='coerce')

# order_delivered_carrier_date
orders['order_delivered_carrier_date'] = pd.to_datetime(
    orders['order_delivered_carrier_date'], errors='coerce')

# order_delivered_customer_date
orders['order_delivered_customer_date'] = pd.to_datetime(
    orders['order_delivered_customer_date'], errors='coerce')

# order_estimated_delivery_date
orders['order_estimated_delivery_date'] = pd.to_datetime(
    orders['order_estimated_delivery_date'], errors='coerce')


# %%
"""
Agregamos funciones auxilares derivadas de las fechas de las ordenes
"""

# %%
# Define una columna con el año en que sucedió la orden
orders['year'] = orders['order_purchase_timestamp'].dt.year

# Define una columna con el mes en que sucedió la orden
orders['month'] = orders['order_purchase_timestamp'].dt.month

# Define una columna con trimestre con el que paso la orden (ej. Q12018)
# https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.to_period.html
orders['quarter'] = orders['order_purchase_timestamp'].dt.to_period('Q')

# Define una columna con mes y año con el que paso la orden (ej. 02-2018)
# Hint: ¿que hace el metodo ...to_period('M')?
orders['year_month'] = orders['month'].astype(
    str).str.zfill(2) + "-" + orders['year'].astype(str)

# %%
"""
Por otro lado, también necesitamos identificar las órdenes que tuvieron retrasos prolongados.
Recordemos que de acuerdo a la documentación del `Anexo A`:

* Oilst notifica el usuario de cuando llegará su pedido con el valor de la columna `order_estimated_delivery_date`,
* Además la fecha real en que se llevó la entrega se encuentra en el campo `order_delivered_customer_date`

A continuación calcularemos distancia (en días) entre ambas fecha definiendo a la variable `delta_days`:
"""

# %%
# Nota: tenemos que realizar la conversion de
# segundos a días

orders['delta_days'] = (
    orders['order_delivered_customer_date'] -
    orders['order_estimated_delivery_date']
).dt.total_seconds() / 60 / 60 / 24

# %%
"""
En el contexto del problema, los valores de `delta_days` tiene el significado:

* Un valor negativo en `delta_days` significa que el pedido llego antes de lo esperado; es decir, no existió retraso.
* Un valor de `delta_days`, mayor a 0 días pero menor a 3 días, significa que es un retrazo aceptable, 
* Sin embargo, si `delta_days` es más grande que 3 días esto significa que tenemos un retrazo prolongado.

Crearemos una variable `delay_status` para indicar la discusión anterior usando el operador `where` de Numpy (https://towardsdatascience.com/creating-conditional-columns-on-pandas-with-numpy-select-and-where-methods-8ee6e2dbd5d5).

Esencialmente, el operador `where` de Numpy permite definir variables siguiendo reglas lógicas de manera condicional, similar al `if ... else ...` de Python:
"""

# %%
# Definimos 'delay_status'
orders['delay_status'] = np.where(
    orders['delta_days'] > 3, 'long_delay',
    np.where(orders['delta_days'] <= 0, 'on_time', 'short_delay')
)

# %%
"""
### 3.5 olist_geolocation_dataset

Aunque anteriormente hemos leído este archivo, debemos notar que contiene información redudante de muchos codigos postales, como en el caso del valor `24220`:

"""

# %%
geolocations.query("geolocation_zip_code_prefix == 24220")

# %%
"""
Para el análisis tendremos que eliminar esta duplicaciones. 
Esto se puede lograr con el método `drop_duplicates`
"""

# %%
unique_geolocations = geolocations.drop_duplicates(
    subset=['geolocation_zip_code_prefix']
)

# %%
"""
Como se aprecia a continuación, ahora el dataframe `unique_geolocations` corrige el error:
"""

# %%
unique_geolocations.query(
    "geolocation_zip_code_prefix == 24220"
)

# %%
"""
## 4. Procesamiento global

Ahora que hemos cargado a Pandas los datos del E-commerce, debemos **consolidar toda la información** en una sola tabla, lo que nos permitirá centralizar el análisis y hacer comparativos.

Para ello, nos proponemos lo siguiente:
    
1. A los datos de clientes le añadiremos los datos de geolocalización. **(Clientes + geolocalización)**
2. Tales datos se complementarán añadiendo los datos del nombre del estado de Brasil en que se localizan.
(**Clientes + geolocalización + nombre del estado donde viven**)
3. Posteriormente archivo de órdenes, agregaremos los datos del precio y cantidad de artículos.
**(Órdenes + total de artículos y precios)**
4. Finalmente, uniremos toda la información de los pasos 2 y 3 en una sola tabla.
"""

# %%
"""
### 4.1 Clientes + geolocalización
"""

# %%
customers_geolocation = customers.merge(
    unique_geolocations,
    left_on='customer_zip_code_prefix',
    right_on='geolocation_zip_code_prefix',
    how='left'
)

# %%
customers_geolocation.head()

# %%
"""
### 4.2 Clientes + geolocalización + nombre del estado donde viven

Ahora repetiremos un proceso análogo pero con los nombres del estado donde viven los customers
"""

# %%
# Une los dataframe customers_geolocation y states_abbreviations

customers_geolocation_estado = customers_geolocation.merge(
    states_abbreviations,
    left_on='geolocation_state',
    right_on='abbreviation',
    how='left'
)

# %%
customers_geolocation_estado

# %%
"""
### 4.3 Órdenes + total de artículos y precios
"""

# %%
# une los dataframe orders y items_agg por order_id
orders_totals = orders.merge(
    items_agg,
    on=['order_id'],
    how='left'
)

# %%
orders_totals

# %%
"""
### 4.4 Clientes + geolocalización + nombre del estado donde viven + Órdenes + total de artículos y precios
"""

# %%
results = orders_totals.merge(
    customers_geolocation_estado,
    on=['customer_id'],
    how='left'
)

# %%
results.info()

# %%
"""
Antes de guardar los resultados, verificacmos si existen las carpetas para guardar los resultados
"""

# %%

check_results_folder()

# %%
"""
Finalmente escribiremos el resultado en un archivo separado por comas `.csv`:
"""

# %%
# Completa el codigo
results.to_csv(
    # nombre del archivo
    'results/1/oilst_processed.csv',
    # flag para no escribir el indice del dataframe al csv
    index=False
)
