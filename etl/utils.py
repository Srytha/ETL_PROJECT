# utils.py
import pandas as pd
from sqlalchemy.engine import Engine

def recargar_dimensiones(dw_conn: Engine) -> dict:
    """
    Recarga todas las dimensiones con sus keys sustitutas 
    """
    dimensiones = {}

    dims = {
        'dim_cliente': ['key_dim_cliente', 'id_cliente'],
        'dim_sede': ['key_dim_sede', 'id_sede'],
        'dim_estado': ['key_dim_estado', 'id_estado'],
        'dim_tiempo': ['key_dim_tiempo', 'id_tiempo', 'fecha'],
        'dim_hora': ['key_dim_hora', 'id_hora', 'hora'],
        'dim_mensajero': ['key_dim_mensajero', 'id_mensajero'],
        'dim_novedad': ['key_dim_tipo_novedad', 'id_tipo_novedad'],  
    }
    
    for tabla, columnas in dims.items():
        query = f"SELECT {', '.join(columnas)} FROM {tabla}"
        dimensiones[tabla] = pd.read_sql(query, dw_conn)
        print(f"Recargada {tabla} con {len(dimensiones[tabla])} registros")
    
    return dimensiones