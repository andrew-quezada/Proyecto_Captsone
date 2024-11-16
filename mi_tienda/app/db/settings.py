import psycopg2

def create_connection():
    try:
        conn = psycopg2.connect(
            host="cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            port=5432,
            dbname="d2ildjn7jaslge",
            user="u8eh61nricdrqi",
            password="pd62d577f9f5f845c0511ff339f090e7d7a06e20aa5b4a950bddd74ed76703e55",
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

            #host="cf980tnnkgv1bp.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
            #port=5432,
            #dbname="d2ildjn7jaslge",
            #user="u8eh61nricdrqi",
            #password="pd62d577f9f5f845c0511ff339f090e7d7a06e20aa5b4a950bddd74ed76703e55",