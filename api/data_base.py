import psycopg2
from psycopg2 import pool

DB_CONFIG = {
    "host": "201.23.68.219",
    "port": 5432,
    "dbname": "fiap_eml_db",
    "user": "postgres",
    "password": "(Pk3LfT7N;P5zfPc"
}

# Cria o pool de conexões
connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **DB_CONFIG
)

def get_connection():
    """Pega uma conexão do pool"""
    return connection_pool.getconn()

def release_connection(conn):
    """Devolve a conexão para o pool"""
    connection_pool.putconn(conn)
