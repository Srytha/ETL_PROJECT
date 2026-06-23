import pandas as pd
from sqlalchemy.engine import Engine

def extract_cliente(conection: Engine):
    dim_cliente = pd.read_sql_table('cliente', conection)
    return dim_cliente

def extract_estado(conection: Engine):
    dim_estado = pd.read_sql_table('mensajeria_estado', conection)
    return dim_estado

def extract_novedad(conection: Engine):
    tipo_novedad = pd.read_sql_table('mensajeria_tiponovedad', conection)
    return tipo_novedad

def extract_ubicacion(conection: Engine):
    sede = pd.read_sql_table('sede', conection)
    ciudad = pd.read_sql_table('ciudad', conection)
    departamento = pd.read_sql_table('departamento', conection)
    return [sede, ciudad, departamento]

def extract_mensajero(conection: Engine):
    dim_mensajero = pd.read_sql_table('clientes_mensajeroaquitoy', conection)
    return dim_mensajero

def extract_hecho_novedad(conection: Engine):
    hecho_novedad = pd.read_sql_table('mensajeria_novedadesservicio', conection)
    return hecho_novedad

def extract_hecho_seguimiento_estado(conection: Engine):
    estados = pd.read_sql_table('mensajeria_estadosservicio', conection)
    servicios = pd.read_sql_table('mensajeria_servicio', conection)
    return [estados, servicios]

def extract_tiempo(conection: Engine = None):

    dim_tiempo = pd.DataFrame({
        "fecha": pd.date_range(start='2023-09-19', end='2024-08-31', freq='D')
    })
    
    dim_tiempo["id_tiempo"] = range(1, len(dim_tiempo) + 1)
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

def extract_hecho_servicio(conection: Engine):
    servicio = pd.read_sql_table('mensajeria_servicio', conection)
    usuario = pd.read_sql_table('clientes_usuarioaquitoy', conection)
    return [servicio, usuario]