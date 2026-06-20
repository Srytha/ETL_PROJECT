import pandas as pd
from sqlalchemy.engine import Engine

def extract_cliente(conection: Engine):
    dim_cliente = pd.read_sql_table('cliente', conection)
    return dim_cliente

def extract_estado(conection: Engine):
    dim_estado = pd.read_sql_table('mensajeria_estado', conection)
    return dim_estado

def extract_novedad(conection: Engine):
    novedad = pd.read_sql_table('mensajeria_novedadesservicio', conection)
    tipo_novedad = pd.read_sql_table('mensajeria_tiponovedad', conection)
    return [novedad, tipo_novedad]

def extract_ubicacion(conection: Engine):
    sede = pd.read_sql_table('sede', conection)
    ciudad = pd.read_sql_table('ciudad', conection)
    departamento = pd.read_sql_table('departamento', conection)
    return [sede, ciudad, departamento]

def extract_mensajero(conection: Engine):
    dim_mensajero = pd.read_sql_table('clientes_mensajeroaquitoy', conection)
    return dim_mensajero




# Revisar 
def extract_tiempo(conection: Engine = None):

    dim_tiempo = pd.DataFrame({
        "fecha": pd.date_range(start='2023-09-19', end='2024-08-31', freq='D')
    })
    
    dim_tiempo["id_tiempo"] = dim_tiempo["fecha"].dt.strftime("%Y%m%d").astype(int)
    dim_tiempo["año"] = dim_tiempo["fecha"].dt.year
    dim_tiempo["mes"] = dim_tiempo["fecha"].dt.month
    dim_tiempo["semana"] = dim_tiempo["fecha"].dt.isocalendar().week
    dim_tiempo["dia"] = dim_tiempo["fecha"].dt.day
    dim_tiempo["fin_de_semana"] = dim_tiempo["fecha"].dt.weekday >= 5
    
    return dim_tiempo

def extract_hora(conection: Engine = None):
    dim_hora = pd.DataFrame({
        "id_hora": pd.date_range(24),
        "hora": pd.date_range(24)
    })
    
    return dim_hora