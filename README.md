# ETL MENSAJERIA

## Requirements installation 
 **if not exists environment create one**
```

python3 -m venv my_env

#unix systems
source my_env/bin/activate  

#win
python3 -m venv my_env

#cmd.exe
C:\> <venv>\Scripts\activate.bat

#PowerShell
PS C:\> <venv>\Scripts\Activate.ps1
```
your terminal should look like
```
(my_env) $
```
here you can install the packages by doing 
```
pip install -r requirements.txt
```

here you can install a missing package 
```
pip install psycopg2
pip install psycopg2-binary
```
structure of config.yml 
```
nombre_conexion:
  drivername: postgresql  
  user: postgres # su username
  password : valor_privado
  port: 5432 # pordefecto 
  host: localhost # la direccion a la base de datos
  dbname: colombia_saludable #nombre de la base de datos
```


## Database setup with Docker

**Requirements: have Docker and Docker Compose installed**

The project includes a `docker-compose.yml` at the root that sets up PostgreSQL and pgAdmin.

### Services

| Service | Port | URL |
|---|---|---|
| PostgreSQL | 5433 | `localhost:5433` |
| pgAdmin | 5050 | `http://localhost:5050` |

### Start the containers

```bash
docker compose up -d
```

### Create the destination database

```bash
docker exec -it etl_postgres psql -U postgres -c "CREATE DATABASE etl_mensajeria;"
```

### Connect pgAdmin to PostgreSQL

1. Go to `http://localhost:5050`
2. Login: email `admin@admin.com` / password `admin`
3. Right click **Servers** → **Register** → **Server**
4. **General** tab: Name `etl_postgres`
5. **Connection** tab:
   - Host: `etl_postgres`
   - Port: `5432`
   - Username: `postgres`
   - Password: `postgres`

### config.yml for Docker

```yaml
mensajeria_bd:
  drivername: postgresql
  dbname: mensajeria_bd
  user: postgres
  password: postgres
  host: localhost
  port: 5433

etl_mensajeria:
  drivername: postgresql
  dbname: etl_mensajeria
  user: postgres
  password: postgres
  host: localhost
  port: 5433
```

### Stop and remove containers

```bash
# Keep data
docker compose down

# Remove data (full reset)
docker compose down -v
```

## Run the ETL

```bash
python main.py
```