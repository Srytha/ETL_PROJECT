import pandas as pd
from sqlalchemy.engine import Engine

def load_cliente(dim_cliente: pd.DataFrame, engine_destino: Engine):
    dim_cliente.to_sql(
        'dim_cliente',
        con=engine_destino,
        if_exists='replace',
        index=False
    )
    
def load_estado(dim_estado: pd.DataFrame, engine_destino: Engine):

    dim_estado.to_sql(
        'dim_estado',
        con=engine_destino,
        if_exists='replace',
        index=False
    )
    
def load_novedad(dim_novedad: pd.DataFrame, engine_destino: Engine):

    dim_novedad.to_sql(
        'dim_novedad',
        con=engine_destino,
        if_exists='replace',
        index=False
    )
    

    
def load_sede(dim_sede: pd.DataFrame, engine_destino: Engine):

    dim_sede.to_sql(
        'dim_sede',
        con=engine_destino,
        if_exists='replace',
        index=False
    )
    
def load_tiempo(dim_tiempo: pd.DataFrame, engine_destino: Engine):

    dim_tiempo.to_sql(
        'dim_tiempo',
        con=engine_destino,
        if_exists='replace',
        index=False
    )