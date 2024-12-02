import psycopg2
from random import randint
from datetime import datetime, timedelta

# Conexión a la base de datos
def create_connection():
    return psycopg2.connect(
        host="localhost",  # Cambiar por tu host
        database="tienda_madrilena",  # Cambiar por tu base de datos
        user="postgrest",  # Cambiar por tu usuario
        password="2001"  # Cambiar por tu contraseña
    )

# Generar fechas aleatorias
def generar_fecha_aleatoria(inicio, fin):
    delta = fin - inicio
    dias_random = randint(0, delta.days)
    return inicio + timedelta(days=dias_random)

# Generar datos
def generar_boletas(cantidad_boletas):
    conn = create_connection()
    cursor = conn.cursor()

    # Fechas
    fecha_inicio = datetime(2020, 1, 1)
    fecha_fin = datetime.now()

    # Insertar boletas y detalles
    for _ in range(cantidad_boletas):
        # Generar datos para la boleta
        fecha = generar_fecha_aleatoria(fecha_inicio, fecha_fin)
        id_empleado = randint(1, 4)  # Empleados entre 1 y 4
        cantidad = randint(1, 10)  # Cantidad aleatoria entre 1 y 10
        precio_unitario = 3000  # Precio fijo para el producto
        total = cantidad * precio_unitario

        # Insertar en la tabla boletas
        cursor.execute(
            """
            INSERT INTO boletas (fecha, total, id_empleado)
            VALUES (%s, %s, %s) RETURNING id_boleta
            """,
            (fecha, total, id_empleado)
        )
        id_boleta = cursor.fetchone()[0]  # Obtener el id_boleta generado

        # Insertar en la tabla detalle_boleta
        cursor.execute(
            """
            INSERT INTO detalle_boleta (id_boleta, id_producto, cantidad, precio_unitario)
            VALUES (%s, %s, %s, %s)
            """,
            (id_boleta, 1, cantidad, precio_unitario)
        )

    conn.commit()
    print(f"{cantidad_boletas} boletas generadas con éxito.")
    cursor.close()
    conn.close()

# Ejecutar
if __name__ == "__main__":
    generar_boletas(500)  # Cambiar el número de boletas si es necesario