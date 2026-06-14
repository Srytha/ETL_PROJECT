#%%
import datetime
from datetime import timedelta, date, datetime
import pandas as pd

def transform_cliente(df_cliente: pd.DataFrame) -> pd.DataFrame:
    df = df_cliente.copy()

    df.columns = [c.lower() for c in df.columns]
    df_dim = pd.DataFrame()
    df_dim["id_cliente"] = df["cliente_id"]

    df_dim["nombre_cliente"] = df["nombre"]
    df_dim["tipo_cliente"] = df["tipo_cliente_id"]

    df_dim["email"] = df["email"]
    df_dim["telefono"] = df["telefono"]

    df_dim["sector"] = df["sector"]

    df_dim = df_dim.drop_duplicates(subset=["id_cliente"])

    return df_dim

