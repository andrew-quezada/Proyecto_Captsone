import psycopg2
from sqlalchemy import create_engine

def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="tienda_madrilena",
            user="postgres",
            password="2001",
            connect_timeout=10,
            sslmode="prefer"
        )
        print("Conexión a la base de datos establecida.")
        return conn
    except psycopg2.OperationalError as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada.")

