from settings import create_connection, close_connection
from tkinter import messagebox
import psycopg2

# Variable global para almacenar el id_usuario
usuario_actual = None

def obtener_id_empleado_actual(nombre_empleado):
    global usuario_actual  # Declaramos que vamos a modificar la variable global

    # Conectar a la base de datos
    conn = create_connection()
    if conn is None:
        print("Error de conexión a la base de datos.")
        return None

    try:
        cursor = conn.cursor()
        
        # Consulta SQL para obtener el id_usuario del empleado según su nombre
        query = """
            SELECT e.id_usuario
            FROM empleados e
            WHERE e.nombre = %s  -- Suponiendo que el nombre es un parámetro
        """
        
        # Ejecutar la consulta con el nombre del empleado
        cursor.execute(query, (nombre_empleado,))
        empleado = cursor.fetchone()
        
        conn.close()

        if empleado:
            # Almacenar el id_usuario en la variable global
            usuario_actual = empleado[0]  # Guardamos el id_usuario
            print(f"ID del empleado almacenado: {usuario_actual}")
            return usuario_actual
        else:
            print("Empleado no encontrado.")
            return None

    except psycopg2.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return None


def obtener_producto_por_codigo(codigo):
    conn = create_connection()  # Conectar a la base de datos
    if conn:
        try:
            cursor = conn.cursor()
            # Consulta para obtener el producto por código
            query = "SELECT cod_barra, nombre, precio_venta FROM productos WHERE cod_barra = %s"
            cursor.execute(query, (codigo,))
            producto = cursor.fetchone()

            cursor.close()
            conn.close()

            if producto:
                return {'cod_barra': producto[0],'nombre': producto[1],'precio_venta': producto[2]}
                 
            else:
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al obtener el producto: {e}")
            return None
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return None


    
def obtener_id_producto_por_nombre(nombre_producto):
    conn = create_connection()  # Crear la conexión a la base de datos
    if conn:
        try:
            cursor = conn.cursor()
            # Consulta para obtener el id_producto usando el nombre del producto
            query = "SELECT id_producto FROM productos WHERE nombre = %s"
            cursor.execute(query, (nombre_producto,))
            producto = cursor.fetchone()

            cursor.close()
            conn.close()

            if producto:
                return producto[0] and usuario_actual # Devolver el id_producto
            else:
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Hubo un error al obtener el id del producto: {e}")
            return None
    else:
        messagebox.showerror("Error", "No se pudo conectar a la base de datos.")
        return None
    


def registrar_venta(total, productos_vendidos,obtener_id_producto_por_nombre):
    # Obtener el id_empleado usando la variable global usuario_actual

    global usuario_actual
    print(usuario_actual)
    id_empleado = usuario_actual
    
    if id_empleado is None:
        # Si no se puede obtener el id_empleado, mostrar un error y salir
        print("Error: No se pudo obtener el ID del empleado.")
        messagebox.showerror("Error", "No se pudo obtener el ID del empleado.")
        return

    conn = create_connection()
    cursor = conn.cursor()

    try:
        # Iniciar transacción
        cursor.execute("BEGIN;")

        # Insertar en tabla `boletas`
        print(f"Ingresando boleta con total: {total} y empleado: {id_empleado}")
        cursor.execute("""
            INSERT INTO boletas (fecha, total, id_empleado)
            VALUES (CURRENT_TIMESTAMP, %s, %s)
            RETURNING id_boleta;
        """, (total, id_empleado))  # Aquí ya tenemos el id_empleado
        id_boleta = cursor.fetchone()[0]
        print(f"Boleta creada con ID: {id_boleta}")

        for producto in productos_vendidos:
            # Obtener el ID del producto a partir del nombre
            id_producto = obtener_id_producto_por_nombre(producto("nombre"))
            
            if id_producto is None:
                print(f"Producto no encontrado: {producto('nombre')}")
                messagebox.showerror("Error", f"Producto {producto('nombre')} no encontrado en la base de datos.")
                continue  # Saltar al siguiente producto en la lista

            cantidad = int(producto("cantidad", 0))
            precio_unitario = int(producto("precio_unitario", 0))

            print(f"Ingresando producto: {producto}")
            print(f"ID Producto: {id_producto}, Cantidad: {cantidad}, Precio Unitario: {precio_unitario}")

            # Insertar en detalle_boleta
            cursor.execute("""
                INSERT INTO detalle_boleta (id_boleta, id_producto, cantidad, precio_unitario)
                VALUES (%s, %s, %s, %s);
            """, (id_boleta, id_producto, cantidad, precio_unitario))

            # Actualizar el stock
            print(f"Actualizando stock para ID Producto: {id_producto}, Reducción: {cantidad}")
            cursor.execute("""
                UPDATE productos
                SET stock = stock - %s
                WHERE id_producto = %s;
            """, (cantidad, id_producto))

        # Confirmar transacción
        conn.commit()
        print("Venta registrada con éxito.")

    except Exception as e:
        # Si ocurre un error, deshacer los cambios
        conn.rollback()
        print(f"Error durante la transacción: {str(e)}")
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

    finally:
        cursor.close()
        conn.close()
