"""
pruebas.py

Ejecuta las 9 consultas de negocio del proyecto contra la base de datos
etl_mensajeria (data warehouse) y muestra los resultados en consola.

Uso:
    python pruebas.py

Requiere que el contenedor de Postgres esté corriendo y que config.yml
tenga la sección ETL_PRO configurada.
"""

import yaml
import pandas as pd
from sqlalchemy import create_engine, text

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 120)


def get_dw_engine():
    with open('config.yml', 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
        config_dw = config['etl_mensajeria']

    url_dw = (
        f"{config_dw['drivername']}://{config_dw['user']}:{config_dw['password']}@"
        f"{config_dw['host']}:{config_dw['port']}/{config_dw['dbname']}"
    )
    return create_engine(url_dw)


CONSULTAS = {
    "1) Meses con más servicios solicitados": """
        SELECT t.mes, t.nombre_mes, COUNT(*) AS total_servicios
        FROM data_mart_entregas.hecho_servicio h
        JOIN dim_tiempo t ON h.key_dim_tiempo = t.key_dim_tiempo
        GROUP BY t.mes, t.nombre_mes
        ORDER BY total_servicios DESC;
    """,

    "2) Días de la semana con más solicitudes": """
        SELECT t.dia_semana, t.nombre_dia, COUNT(*) AS total_servicios
        FROM data_mart_entregas.hecho_servicio h
        JOIN dim_tiempo t ON h.key_dim_tiempo = t.key_dim_tiempo
        GROUP BY t.dia_semana, t.nombre_dia
        ORDER BY total_servicios DESC;
    """,

    "3) Hora en que los mensajeros están más ocupados": """
        SELECT hr.hora, COUNT(*) AS eventos
        FROM data_mart_entregas.hecho_seguimiento_estado h
        JOIN dim_hora hr ON h.key_dim_hora = hr.key_dim_hora
        JOIN dim_mensajero m ON h.key_dim_mensajero = m.key_dim_mensajero
        WHERE m.id_mensajero != 0
        GROUP BY hr.hora
        ORDER BY eventos DESC;
    """,

    "4) Servicios solicitados por cliente y por mes": """
        SELECT c.nombre_cliente, t.mes, t.nombre_mes, COUNT(*) AS total_servicios
        FROM data_mart_entregas.hecho_servicio h
        JOIN dim_cliente c ON h.key_dim_cliente = c.key_dim_cliente
        JOIN dim_tiempo t ON h.key_dim_tiempo = t.key_dim_tiempo
        GROUP BY c.nombre_cliente, t.mes, t.nombre_mes
        ORDER BY c.nombre_cliente, t.mes;
    """,

    "5) Mensajeros más eficientes (más servicios prestados)": """
        SELECT m.id_mensajero, COUNT(*) AS total_servicios
        FROM data_mart_entregas.hecho_servicio h
        JOIN dim_mensajero m ON h.key_dim_mensajero = m.key_dim_mensajero
        WHERE m.id_mensajero != 0
        GROUP BY m.id_mensajero
        ORDER BY total_servicios DESC
        LIMIT 10;
    """,

    "6) Sedes que más servicios solicitan por cada cliente": """
        SELECT c.nombre_cliente, s.nombre_sede, COUNT(*) AS total_servicios
        FROM data_mart_entregas.hecho_servicio h
        JOIN dim_cliente c ON h.key_dim_cliente = c.key_dim_cliente
        JOIN dim_sede s ON h.key_dim_sede = s.key_dim_sede
        GROUP BY c.nombre_cliente, s.nombre_sede
        ORDER BY c.nombre_cliente, total_servicios DESC;
    """,

    "7) Tiempo promedio de entrega (solicitud -> cierre, en minutos)": """
        SELECT ROUND(AVG(duracion_servicio), 2) AS minutos_promedio
        FROM data_mart_entregas.hecho_servicio
        WHERE duracion_servicio > 0;
    """,

    "8) Tiempo de espera promedio por fase del servicio": """
        SELECT e.nombre_estado, ROUND(AVG(h.duracion_tiempo_estado), 2) AS minutos_promedio
        FROM data_mart_entregas.hecho_seguimiento_estado h
        JOIN dim_estado e ON h.key_dim_estado = e.key_dim_estado
        WHERE h.duracion_tiempo_estado > 0
        GROUP BY e.nombre_estado
        ORDER BY minutos_promedio DESC;
    """,

    "9) Novedades más frecuentes": """
        SELECT n.tipo_novedad, SUM(h.cantidad_novedades) AS total
        FROM data_mart_novedades.hecho_novedad h
        JOIN dim_novedad n ON h.key_dim_tipo_novedad = n.key_dim_tipo_novedad
        GROUP BY n.tipo_novedad
        ORDER BY total DESC;
    """,
}


def main():
    engine = get_dw_engine()

    with engine.connect() as conn:
        for titulo, query in CONSULTAS.items():
            print("=" * 100)
            print(titulo)
            print("=" * 100)
            try:
                df = pd.read_sql(text(query), conn)
                if df.empty:
                    print("(sin resultados)")
                else:
                    print(df.to_string(index=False))
            except Exception as e:
                print(f"Error al ejecutar la consulta: {e}")
            print()


if __name__ == "__main__":
    main()