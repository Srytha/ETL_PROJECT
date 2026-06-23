#%%
import datetime
from datetime import timedelta, date, datetime
import pandas as pd
import numpy as np

def transform_cliente(df_cliente: pd.DataFrame) -> pd.DataFrame:
    df = df_cliente.copy()

    df_dim_cliente = pd.DataFrame()
    df_dim_cliente["id_cliente"] = df["cliente_id"]

    df_dim_cliente["nombre_cliente"] = df["nombre"]
    df_dim_cliente["tipo_cliente"] = df["tipo_cliente_id"]

    df_dim_cliente["email"] = df["email"]
    df_dim_cliente["telefono"] = df["telefono"]

    df_dim_cliente["sector"] = df["sector"]

    df_dim_cliente = df_dim_cliente.drop_duplicates(subset=["id_cliente"])
    return df_dim_cliente

def transform_sede(args) -> pd.DataFrame:
    sede, ciudad, departamento = args

    df_merged= pd.merge(sede, ciudad, on='ciudad_id', how='left')
    df_merged = pd.merge(df_merged, departamento, on='departamento_id', how='left')
    
    df_dim_sede= pd.DataFrame()
    df_dim_sede["id_sede"] = df_merged["sede_id"]
    df_dim_sede["nombre_sede"] = df_merged["nombre_x"]
    df_dim_sede["ciudad"] = df_merged["nombre_y"]
    df_dim_sede["departamento"] = df_merged["nombre"]
    df_dim_sede["direccion"] = df_merged["direccion"]
    
    df_dim_sede = df_dim_sede.drop_duplicates(subset=["id_sede"])

    return df_dim_sede

def transform_estado(df_estado: pd.DataFrame) -> pd.DataFrame:
    df = df_estado.copy()
    df_dim_estado = pd.DataFrame()
    df_dim_estado["id_estado"] = df["id"]
    df_dim_estado["nombre_estado"] = df["nombre"]
    df_dim_estado["descripcion"] = df["descripcion"]
    
    df_dim_estado = df_dim_estado.drop_duplicates(subset=["id_estado"])
    return df_dim_estado

def transform_novedad(df_novedad: pd.DataFrame) -> pd.DataFrame:
    df = df_novedad.copy()

    df_dim_novedad = pd.DataFrame()
    df_dim_novedad["id_tipo_novedad"] = df["id"]
    df_dim_novedad["tipo_novedad"] = df["nombre"]
    
    return df_dim_novedad


def transform_mensajero(df_mensajero: pd.DataFrame) -> pd.DataFrame:
    df = df_mensajero.copy()
    df_dim_mensajero = pd.DataFrame()
    df_dim_mensajero["id_mensajero"] = df["id"]
    df_dim_mensajero["activo"] = df["activo"]
    
    return df_dim_mensajero

def transform_fecha() -> pd.DataFrame:
  
    dim_tiempo = pd.DataFrame({
        "fecha": pd.date_range(start='09/19/2023', end='31/08/2024', freq='D')
    })
    
    dim_tiempo["id_tiempo"] = range(1, len(dim_tiempo) + 1)
    dim_tiempo["año"] = dim_tiempo["fecha"].dt.year
    dim_tiempo["mes"] = dim_tiempo["fecha"].dt.month
    dim_tiempo["dia"] = dim_tiempo["fecha"].dt.day
    dim_tiempo["dia_semana"] = dim_tiempo["fecha"].dt.weekday
    dim_tiempo["fin_de_semana"] = np.where(dim_tiempo["dia_semana"].isin([5, 6]), 1, 0)
    
    
    return dim_tiempo

def transform_hora() -> pd.DataFrame:
    dim_hora = pd.DataFrame({
        "id_hora": range(24),
        "hora": range(24)
    })
    
    return dim_hora

def transform_hecho_novedad(df_novedad: pd.DataFrame, dim_tiempo: pd.DataFrame) -> pd.DataFrame:

    hecho = pd.DataFrame()

    hecho["id_novedad_servicio"] = df_novedad["id"]
    hecho["id_tipo_novedad"] = df_novedad["tipo_novedad_id"]
    hecho["id_mensajero"] = df_novedad["mensajero_id"]
    hecho["fecha"] = pd.to_datetime(df_novedad["fecha_novedad"], utc=True).dt.tz_convert(None).dt.normalize()    
    hecho = hecho.merge(dim_tiempo[["fecha", "id_tiempo"]],on="fecha", how="left")
    hecho["id_hora"] = pd.to_datetime(df_novedad["fecha_novedad"]).dt.hour
    hecho["cod_servicio"] = df_novedad["servicio_id"]

  
    hecho["cantidad_novedades"] = 1


    hecho.drop(columns=["fecha"], inplace=True)
    
    return hecho
