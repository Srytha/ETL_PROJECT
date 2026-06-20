import pandas as pd
from sqlalchemy.engine import Engine



def load_table(df: pd.DataFrame, table: str, schema: str, etl_conn: Engine):
    df.to_sql(
        name=table,
        con=etl_conn,
        schema=schema,
        if_exists='replace',
        index=False
    )


def load_cliente(dim_cliente: pd.DataFrame, etl_conn: Engine):
    load_table(dim_cliente, "dim_cliente", "data_mart_entregas", etl_conn)


def load_mensajero(dim_mensajero: pd.DataFrame, etl_conn: Engine):
    load_table(dim_mensajero, "dim_mensajero", "data_mart_entregas", etl_conn)


def load_estado(dim_estado: pd.DataFrame, etl_conn: Engine):
    load_table(dim_estado, "dim_estado", "data_mart_entregas", etl_conn)


def load_sede(dim_sede: pd.DataFrame, etl_conn: Engine):
    load_table(dim_sede, "dim_sede", "data_mart_entregas", etl_conn)


def load_tiempo(dim_tiempo: pd.DataFrame, etl_conn: Engine):
    load_table(dim_tiempo, "dim_tiempo", "data_mart_entregas", etl_conn)



def load_novedad(dim_novedad: pd.DataFrame, etl_conn: Engine):
    load_table(dim_novedad, "dim_novedad", "data_mart_novedades", etl_conn)


def load_mensajero_novedades(dim_mensajero: pd.DataFrame, etl_conn: Engine):
    load_table(dim_mensajero, "dim_mensajero", "data_mart_novedades", etl_conn)


def load_tiempo_novedades(dim_tiempo: pd.DataFrame, etl_conn: Engine):
    load_table(dim_tiempo, "dim_tiempo", "data_mart_novedades", etl_conn)


def load_hora(dim_hora: pd.DataFrame, etl_conn: Engine):
    load_table(dim_hora, "dim_hora", "data_mart_entregas", etl_conn)

def load_hora_novedades(dim_hora: pd.DataFrame, etl_conn: Engine):
    load_table(dim_hora, "dim_hora", "data_mart_novedades", etl_conn)