from sqlalchemy import Engine, text
# Original del monitor
def new_data(conne: Engine) -> bool:
    queryo = text('select saved from hecho_atencion order by saved desc limit 1;')
    queryt = text(''' select date from dim_fecha where key_dim_fecha =
    (select key_fecha_atencion from hecho_atencion order by key_fecha_atencion desc limit 1) ;''')
    with conne.connect() as con:
        try:
            rs1 = con.execute(queryo)
            rs2 = con.execute(queryt)
            lastupdate = rs1.fetchone()
            lastdate = rs2.fetchone()
            if lastupdate is None or lastdate is None:
                return True
            if lastdate.date() > lastupdate:
                return True
            print(f'''No hay datos nuevos desde la ultima fecha de carga {lastupdate}''')
            return False
        except Exception as e:
            print('[*]', e)
            return False


