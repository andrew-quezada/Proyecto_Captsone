import psycopg2

def create_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="tienda_madrilena",
            user="postgres",
            password="2001",
            connect_timeout=10,
            sslmode="prefer",
            client_encoding="UTF8"
        )
        print("Conexión a la base de datos establecida.")
        return conn
    except psycopg2.OperationalError as e:
        print("Error al conectar a la base de datos.")
        print(f"Detalles del error: {e}")
        return None

def close_connection(conn):
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada.")
    else:
        print("No hay conexión activa para cerrar.")