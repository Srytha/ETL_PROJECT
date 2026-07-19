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
    df_dim_estado = df_dim_estado.sort_values('id_estado')
    

    return df_dim_estado

def transform_novedad(df_novedad: pd.DataFrame) -> pd.DataFrame:
    df = df_novedad.copy()

    df_dim_novedad = pd.DataFrame()
    df_dim_novedad["id_tipo_novedad"] = df["id"]
    df_dim_novedad["tipo_novedad"] = df["nombre"]
    df_dim_novedad = df_dim_novedad.sort_values('id_tipo_novedad')
    return df_dim_novedad


def transform_mensajero(df_mensajero: pd.DataFrame) -> pd.DataFrame:
    df = df_mensajero.copy()
    df_dim_mensajero = pd.DataFrame()
    df_dim_mensajero["id_mensajero"] = df["id"]
    df_dim_mensajero["activo"] = df["activo"]

    fila_sin_asignar = pd.DataFrame({
        "id_mensajero": [0],
        "activo": [False]
    })
    df_dim_mensajero = pd.concat([fila_sin_asignar, df_dim_mensajero], ignore_index=True)

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
    dim_tiempo["fin_de_semana"] = np.where(dim_tiempo["dia_semana"].isin([5, 6]), True, False)
    
    
    return dim_tiempo

def transform_hora() -> pd.DataFrame:
    dim_hora = pd.DataFrame({
        "id_hora": range(24),
        "hora": range(24)
    })
    
    return dim_hora

def transform_hecho_novedad(df_novedad: pd.DataFrame, 
                            dim_tiempo: pd.DataFrame, 
                            dim_mensajero: pd.DataFrame, 
                            dim_novedad: pd.DataFrame,
                            dim_hora: pd.DataFrame) -> pd.DataFrame:
    

    hecho = pd.DataFrame()
    hecho["id_novedad_servicio"] = df_novedad["id"]
    hecho["id_novedad"] = df_novedad["tipo_novedad_id"]
    hecho["id_mensajero"] = df_novedad["mensajero_id"].fillna(0).astype(int)
    hecho["fecha"] = pd.to_datetime(df_novedad["fecha_novedad"], utc=True).dt.tz_convert(None).dt.normalize()
    

    hecho["id_hora"] = pd.to_datetime(df_novedad["fecha_novedad"]).dt.hour
    

    hecho = hecho.merge(
        dim_hora[["key_dim_hora", "id_hora"]], 
        on="id_hora", 
        how="left"
    )

    hecho = hecho.merge(
        dim_novedad[["key_dim_tipo_novedad", "id_tipo_novedad"]], 
        left_on="id_novedad", 
        right_on="id_tipo_novedad", 
        how="left"
    )
    
    
    hecho = hecho.merge(
        dim_mensajero[["key_dim_mensajero", "id_mensajero"]], 
        left_on="id_mensajero", 
        right_on="id_mensajero", 
        how="left"
    )
    
   
    dim_tiempo_copy = dim_tiempo.copy()
    dim_tiempo_copy["fecha"] = pd.to_datetime(dim_tiempo_copy["fecha"]).dt.normalize()
    
    hecho = hecho.merge(
        dim_tiempo_copy[["key_dim_tiempo", "fecha"]], 
        on="fecha", 
        how="left"
    )
    
   
    hecho_final = pd.DataFrame({
        "key_dim_tipo_novedad": hecho["key_dim_tipo_novedad"],
        "key_dim_mensajero": hecho["key_dim_mensajero"],
        "key_dim_tiempo": hecho["key_dim_tiempo"],
        "key_dim_hora": hecho["key_dim_hora"],  
        "cod_servicio": df_novedad["servicio_id"],
        "cantidad_novedades": 1
    })
    
    return hecho_final


