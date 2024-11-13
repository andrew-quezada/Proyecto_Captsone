from settings import create_connection, close_connection
from tkinter import messagebox
import psycopg2 
from tkinter import messagebox
from datetime import datetime

def cargar_proveedores():
    conn = create_connection()  # Llama a la función que crea la conexión
    proveedores = []
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL para seleccionar el id y la empresa
                sql = "SELECT id, empresa FROM proveedores"
                cursor.execute(sql)
                proveedores = cursor.fetchall()  # Obtener todos los registros
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proveedores: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

    return proveedores

def cargar_productos_por_proveedor_combobox(id_proveedor):
    conn = create_connection()
    productos = []
    if conn:
        try:
            with conn.cursor() as cursor:
                sql = "SELECT id_producto, nombre FROM productos WHERE proveedor_id = %s"
                cursor.execute(sql, (id_proveedor,))
                productos = cursor.fetchall()  # Obtiene todos los productos para el proveedor
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
        finally:
            close_connection(conn)
    return productos


def obtener_codigo_unico():
    fecha_actual = datetime.now().date()
    fecha_formateada = fecha_actual.strftime("%d%m%Y")  # Formato: DDMMYYYY

    conn = create_connection()  # Usar create_connection para establecer la conexión
    if not conn:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")
        return None  # Si no hay conexión, salir de la función

    try:
        with conn.cursor() as cursor:
            # Intentar obtener el último número para la fecha actual
            cursor.execute("SELECT ultimo_numero FROM codigo_solicitudes WHERE fecha = %s;", (fecha_actual,))
            resultado = cursor.fetchone()

            if resultado:
                ultimo_numero = resultado[0] + 1  # Incrementar el número
            else:
                ultimo_numero = 1  # Comenzar con 1 si no existe la fecha

            # Insertar o actualizar el número en la base de datos
            if resultado:
                cursor.execute("UPDATE codigo_solicitudes SET ultimo_numero = %s WHERE fecha = %s;", (ultimo_numero, fecha_actual))
            else:
                cursor.execute("INSERT INTO codigo_solicitudes (fecha, ultimo_numero) VALUES (%s, %s);", (fecha_actual, ultimo_numero))

    except Exception as e:
        messagebox.showerror("Error", f"Error al obtener el código único: {e}")
        return None  # En caso de error, salir de la función
    finally:
        close_connection(conn)  # Asegúrate de cerrar la conexión al final

    # Formar el código único
    codigo_unico = f"{fecha_formateada}{str(ultimo_numero).zfill(3)}"  # Completar con ceros a la izquierda
    return codigo_unico


def cargar_productos_por_proveedor(proveedor_id):
    if proveedor_id is None:
        messagebox.showerror("Error", "ID de proveedor no válido.")
        return []

    conn = create_connection()  # Llama a la función que crea la conexión
    productos = []
    if conn:
        try:
            with conn.cursor() as cursor:
                # Consulta SQL para obtener productos por proveedor
                sql = """
                SELECT proveedores.empresa, productos.nombre, productos.stock, productos.precio_venta
                FROM proveedores
                RIGHT JOIN productos ON productos.proveedor_id = proveedores.id
                WHERE proveedores.id = %s
                """
                cursor.execute(sql, (proveedor_id,))
                productos = cursor.fetchall()  # Obtener todos los registros
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

    # Retornar una lista de tuplas (empresa, nombre, stock, precio_venta)
    return productos  # Puedes modificar esto para devolver más metadatos si es necesario

def crear_solicitud(codigo_solicitud, proveedor_id, cantidad, producto_id):
    conn = create_connection()  # Define esta función para obtener tu conexión a la base de datos
    cursor = conn.cursor()
    
    # Obtener el precio del producto
    cursor.execute("SELECT precio FROM productos WHERE id = %s", (producto_id,))
    precio = cursor.fetchone()
    
    if precio:
        precio_total = precio[0] * cantidad
        
        # Insertar la solicitud
        cursor.execute("""
            INSERT INTO solicitudes_productos (codigo_solicitud, proveedor_id, cantidad, precio_total)
            VALUES (%s, %s, %s, %s)
        """, (codigo_solicitud, proveedor_id, cantidad, precio_total))
        
        conn.commit()
        print("Solicitud creada correctamente.")
    else:
        print("Producto no encontrado.")
    
    cursor.close()
    conn.close()

