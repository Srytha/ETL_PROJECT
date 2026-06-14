import pandas as pd
from sqlalchemy.engine import Engine

def load_cliente(dim_cliente: pd.DataFrame, etl_conn: Engine):
    dim_cliente.to_sql(
        'dim_cliente',
        etl_conn,
        if_exists='append',
        index=False
    )