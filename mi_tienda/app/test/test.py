import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import psycopg2
from datetime import datetime

class ProveedoresTabla:
    def __init__(self, root):
        self.root = root
        self.root.title("Proveedores")

        # Configurar la ventana
        self.root.geometry("1000x500")
        self.root.resizable(True, True)

        # Configuración de columnas y filas para expandirse
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Crear dos frames: uno para la inserción y otro para la tabla
        self.frame_insercion = ttk.Frame(self.root)
        self.frame_insercion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_tabla = ttk.Frame(self.root)
        self.frame_tabla.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        # ---- Frame de Inserción de Datos ----
        LB_Nombre = ttk.Label(self.frame_insercion, text="Nombre Completo:")
        LB_Nombre.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        LB_Email = ttk.Label(self.frame_insercion, text="Email:")
        LB_Email.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        LB_Telefono = ttk.Label(self.frame_insercion, text="Teléfono:")
        LB_Telefono.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        LB_Empresa = ttk.Label(self.frame_insercion, text="Empresa:")
        LB_Empresa.grid(row=3, column=0, padx=10, pady=10, sticky="w")

        LB_Fecha = ttk.Label(self.frame_insercion, text="Fecha de Ingreso:")
        LB_Fecha.grid(row=4, column=0, padx=10, pady=10, sticky="w")

        # Entradas
        self.entry_nombre = ttk.Entry(self.frame_insercion)
        self.entry_nombre.grid(row=0, column=1, padx=10, pady=10)

        self.entry_email = ttk.Entry(self.frame_insercion)
        self.entry_email.grid(row=1, column=1, padx=10, pady=10)

        self.entry_telefono = ttk.Entry(self.frame_insercion)
        self.entry_telefono.grid(row=2, column=1, padx=10, pady=10)

        self.entry_empresa = ttk.Entry(self.frame_insercion)
        self.entry_empresa.grid(row=3, column=1, padx=10, pady=10)

        self.entry_fecha = ttk.Entry(self.frame_insercion)
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))  # Prellenar con la fecha actual
        self.entry_fecha.grid(row=4, column=1, padx=10, pady=10)

        # Botones para enviar, modificar y eliminar
        btn_enviar = ttk.Button(self.frame_insercion, text="Enviar", command=self.enviar_datos)
        btn_enviar.grid(row=5, column=0, padx=10, pady=20)

        btn_modificar = ttk.Button(self.frame_insercion, text="Modificar", command=self.modificar_datos)
        btn_modificar.grid(row=5, column=1, padx=5, pady=20)

        btn_eliminar = ttk.Button(self.frame_insercion, text="Eliminar", command=self.eliminar_datos)
        btn_eliminar.grid(row=5, column=2, padx=5, pady=20)

        # ---- Frame de la Tabla ----
        # Crear la tabla (Treeview) para mostrar los proveedores
        self.tree = ttk.Treeview(self.frame_tabla, columns=("id", "nombre_completo", "empresa", "correo", "telefono"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("nombre_completo", text="Nombre del proveedor")
        self.tree.heading("empresa", text="Empresa")
        self.tree.heading("correo", text="Correo")
        self.tree.heading("telefono", text="Teléfono")

        self.tree.column("id", width=50)
        self.tree.column("nombre_completo", width=150)
        self.tree.column("empresa", width=100)
        self.tree.column("correo", width=200)
        self.tree.column("telefono", width=100)

        self.tree.grid(row=0, column=0, sticky="nsew")  # Hacer que la tabla se expanda

        # Configurar el frame para que la tabla también se expanda
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        # Botón para cargar proveedores en el frame de la tabla
        btn_cargar = ttk.Button(self.frame_tabla, text="Cargar Proveedores", command=self.cargar_proveedores)
        btn_cargar.grid(row=1, column=0, padx=10, pady=10)

        # Cargar proveedores inicialmente
        self.cargar_proveedores()

        # Enlazar el evento de selección en la tabla
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_proveedor)

        self.proveedor_id = None  # Variable para almacenar el ID del proveedor seleccionado

    def cargar_proveedores(self):
        # Limpiar la tabla antes de cargar nuevos datos
        for i in self.tree.get_children():
            self.tree.delete(i)

        conn = self.connect_db()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("SELECT * FROM proveedores")
            for row in cursor.fetchall():
                self.tree.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron cargar los proveedores: {e}")
        finally:
            cursor.close()
            conn.close()

    def seleccionar_proveedor(self, event):
        try:
            item = self.proveedores.item(self.proveedores.focus())
            self.proveedor_id = item['values'][0]
            self.entry_nombre.delete(0, tk.END)
            self.entry_nombre.insert(0, item['values'][1])
            self.entry_empresa.delete(0, tk.END)
            self.entry_empresa.insert(0, item['values'][3])
            self.entry_email.delete(0, tk.END)
            self.entry_email.insert(0, item['values'][2])
            self.entry_telefono.delete(0, tk.END)
            self.entry_telefono.insert(0, item['values'][4])
            
            # Verificar si la fecha es una cadena o un objeto datetime
            fecha_ingreso = item['values'][5]
            if isinstance(fecha_ingreso, str):
                self.entry_fecha.delete(0, tk.END)
                self.entry_fecha.insert(0, fecha_ingreso)  # Ya está en formato de cadena
            else:
                self.entry_fecha.delete(0, tk.END)
                self.entry_fecha.insert(0, fecha_ingreso.strftime("%d/%m/%Y"))  # Formato si fuera datetime
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al seleccionar el proveedor: {e}")

    def enviar_datos(self):
        # Obtener los datos ingresados
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        empresa = self.entry_empresa.get()
        fecha = self.entry_fecha.get()

        # Validación básica
        if not nombre or not email or not telefono or not empresa:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Convertir la fecha a formato de base de datos
        try:
            fecha_registro = datetime.strptime(fecha, "%d/%m/%Y").date()
            self.insertar_proveedor(nombre, empresa, email, telefono, fecha_registro)
            messagebox.showinfo("Éxito", "Los datos han sido guardados correctamente.")
            self.cargar_proveedores()  # Refrescar la tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar en la base de datos: {e}")

    def modificar_datos(self):
        if self.proveedor_id is None:
            messagebox.showerror("Error", "Seleccione un proveedor para modificar.")
            return

        # Obtener los datos ingresados
        nombre = self.entry_nombre.get()
        email = self.entry_email.get()
        telefono = self.entry_telefono.get()
        empresa = self.entry_empresa.get()
        fecha = self.entry_fecha.get()

        # Validación básica
        if not nombre or not email or not telefono or not empresa:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        # Convertir la fecha a formato de base de datos
        try:
            fecha_registro = datetime.strptime(fecha, "%d/%m/%Y").date()
            self.actualizar_proveedor(self.proveedor_id, nombre, empresa, email, telefono, fecha_registro)
            messagebox.showinfo("Éxito", "Los datos han sido modificados correctamente.")
            self.cargar_proveedores()  # Refrescar la tabla
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo modificar en la base de datos: {e}")

    def eliminar_datos(self):
        if self.proveedor_id is None:
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este proveedor?")
        if confirmacion:
            try:
                self.borrar_proveedor(self.proveedor_id)
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
                self.cargar_proveedores()  # Refrescar la tabla
                self.proveedor_id = None  # Reiniciar la selección
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar de la base de datos: {e}")

    def insertar_proveedor(self, nombre, empresa, email, telefono, fecha_registro):
        conn = self.connect_db()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO proveedores (nombre_completo, empresa, correo, telefono, fecha_ingreso) VALUES (%s, %s, %s, %s, %s)", 
                           (nombre, empresa, email, telefono, fecha_registro))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def actualizar_proveedor(self, proveedor_id, nombre, empresa, email, telefono, fecha_registro):
        conn = self.connect_db()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("UPDATE proveedores SET nombre_completo=%s, empresa=%s, correo=%s, telefono=%s, fecha_ingreso=%s WHERE id=%s", 
                           (nombre, empresa, email, telefono, fecha_registro, proveedor_id))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def borrar_proveedor(self, proveedor_id):
        conn = self.connect_db()
        if conn is None:
            return

        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM proveedores WHERE id=%s", (proveedor_id,))
            conn.commit()
        except Exception as e:
            raise e
        finally:
            cursor.close()
            conn.close()

    def connect_db(self):
        try:
            conn = psycopg2.connect(database="tienda_madrilena", user="postgres", password="2001", host="localhost", port="5432")
            return conn
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

if __name__ == "__main__":
    root = tk.Tk()
    app = ProveedoresTabla(root)
    root.mainloop()
