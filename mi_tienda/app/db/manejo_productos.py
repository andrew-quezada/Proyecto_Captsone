from settings import create_connection, close_connection
from tkinter import messagebox

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
    
    # Retornar una lista de tuplas (id, empresa)
    return proveedores

def cargar_categorias():
    conn = create_connection()
    categorias = []
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL para seleccionar el id y el nombre de la categoría
                sql = "SELECT id_categoria, nombre_categoria FROM categoria"
                cursor.execute(sql)
                categorias = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar categorías: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")
    
    # Retornar una lista de tuplas (id, nombre_categoria)
    return categorias


def enviar_producto(nombre, precio_compra, precio_venta, stock, cod_barra, id_categoria, proveedor_id):
    conn = create_connection()  # Llama a la función que crea la conexión
    if conn:
        try:
            with conn.cursor() as cursor:
                # SQL para insertar un nuevo producto
                sql = """
                INSERT INTO productos (nombre, precio_compra, precio_venta, stock, cod_barra, id_categoria, proveedor_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """  # Eliminar el último %s
                cursor.execute(sql, (nombre, precio_compra, precio_venta, stock, cod_barra, id_categoria, proveedor_id))
                conn.commit()  # Confirmar cambios
                messagebox.showinfo("Éxito", "Producto agregado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al insertar el producto: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

def cargar_productos(tree):
    conn = create_connection()
    productos = []
    if conn:
        try:
            with conn.cursor() as cursor:
                # Modificar la consulta para incluir los JOINs y las columnas adicionales
                cursor.execute("""
                    SELECT 
                        productos.id_producto,
                        productos.cod_barra,
                        productos.nombre,
                        categoria.nombre_categoria,
                        productos.precio_compra,
                        productos.precio_venta,
                        productos.stock,
                        TO_CHAR(productos.fecha_ingreso, 'DD/MM/YYYY') AS fecha_ingreso,
                        proveedores.empresa
                    FROM productos
                    LEFT JOIN categoria ON categoria.id_categoria = productos.id_categoria
                    LEFT JOIN proveedores ON proveedores.id = productos.proveedor_id
                """)
                
                productos = cursor.fetchall()  # Obtener todos los registros
                
                # Limpiar la tabla antes de cargar nuevos datos
                for row in tree.get_children():
                    tree.delete(row)

                # Insertar los datos en la tabla
                for row in productos:
                    tree.insert("", "end", values=row)

                print("Productos cargados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar productos: {e}")
        finally:
            close_connection(conn)
    else:
        messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")
    
    return productos  # Devuelve la lista de productos cargados
