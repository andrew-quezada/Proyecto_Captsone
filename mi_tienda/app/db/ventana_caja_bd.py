from settings import create_connection, close_connection
from tkinter import messagebox

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