def transform_hecho_seguimiento_estado(args, dim_tiempo: pd.DataFrame, 
                                       dim_mensajero: pd.DataFrame, 
                                       dim_estado: pd.DataFrame, 
                                       dim_hora: pd.DataFrame) -> pd.DataFrame:
    df, servicios = args
    df = df.copy()
    
    df = df.merge(servicios[['id', 'mensajero_id']], left_on='servicio_id', right_on='id', how='left')
    df['mensajero_id'] = df['mensajero_id'].fillna(0).astype(int)  # ← Esto está bien
    
    df = df.merge(
        dim_mensajero[['key_dim_mensajero', 'id_mensajero']],
        left_on='mensajero_id',
        right_on='id_mensajero',
        how='left'
    )

    df['key_dim_mensajero'] = df['key_dim_mensajero'].astype("Int64")
    
   
    df = df.merge(
        dim_estado[['key_dim_estado', 'id_estado']],
        left_on='estado_id',
        right_on='id_estado',
        how='left'
    )
    df['key_dim_estado'] = df['key_dim_estado'].astype("Int64")
    

    df['datetime'] = pd.to_datetime(df['fecha'].astype(str) + ' ' + df['hora'].astype(str), format='mixed')

    df = df.sort_values(['servicio_id', 'datetime']).reset_index(drop=True)
    df['datetime_fin'] = df.groupby('servicio_id')['datetime'].shift(-1)
    
    df['duracion_tiempo_estado'] = (
        (df['datetime_fin'] - df['datetime'])
        .dt.total_seconds()
        .div(60)
        .fillna(0)
        .astype(int)
    )
    
    dim_tiempo_join = dim_tiempo[['key_dim_tiempo', 'fecha']].copy()
    dim_tiempo_join['fecha'] = pd.to_datetime(dim_tiempo_join['fecha'])
    
    df['fecha_inicio'] = df['datetime'].dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_inicio', right_on='fecha', how='left')
    df = df.rename(columns={'key_dim_tiempo': 'key_dim_tiempo_inicio'})
    
    df['fecha_fin'] = df['datetime_fin'].dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_fin', right_on='fecha', how='left')
    df = df.rename(columns={'key_dim_tiempo': 'key_dim_tiempo_fin'})
    
    min_key = dim_tiempo['key_dim_tiempo'].min()
    df['key_dim_tiempo_fin'] = df['key_dim_tiempo_fin'].fillna(min_key).astype(int)
    
    df['id_hora'] = df['datetime'].dt.hour
    df = df.merge(
        dim_hora[['key_dim_hora', 'id_hora']],
        left_on='id_hora',
        right_on='id_hora',
        how='left'
    )
    df['key_dim_hora'] = df['key_dim_hora'].astype("Int64")

    hecho = pd.DataFrame()
    hecho['key_dim_estado'] = df['key_dim_estado']
    hecho['key_dim_mensajero'] = df['key_dim_mensajero']  
    hecho['key_dim_tiempo_inicio'] = df['key_dim_tiempo_inicio'].astype(int)
    hecho['key_dim_tiempo_fin'] = df['key_dim_tiempo_fin']
    hecho['duracion_tiempo_estado'] = df['duracion_tiempo_estado']
    hecho['key_dim_hora'] = df['key_dim_hora']
    hecho['cod_servicio'] = df['servicio_id']
    
    print(f"Registros procesados: {len(hecho)}")
    print(f"Con mensajero: {len(hecho[hecho['key_dim_mensajero'].notna()])}")
    print(f"Sin mensajero (NULL): {len(hecho[hecho['key_dim_mensajero'].isna()])}")
    
    return hecho

def transform_hecho_servicio(args, dim_tiempo: pd.DataFrame, 
                             dim_cliente: pd.DataFrame,
                             dim_sede: pd.DataFrame,
                             dim_mensajero: pd.DataFrame,
                             dim_hora: pd.DataFrame) -> pd.DataFrame:
    servicio, usuario, estados = args

    df = pd.merge(servicio, usuario[['id', 'sede_id']], left_on='usuario_id', right_on='id', how='left')

    #Crea datetime de solicitud
    df['datetime_solicitud'] = pd.to_datetime(
        df['fecha_solicitud'].astype(str) + ' ' + df['hora_solicitud'].astype(str),
        format='mixed'
    )

    #Calcula duracion del servicio
    estados['fecha_str'] = pd.to_datetime(estados['fecha']).dt.strftime('%Y-%m-%d')
    estados['hora_str'] = estados['hora'].astype(str).str.split('.').str[0]
    estados['datetime'] = pd.to_datetime(
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

    # Mapear fecha a key_dim_tiempo
    dim_tiempo_join = dim_tiempo[['key_dim_tiempo', 'fecha']].copy()
    dim_tiempo_join['fecha'] = pd.to_datetime(dim_tiempo_join['fecha'])
    df['fecha_solicitud_norm'] = pd.to_datetime(df['fecha_solicitud']).dt.normalize()
    df = df.merge(dim_tiempo_join, left_on='fecha_solicitud_norm', right_on='fecha', how='left')
    df['key_dim_tiempo'] = df['key_dim_tiempo'].fillna(1).astype(int)


    # Mapear hora a key_dim_hora
    df['id_hora'] = df['datetime_solicitud'].dt.hour
    df = df.merge(
        dim_hora[['key_dim_hora', 'id_hora']],
        left_on='id_hora',
        right_on='id_hora',
        how='left'
    )
    df['key_dim_hora'] = df['key_dim_hora'].fillna(1).astype(int)


    # Mapear cliente a key_dim_cliente
    df = df.merge(
        dim_cliente[['key_dim_cliente', 'id_cliente']],
        left_on='cliente_id',
        right_on='id_cliente',
        how='left'
    )
    df['key_dim_cliente'] = df['key_dim_cliente'].fillna(0).astype(int)


     # Mapear sede a key_dim_sede
    df = df.merge(
        dim_sede[['key_dim_sede', 'id_sede']],
        left_on='sede_id',
        right_on='id_sede',
        how='left'
    )
    df['key_dim_sede'] = df['key_dim_sede'].fillna(0).astype(int)

    # Mapear mensajero a key_dim_mensajero
    df['mensajero_id'] = df['mensajero_id'].fillna(0).astype(int)
    df = df.merge(
        dim_mensajero[['key_dim_mensajero', 'id_mensajero']],
        left_on='mensajero_id',
        right_on='id_mensajero',
        how='left'
    )
   
    df['key_dim_mensajero'] = df['key_dim_mensajero'].astype("Int64")

    hecho = pd.DataFrame()
    hecho['key_dim_cliente'] = df['key_dim_cliente']
    hecho['key_dim_sede'] = df['key_dim_sede']
    hecho['key_dim_tiempo'] = df['key_dim_tiempo']
    hecho['key_dim_hora'] = df['key_dim_hora']
    hecho['key_dim_mensajero'] = df['key_dim_mensajero']
    hecho['cod_servicio'] = df['id_x']
    hecho['duracion_servicio'] = df['duracion_servicio'].fillna(0).astype(int)
    hecho['total_servicios'] = 1

    hecho = hecho[df['es_prueba'] == False].reset_index(drop=True)

    return hecho