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


# Extract
df_cliente = extract.extract_cliente(source_conn)
# Transform
dim_cliente = transform.transform_cliente(df_cliente)
# Load
load.load_cliente(dim_cliente, dw_conn)
print("Dimension cliente completado :v")

#%%
