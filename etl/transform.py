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


    return hecho


def transform_hecho_seguimiento_estado(args, dim_tiempo: pd.DataFrame) -> pd.DataFrame:
    df, servicios = args
    df = df.copy()
    
    # traer mensajero_id desde mensajeria_servicio
    df = df.merge(servicios[['id', 'mensajero_id']], left_on='servicio_id', right_on='id', how='left')
    df['mensajero_id'] = df['mensajero_id'].fillna(0).astype(int)
    
    # combinar fecha y hora en un datetime
    df['datetime'] = pd.to_datetime(df['fecha'].astype(str) + ' ' + df['hora'].astype(str), format='mixed')    
    # ordenar por servicio y datetime
    df = df.sort_values(['servicio_id', 'datetime']).reset_index(drop=True)
    
    # calcular datetime_fin
    df['datetime_fin'] = df.groupby('servicio_id')['datetime'].shift(-1)
    
    # duracion en minutos
    df['duracion_tiempo_estado'] = (
        (df['datetime_fin'] - df['datetime'])
        .dt.total_seconds()
        .div(60)
        .fillna(0)
        .astype(int)
    )
    
    # join dim_tiempo para inicio
    dim_tiempo_join = dim_tiempo[['id_tiempo', 'fecha']].copy()
    dim_tiempo_join['fecha'] = pd.to_datetime(dim_tiempo_join['fecha'])
    
    df['fecha_inicio'] = df['datetime'].dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_inicio', right_on='fecha', how='left')
    df = df.rename(columns={'id_tiempo': 'id_tiempo_estado_inicio'})
    
    # join dim_tiempo para fin
    df['fecha_fin'] = df['datetime_fin'].dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_fin', right_on='fecha', how='left')
    df = df.rename(columns={'id_tiempo': 'id_tiempo_estado_fin'})
    
    # ultimo estado sin fin
    df['id_tiempo_estado_fin'] = df['id_tiempo_estado_fin'].fillna(1).astype(int)
    
    # construir hecho final
    hecho = pd.DataFrame()
    hecho['id_estado_servicio']      = df['id_x']  
    hecho['id_estado']               = df['estado_id']
    hecho['id_mensajero']            = df['mensajero_id']
    hecho['id_tiempo_estado_inicio'] = df['id_tiempo_estado_inicio'].astype(int)
    hecho['id_tiempo_estado_fin']    = df['id_tiempo_estado_fin']
    hecho['duracion_tiempo_estado']  = df['duracion_tiempo_estado']
    hecho['id_hora']                 = df['datetime'].dt.hour
    hecho['cod_servicio']            = df['servicio_id']
    
    return hecho

def transform_hecho_servicio(args, dim_tiempo: pd.DataFrame) -> pd.DataFrame:
    servicio, usuario, estados = args

    df = pd.merge(servicio, usuario[['id', 'sede_id']], left_on='usuario_id', right_on='id', how='left')

    df['datetime_solicitud'] = pd.to_datetime(
        df['fecha_solicitud'].astype(str) + ' ' + df['hora_solicitud'].astype(str),
        format='mixed'
    )
    estados['fecha_str'] = pd.to_datetime(estados['fecha']).dt.strftime('%Y-%m-%d')
    estados['hora_str']  = estados['hora'].astype(str).str.split('.').str[0]
    estados['datetime']  = pd.to_datetime(
        estados['fecha_str'] + ' ' + estados['hora_str'],
        format='%Y-%m-%d %H:%M:%S'
    )

    duracion = estados.groupby('servicio_id')['datetime'].agg(
        inicio='min', fin='max'
    ).reset_index()
    duracion['duracion_servicio'] = (
        (duracion['fin'] - duracion['inicio'])
        .dt.total_seconds()
        .div(60)
        .fillna(0)
        .round()
        .astype(int)
    )
    df = pd.merge(df, duracion[['servicio_id', 'duracion_servicio']], left_on='id_x', right_on='servicio_id', how='left')

    dim_tiempo_join = dim_tiempo[['id_tiempo', 'fecha']].copy()
    dim_tiempo_join['fecha'] = pd.to_datetime(dim_tiempo_join['fecha'])
    df['fecha_solicitud_norm'] = pd.to_datetime(df['fecha_solicitud']).dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_solicitud_norm', right_on='fecha', how='left')

    df['mensajero_id'] = df['mensajero_id'].fillna(0).astype(int)

    hecho = pd.DataFrame()
    hecho['id_hecho_servicio'] = df['id_x']
    hecho['id_cliente']        = df['cliente_id']
    hecho['id_sede']           = df['sede_id']
    hecho['id_tiempo']         = df['id_tiempo'].fillna(1).astype(int)
    hecho['id_hora']           = df['datetime_solicitud'].dt.hour
    hecho['id_mensajero']      = df['mensajero_id']
    hecho['cod_servicio']      = df['id_x']
    hecho['duracion_servicio'] = df['duracion_servicio'].fillna(0).astype(int)
    hecho['total_servicios']   = 1

    hecho = hecho[df['es_prueba'] == False].reset_index(drop=True)
    return hecho