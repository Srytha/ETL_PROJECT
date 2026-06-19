import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, inspect
from etl import extract, transform, load

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)
    config_source = config['SOURCE_DB']
    config_dw = config['ETL_PRO']


url_source = (
    f"{config_source['drivername']}://{config_source['user']}:{config_source['password']}@"
    f"{config_source['host']}:{config_source['port']}/{config_source['dbname']}"
)

url_dw = (
    f"{config_dw['drivername']}://{config_dw['user']}:{config_dw['password']}@"
    f"{config_dw['host']}:{config_dw['port']}/{config_dw['dbname']}"
)

source_conn = create_engine(url_source)
dw_conn = create_engine(url_dw)

inspector = inspect(dw_conn)
tnames = inspector.get_table_names()

if not tnames:
    conn = psycopg2.connect(
        dbname=config_dw['dbname'],
        user=config_dw['user'],
        password=config_dw['password'],
        host=config_dw['host'],
        port=config_dw['port']
    )

    cur = conn.cursor()
    with open('sqlscripts.yml', 'r') as f:
        sql = yaml.safe_load(f)
        for val in sql.values():
            cur.execute(val)
            conn.commit()



df_cliente = extract.extract_cliente(source_conn)
dim_cliente = transform.transform_cliente(df_cliente)
load.load_cliente(dim_cliente, dw_conn)
print("Dimension cliente completado :v")


sede, ciudad, departamento = extract.extract_ubicacion(source_conn)
dim_sede = transform.transform_ubicacion([sede, ciudad, departamento])
load.load_sede(dim_sede, dw_conn)
print("Dimension sede completado :v")

df_estado = extract.extract_estado(source_conn)
dim_estado = transform.transform_estado(df_estado)
load.load_estado(dim_estado, dw_conn)
print("Dimension estado completado :v")

novedad, tipo_novedad = extract.extract_novedad(source_conn)
dim_novedad = transform.transform_novedad([novedad, tipo_novedad])
load.load_novedad(dim_novedad, dw_conn)
print("Dimension novedad completado :v")

dim_tiempo = transform.transform_fecha()
load.load_tiempo(dim_tiempo, dw_conn)
print("Dimension tiempo completado :v")