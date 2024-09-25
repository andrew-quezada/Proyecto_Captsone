import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkFont
from datetime import datetime
from db.manejo_proveedores import enviar_datos, cargar_proveedores, eliminar_proveedor_db,modificar_proveedor_db
from settings import create_connection, close_connection
from tkinter import messagebox
from tkinter import simpledialog


class GenerarProveedor:
    def __init__(self, root):
        self.root = root
        self.root.title("Nuevo Proveedor")

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir el tamaño de la ventana como el 100% del tamaño de la pantalla
        window_width = screen_width
        window_height = screen_height

        # Establecer el tamaño y la posición de la ventana
        self.root.geometry(f"{window_width}x{window_height}+0+0")

        # Configurar el comportamiento de la ventana para que no se pueda redimensionar
        self.root.resizable(True, True)

        # Crear una fuente personalizada para el botón específico
        fuente_personalizada_boton_salida = tkFont.Font(family="Arial", size=10, weight="bold")

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

        # Botones 
        btn_enviar = ttk.Button(self.frame_insercion, text="Enviar", command=self.enviar_datos)
        btn_enviar.grid(row=5, column=0, padx=10, pady=20)

        btn_modificar = ttk.Button(self.frame_insercion, text="Modificar", command=self.modificar_proveedor)
        btn_modificar.grid(row=5, column=1, padx=5, pady=20)

        btn_eliminar = ttk.Button(self.frame_insercion, text="Eliminar", command=self.eliminar_proveedor)
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

        # Llamada automática a cargar_proveedores cuando se inicia la ventana
        self.cargar_proveedores()

        # Botón para cargar proveedores en el frame de la tabla
        btn_cargar = ttk.Button(self.frame_tabla, text="Cargar Proveedores", command=lambda: cargar_proveedores(self.tree))
        btn_cargar.grid(row=1, column=0, padx=10, pady=10)

        self.proveedor_id = None  # Variable para almacenar el ID del proveedor seleccionado

    def enviar_datos(self):
        # Obtener los valores de los campos de entrada
        nombre = self.entry_nombre.get()
        empresa = self.entry_empresa.get()
        correo = self.entry_email.get()
        telefono = self.entry_telefono.get()
        fecha_ingreso = self.entry_fecha.get()

        # Validar que no haya campos vacíos
        if not all([nombre, empresa, correo, telefono]):
            messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")
            return

        # Llamar a la función enviar_datos importada
        try:
            enviar_datos(nombre, empresa, correo, telefono)
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
            self.limpiar_campos()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el proveedor: {str(e)}")

    def limpiar_campos(self):
        self.entry_nombre.delete(0, 'end')
        self.entry_empresa.delete(0, 'end')
        self.entry_email.delete(0, 'end')
        self.entry_telefono.delete(0, 'end')
        self.entry_fecha.delete(0, 'end')
        self.entry_fecha.insert(0, datetime.now().strftime("%d/%m/%Y"))  # Restablecer a la fecha actual

    # Función para cargar los proveedores
    def cargar_proveedores(self):
        conn = create_connection()
        if conn:
            try:
                with conn.cursor() as cursor:
                    # Consulta SQL para obtener los proveedores
                    sql = "SELECT id, nombre_completo, empresa, email, telefono FROM proveedores"
                    cursor.execute(sql)
                    rows = cursor.fetchall()  # Obtener todos los proveedores

                    # Limpiar la tabla antes de cargar nuevos datos
                    for row in self.tree.get_children():
                        self.tree.delete(row)

                    # Insertar los datos en la tabla
                    for row in rows:
                        self.tree.insert("", "end", values=row)

                    print("Proveedores cargados correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar proveedores: {e}")
            finally:
                close_connection(conn)
        else:
            messagebox.showerror("Error de conexión", "No se pudo establecer la conexión a la base de datos.")

    def eliminar_proveedor(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este proveedor?")
            if confirmacion:
                proveedor_id = self.tree.item(selected_item)['values'][0]
                eliminar_proveedor_db(proveedor_id)  # Llamada a la función de eliminación
                self.tree.delete(selected_item)
                messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un proveedor para eliminar.")

    # Método para gestionar la modificación en la interfaz
    def modificar_proveedor(self):
        selected_item = self.tree.selection()
        if selected_item:
            proveedor_id = self.tree.item(selected_item)['values'][0]  # ID del proveedor seleccionado
            # Obtener los datos actuales
            nombre_actual = self.tree.item(selected_item)['values'][1]
            empresa_actual = self.tree.item(selected_item)['values'][2]
            email_actual = self.tree.item(selected_item)['values'][3]
            telefono_actual = self.tree.item(selected_item)['values'][4]

            # Mostrar un cuadro de diálogo para ingresar nuevos datos
            nuevo_nombre = simpledialog.askstring("Modificar Proveedor", "Nuevo Nombre Completo:", initialvalue=nombre_actual)
            nueva_empresa = simpledialog.askstring("Modificar Proveedor", "Nueva Empresa:", initialvalue=empresa_actual)
            nuevo_email = simpledialog.askstring("Modificar Proveedor", "Nuevo Email:", initialvalue=email_actual)
            nuevo_telefono = simpledialog.askstring("Modificar Proveedor", "Nuevo Teléfono:", initialvalue=telefono_actual)

            if nuevo_nombre and nueva_empresa and nuevo_email and nuevo_telefono:
                # Llamar a la función de modificación en la base de datos
                modificar_proveedor_db(proveedor_id, nuevo_nombre, nueva_empresa, nuevo_email, nuevo_telefono)
                # Actualizar el árbol
                self.tree.item(selected_item, values=(proveedor_id, nuevo_nombre, nueva_empresa, nuevo_email, nuevo_telefono))
            else:
                messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un proveedor para modificar.")

if __name__ == "__main__":    
    root = ttk.Window(themename="superhero")
    app = GenerarProveedor(root)
    root.mainloop()
