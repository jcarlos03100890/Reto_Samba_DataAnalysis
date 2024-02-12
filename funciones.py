# %%
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 21:35:00 2024

@author: juan_
"""

# %%
"""
# Funciones Auxiliares para acceder a los datos procesados
"""

# %%

# Importamos las librerias requeridas

import json
import os
import pandas as pd

# %%
# Primero indicamos la ruta a la carpeta donde se encuentran los archivos a procesarse
# indicamos en que subfolder se encuentran y construimos la valiable PATH

def set_data_path(folder):
    # Set the file path
    current_path = os.getcwd()
    print("Current Working Directory: ", current_path)

    for dirname, _, filenames in os.walk(folder):
        for filename in filenames:
            print(os.path.join(dirname, filename))

    return current_path + "\\"+folder+"\\"


# %%
"""
En esta funcion leemos el archivo de datos consolidado
"""

def read_data(folder):

    DATA_PATH = set_data_path(folder)

    FILE_CONSOLIDATED_DATA = 'oilst_processed.csv'

    """
    Recordemos que algunas de las columnas que contienen fechas deben ser convertidas al }
    formato correspondiente, lo cual se puede llevar a cabo de forma automática usando el parámetro de `parse_dates`:
    """

    # Lista de columnas a interpretar como fecha
    columns_dates = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]

    """
    ## 3. Lectura de datos

     Leeremos los datos, indicando a Python donde se encuentra la carpeta que se aloja los datos 
     y los nombres de los archivos relevantes para el análisis.
     """
    # Lectura del archivo csv
    return pd.read_csv(
        os.path.join(DATA_PATH, FILE_CONSOLIDATED_DATA),
        parse_dates=columns_dates
    )


# %%
"""
Leemos el archivo de regiones, 
"""

def get_data_region(folder):

    DATA_PATH = set_data_path(folder)
    FILE_REGIONS = 'brasil_regions.csv'

    return pd.read_csv(
        os.path.join(DATA_PATH, FILE_REGIONS),
    )


# %%
"""
Leemos el archivo brasil_geodata.json
"""

def get_geo_data(folder):

    DATA_PATH = set_data_path(folder)
    FILE_GEODATA = 'brasil_geodata.json'
    
    # Cargar archivo datos geográficos de Brasil
    with open(os.path.join(DATA_PATH, FILE_GEODATA), 'r') as f:
        geojson = json.load(f)
    
    return geojson

