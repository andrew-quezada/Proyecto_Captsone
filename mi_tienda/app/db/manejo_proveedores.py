from settings import create_connection, close_connection
from tkinter import messagebox

# Funcion de agregar proveedor 
def enviar_datos(nombre_completo, empresa, email, telefono):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL para insertar un nuevo proveedor
                sql = """
                INSERT INTO proveedores (nombre_completo, empresa, email, telefono)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(sql, (nombre_completo, empresa, email, telefono))
                conn.commit()  # Confirmar cambios
                messagebox.showinfo("Éxito", "Proveedor agregado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el proveedor: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

# Funcion cargar proveedor 
def cargar_proveedores(tree):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Consulta SQL para obtener los proveedores
                sql = "SELECT id, nombre_completo, empresa, email, telefono FROM proveedores"
                cursor.execute(sql)
                rows = cursor.fetchall()  # Obtener todos los proveedores

                # Limpiar la tabla antes de cargar nuevos datos
                for row in tree.get_children():
                    tree.delete(row)

                # Insertar los datos en la tabla
                for row in rows:
                    tree.insert("", "end", values=row)

                print("Proveedores cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar proveedores: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")



# Función para eliminar proveedor
def eliminar_proveedor_db(proveedor_id):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # Eliminar proveedor usando su ID
                sql = "DELETE FROM proveedores WHERE id = %s"
                cursor.execute(sql, (proveedor_id,))
                conn.commit()
                print(f"Proveedor con ID {proveedor_id} eliminado.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar proveedor: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")


# Función para modificar proveedor
def modificar_proveedor_db(proveedor_id, nombre_completo, empresa, email, telefono):
    conn = create_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL para actualizar un proveedor existente
                sql = """
                UPDATE proveedores
                SET nombre_completo = %s, empresa = %s, email = %s, telefono = %s
                WHERE id = %s
                """
                cursor.execute(sql, (nombre_completo, empresa, email, telefono, proveedor_id))
                conn.commit()
                messagebox.showinfo("Éxito", "Proveedor modificado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al modificar el proveedor: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

