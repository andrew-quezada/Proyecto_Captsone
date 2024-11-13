import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db.manejo_solicitudes import cargar_proveedores, obtener_codigo_unico, cargar_productos_por_proveedor,cargar_productos_por_proveedor_combobox
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class MenuSolicitudes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Solicitudes de Stock")

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir tamaño y posición de la ventana
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

        # Sección principal del título
        title_label = ttk.Label(self.root, text="Gestión de Solicitudes de Stock", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Frame contenedor de secciones
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Frame para Crear Solicitud
        frame_crear_solicitud = ttk.Labelframe(main_frame, text="Crear Nueva Solicitud", padding=10)
        frame_crear_solicitud.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Configuración de expansión de columnas y filas dentro del frame
        frame_crear_solicitud.columnconfigure(1, weight=1)
        frame_crear_solicitud.columnconfigure(3, weight=1)

        # Entrada para el código de solicitud
        ttk.Label(frame_crear_solicitud, text="Código de Solicitud").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_codigo = ttk.Entry(frame_crear_solicitud)
        self.entry_codigo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Obtener el código único y manejar errores
        codigo_unico = obtener_codigo_unico()
        if codigo_unico:
            self.entry_codigo.insert(0, codigo_unico)  # Insertar el código único al iniciar
        else:
            messagebox.showerror("Error", "No se pudo obtener el código único.")

        # Etiqueta y Combobox para seleccionar el proveedor
        LB_Proveedor = ttk.Label(frame_crear_solicitud, text="Proveedor:")
        LB_Proveedor.grid(row=0, column=2, padx=10, pady=5, sticky="e")

        self.combo_proveedor = ttk.Combobox(frame_crear_solicitud, state="readonly")
        self.combo_proveedor.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Seleccionar producto
        ttk.Label(frame_crear_solicitud, text="Producto:").grid(row=1, column=0, padx=5, pady=5)
        self.combo_producto = ttk.Combobox(frame_crear_solicitud, state="readonly")
        self.combo_producto.grid(row=1, column=1, padx=5, pady=5)

        # Etiqueta y entrada para solicitud de stock
        LB_Stock_solic = ttk.Label(frame_crear_solicitud, text="Cantidad Solicitada:")
        LB_Stock_solic.grid(row=1, column=2, padx=10, pady=5, sticky="e")
        self.entry_cod_barra = ttk.Entry(frame_crear_solicitud)
        self.entry_cod_barra.grid(row=1, column=3, padx=5, pady=5, sticky="ew")

        # Precio total
        ttk.Label(frame_crear_solicitud, text="Precio Total:").grid(row=2, column=0, padx=5, pady=5)
        self.label_precio_total = ttk.Label(frame_crear_solicitud, text="0")
        self.label_precio_total.grid(row=2, column=1, padx=5, pady=5)

        # Botón para crear solicitud
        ttk.Button(frame_crear_solicitud, text="Crear Solicitud").grid(row=3, columnspan=4, pady=10, sticky="ew")

        # Frame para ver productos
        self.frame_productos = ttk.Labelframe(main_frame, text="Productos por Proveedor", padding=10)
        self.frame_productos.pack(side=LEFT, fill=Y, expand=True, padx=1)
        
        # Tabla para mostrar los productos
        self.treeview_productos = ttk.Treeview(self.frame_productos, columns=("Empresa", "Nombre", "Stock", "Precio"), show="headings")
        self.treeview_productos.heading("Empresa", text="Empresa")
        self.treeview_productos.heading("Nombre", text="Nombre")
        self.treeview_productos.heading("Stock", text="Stock")
        self.treeview_productos.heading("Precio", text="Precio")

        # Crear scrollbar
        scrollbar = ttk.Scrollbar(self.frame_productos, orient="vertical", command=self.treeview_productos.yview)
        self.treeview_productos.configure(yscroll=scrollbar.set)

        # Empaquetar el Treeview y el Scrollbar
        self.treeview_productos.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Agregar evento de selección en el ComboBox
        self.combo_proveedor.bind("<<ComboboxSelected>>", self.mostrar_productos_combobox)

        # Llenar el Combobox con los proveedores al inicio
        self.cargar_proveedores_en_combobox()


    # Función para cargar los proveedores en el ComboBox
    def cargar_proveedores_en_combobox(self):
        proveedores = cargar_proveedores()  # Devuelve una lista de tuplas (id, nombre)
        
        # Crear un diccionario donde el nombre es la clave y el ID es el valor
        self.proveedores_dict = {f"{id_} - {nombre}": id_ for id_, nombre in proveedores}
        
        # Asignar los nombres al ComboBox
        self.combo_proveedor['values'] = list(self.proveedores_dict.keys())


    def cargar_productos_segun_proveedor_tabla(self, event):
        proveedor_seleccionado = self.combo_proveedor.get()

        if proveedor_seleccionado:
            try:
                id_proveedor = int(proveedor_seleccionado.split(" - ")[0])  # Extrae el ID del proveedor seleccionado
            except ValueError:
                messagebox.showerror("Error", "ID de proveedor no válido.")
                return

            productos = cargar_productos_por_proveedor(id_proveedor)  # Llama a tu función para cargar productos

            if productos:
                self.combo_producto['values'] = [f"{p[1]} - $ {p[2]}" for p in productos]  # Asigna nombre y precio
            else:
                self.combo_producto['values'] = []  # Limpia si no hay productos para este proveedor
                messagebox.showinfo("Información", "No hay productos disponibles para este proveedor.")
                self.combo_producto.set('')  # Limpia el ComboBox de productos si no hay productos
        
            self.combo_proveedor.bind("<<ComboboxSelected>>", self.mostrar_productos)

    # Función para cargar productos según el proveedor seleccionado y actualizar tanto el ComboBox como la tabla
    def mostrar_productos(self, event):
        proveedor_seleccionado = self.combo_proveedor.get()

        if proveedor_seleccionado not in self.proveedores_dict:
            messagebox.showerror("Error", "Proveedor no seleccionado correctamente.")
            return

        # Obtener el ID del proveedor
        proveedor_id = self.proveedores_dict[proveedor_seleccionado]

        # Llamar a la función para cargar los productos del proveedor
        productos = cargar_productos_por_proveedor(proveedor_id)

        if productos:
            # Actualizar el ComboBox de productos con los nombres de los productos
            self.productos_dict = {nombre: id_ for id_, nombre, precio in productos}
            self.combo_producto['values'] = list(self.productos_dict.keys())  # Solo los nombres
            
            # Limpiar la tabla de productos
            for item in self.treeview_productos.get_children():
                self.treeview_productos.delete(item)

            # Insertar los productos en la tabla
            for producto in productos:
                id_producto, nombre, precio = producto
                self.treeview_productos.insert("", "end", values=(id_producto, nombre, f"${precio}"))
        else:
            # Si no hay productos, limpiar el ComboBox y la tabla
            self.combo_producto['values'] = []
            for item in self.treeview_productos.get_children():
                self.treeview_productos.delete(item)
            messagebox.showinfo("Información", "No hay productos disponibles para este proveedor.")


    def mostrar_productos_combobox(self, event):
        # Obtener el nombre completo del proveedor seleccionado
        proveedor_seleccionado = self.combo_proveedor.get()
        
        # Comprobar si el proveedor seleccionado está en el diccionario
        if proveedor_seleccionado not in self.proveedores_dict:
            messagebox.showerror("Error", "Proveedor no seleccionado correctamente.")
            return

        # Obtener el ID del proveedor
        proveedor_id = self.proveedores_dict[proveedor_seleccionado]
        
        # Llamar a la función para cargar los productos correspondientes a ese proveedor
        productos = cargar_productos_por_proveedor_combobox(proveedor_id)

        # Si se cargan productos, los asignamos al ComboBox de productos
        if productos:
            self.productos_dict = {nombre: id_ for id_, nombre in productos}
            self.combo_producto['values'] = list(self.productos_dict.keys())  # Solo los nombres
        else:
            messagebox.showwarning("Advertencia", "No hay productos disponibles para este proveedor.")



if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MenuSolicitudes(root)
    root.mainloop()
