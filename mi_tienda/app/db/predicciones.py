import pandas as pd
from settings import create_connection,close_connection

def obtener_datos():
    """Obtiene datos de ventas desde la base de datos y los devuelve en un DataFrame."""
    conn = create_connection()
    if not conn:
        print("Error: No se pudo conectar a la base de datos.")
        return None

    try:
        consulta = """
            SELECT 
            b.fecha, 
            db.id_producto, 
            db.cantidad
            FROM 
            boletas b
            INNER JOIN detalle_boleta db ON b.id_boleta = db.id_boleta
            ORDER BY b.fecha;
        """
        # Obtiene los datos desde la base de datos
        datos = pd.read_sql_query(consulta, conn)

        if datos.empty:
            print("No se encontraron datos en la consulta.")
            return None

        # Asegurarse de que 'fecha' sea de tipo datetime con zona horaria UTC
        datos['fecha'] = pd.to_datetime(datos['fecha'], utc=True)

        # Convertir fechas a la zona horaria local (si es necesario)
        datos['fecha'] = datos['fecha'].dt.tz_convert('America/Santiago')

        # Agrupar por 'id_producto' y 'fecha', sumando las cantidades
        datos_agrupados = datos.groupby(['fecha', 'id_producto']).agg({'cantidad': 'sum'}).reset_index()

        # Verificación: mostrar las primeras filas
        print("Datos después de agrupar:")
        print(datos_agrupados.head())

        return datos_agrupados

    except Exception as e:
        print(f"Error al obtener los datos: {e}")
        return None

    finally:
        if conn:
            close_connection(conn)


def procesar_datos(datos):
    """Procesa los datos en un formato adecuado para análisis de series temporales."""
    if datos is None:
        print("No hay datos para procesar.")
        return None

    # Aquí los datos ya tienen 'fecha' como datetime gracias a obtener_datos
    # Solo asegurarnos de que los productos estén correctamente pivotados
    serie_temporal = datos.copy()

    # Rellenar valores faltantes con 0 (si un producto no tiene ventas en alguna fecha)
    serie_temporal.fillna(0, inplace=True)

    # Otras transformaciones o limpieza pueden ir aquí si es necesario

    return serie_temporal

#datos = obtener_datos()
#print ("datos obtenido:",datos)

#pr = procesar_datos(datos)

#print("datos procesados:",pr)