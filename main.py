import yaml
import psycopg2
import pandas as pd
from sqlalchemy import create_engine, inspect
from etl import extract, transform, load
from sqlalchemy import text

pd.set_option('display.max_rows', 100)
pd.set_option('display.max_columns', 100)

# Conexion a base de datos

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

# Crear esquemas y tablas

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



# DataMart 1
print("DataMart 1")
df_cliente = extract.extract_cliente(source_conn)
dim_cliente = transform.transform_cliente(df_cliente)
load.load_cliente(dim_cliente, dw_conn)
print("Dimension cliente completado :v")


sede, ciudad, departamento = extract.extract_ubicacion(source_conn)
dim_sede = transform.transform_sede([sede, ciudad, departamento])
load.load_sede(dim_sede, dw_conn)
print("Dimension sede completado :v")

df_estado = extract.extract_estado(source_conn)
dim_estado = transform.transform_estado(df_estado)
load.load_estado(dim_estado, dw_conn)
print("Dimension estado completado :v")

df_mensajero = extract.extract_mensajero(source_conn)
dim_mensajero = transform.transform_mensajero(df_mensajero)
load.load_mensajero(dim_mensajero, dw_conn)
print("Dimension mensajero completado :v")


dim_tiempo = transform.transform_fecha()
load.load_tiempo(dim_tiempo, dw_conn)
print("Dimension tiempo completado :v")

dim_hora = transform.transform_hora()
load.load_hora(dim_hora, dw_conn)
print("Dimension hora completado :v")

df_seguimiento, df_servicios = extract.extract_hecho_seguimiento_estado(source_conn)
dim_tiempo_df = transform.transform_fecha()
hecho_seguimiento = transform.transform_hecho_seguimiento_estado([df_seguimiento, df_servicios], dim_tiempo_df)
load.load_hecho_seguimiento_estado(hecho_seguimiento, dw_conn)
print("Hecho seguimiento estado completado :v")

# DataMart 2
print("DataMart 2")
tipo_novedad = extract.extract_novedad(source_conn)
dim_novedad = transform.transform_novedad(tipo_novedad)
load.load_novedad(dim_novedad, dw_conn)
print("Dimension novedad completado :v")

load.load_mensajero_novedades(dim_mensajero, dw_conn)
print("Dimension mensajero completado :v")

load.load_tiempo_novedades(dim_tiempo, dw_conn)
print("Dimension tiempo completado :v")

load.load_hora_novedades(dim_hora, dw_conn)
print("Dimension hora completado :v")

# Hecho Novedad
df_hecho_novedad = extract.extract_hecho_novedad(source_conn)
hecho_novedad = transform.transform_hecho_novedad(df_hecho_novedad, dim_tiempo)
load.load_hecho_novedad(hecho_novedad,dw_conn)
print("Hecho novedad completado :v")


with dw_conn.connect() as conn:
    tablas = [
        'data_mart_entregas.dim_cliente',
        'data_mart_entregas.dim_mensajero',
        'data_mart_entregas.dim_sede',
        'data_mart_entregas.dim_estado',
        'data_mart_entregas.dim_tiempo',
        'data_mart_entregas.dim_hora',
        'data_mart_novedades.dim_novedad',
        'data_mart_novedades.dim_mensajero',
        'data_mart_novedades.dim_tiempo',
        'data_mart_novedades.dim_hora',
        'data_mart_novedades.hecho_novedad',
    ]
    
    for tabla in tablas:
        try:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {tabla}"))
            count = result.fetchone()[0]
            print(f"Tabla {tabla}: {count} registros")
        except Exception as e:
            print(f"Error al consultar {tabla}: {e}")
