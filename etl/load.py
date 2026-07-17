import pandas as pd
from sqlalchemy.engine import Engine
from sqlalchemy import text


def load_table(df: pd.DataFrame, table: str, schema: str, etl_conn: Engine, replace: bool = True):
    full_table_name = f"{schema}.{table}" if schema else table
    
    if replace:
        with etl_conn.begin() as conn:
            conn.execute(text(f'DELETE FROM {full_table_name}'))

    
    df.to_sql(
        name=table,
        con=etl_conn,
        schema=schema,
        if_exists='append',
        index=False
    )


def load_cliente(dim_cliente: pd.DataFrame, etl_conn: Engine):
    load_table(dim_cliente, "dim_cliente", None, etl_conn)  


def load_mensajero(dim_mensajero: pd.DataFrame, etl_conn: Engine):
    load_table(dim_mensajero, "dim_mensajero", None, etl_conn)  


def load_estado(dim_estado: pd.DataFrame, etl_conn: Engine):
    load_table(dim_estado, "dim_estado", None, etl_conn) 


def load_sede(dim_sede: pd.DataFrame, etl_conn: Engine):
    load_table(dim_sede, "dim_sede", None, etl_conn)  


def load_tiempo(dim_tiempo: pd.DataFrame, etl_conn: Engine):
    load_table(dim_tiempo, "dim_tiempo", None, etl_conn) 


def load_hora(dim_hora: pd.DataFrame, etl_conn: Engine):
    load_table(dim_hora, "dim_hora", None, etl_conn)  


def load_novedad(dim_novedad: pd.DataFrame, etl_conn: Engine):
    load_table(dim_novedad, "dim_novedad", None, etl_conn) 


def load_hecho_novedad(hecho_novedad: pd.DataFrame, etl_conn: Engine):
    load_table(hecho_novedad, "hecho_novedad", "data_mart_novedades", etl_conn)  


def load_hecho_seguimiento_estado(hecho: pd.DataFrame, etl_conn: Engine):
    load_table(hecho, "hecho_seguimiento_estado", "data_mart_entregas", etl_conn)  


def load_hecho_servicio(hecho_servicio: pd.DataFrame, etl_conn: Engine):
    load_table(hecho_servicio, "hecho_servicio", "data_mart_entregas", etl_conn)