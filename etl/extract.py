import pandas as pd
from sqlalchemy.engine import Engine


def extract_cliente(conection: Engine):
    return pd.read_sql_table('cliente', conection)


