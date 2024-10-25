import ttkbootstrap as ttk
from tkinter import font as tkFont
import tkinter as tk
from db.manejo_productos import enviar_producto, cargar_proveedores, cargar_categorias,cargar_productos,eliminar_producto_db,modificar_producto_db
from tkinter import messagebox
from tkinter import simpledialog

class GenerarProducto:
    def __init__(self, root):  
        self.root = root
        self.root.title("Nuevo Producto")

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
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=3)

        # Crear dos frames: uno para la inserción (arriba) y otro para la tabla (abajo)
        self.frame_insercion = ttk.Frame(self.root)
        self.frame_insercion.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.frame_tabla = ttk.Frame(self.root)
        self.frame_tabla.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # ---- Frame de Inserción de Datos ----
        LB_CodBarra = ttk.Label(self.frame_insercion, text="Código de Barras:")
        LB_CodBarra.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        LB_Nombre = ttk.Label(self.frame_insercion, text="Nombre del Producto:")
        LB_Nombre.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        LB_Categoria = ttk.Label(self.frame_insercion, text="Categoría:")
        LB_Categoria.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        LB_PrecioCompra = ttk.Label(self.frame_insercion, text="Precio de Compra:")
        LB_PrecioCompra.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        LB_PrecioVenta = ttk.Label(self.frame_insercion, text="Precio de Venta:")
        LB_PrecioVenta.grid(row=0, column=2, padx=10, pady=10, sticky="w")

        LB_Stock = ttk.Label(self.frame_insercion, text="Stock:")
        LB_Stock.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        LB_Proveedor = ttk.Label(self.frame_insercion, text="Proveedor:")
        LB_Proveedor.grid(row=0, column=3, padx=10, pady=10, sticky="w")

        # Entradas
        self.entry_cod_barra = ttk.Entry(self.frame_insercion)
        self.entry_cod_barra.grid(row=1, column=0, padx=10, pady=10)

        self.entry_nombre = ttk.Entry(self.frame_insercion)
        self.entry_nombre.grid(row=3, column=0, padx=10, pady=10)

        self.combo_categoria = ttk.Combobox(self.frame_insercion)
        self.combo_categoria.grid(row=1, column=1, padx=10, pady=10)

        self.entry_precio_compra = ttk.Entry(self.frame_insercion)
        self.entry_precio_compra.grid(row=3, column=1, padx=10, pady=10)

        self.entry_precio_venta = ttk.Entry(self.frame_insercion)
        self.entry_precio_venta.grid(row=1, column=2, padx=10, pady=10)

        self.entry_stock = ttk.Entry(self.frame_insercion)
        self.entry_stock.grid(row=3, column=2, padx=10, pady=10)

        self.combo_proveedor = ttk.Combobox(self.frame_insercion)
        self.combo_proveedor.grid(row=1, column=3, padx=10, pady=10)

        # Botones 
        btn_enviar = ttk.Button(self.frame_insercion, text="Enviar", command=self.agregar_producto)
        btn_enviar.grid(row=0, column=6, padx=10, pady=20)

        btn_modificar = ttk.Button(self.frame_insercion, text="Modificar", command=self.modificar_producto)
        btn_modificar.grid(row=1, column=6, padx=5, pady=20)

        btn_eliminar = ttk.Button(self.frame_insercion, text="Eliminar", command=self.eliminar_producto)
        btn_eliminar.grid(row=2, column=6, padx=5, pady=20)

        btn_regresar = ttk.Button(self.frame_insercion, text="Regresar")
        btn_regresar.grid(row=3, column=6, padx=5, pady=20)

        # ---- Frame de la Tabla ----
        # Aquí eliminamos la segunda declaración de self.frame_tabla

        # Definir las columnas del Treeview
        self.tree = ttk.Treeview(self.frame_tabla, columns=("id", "codigo", "nombre", "categoria", "precio_compra", "precio_venta", "stock", "fecha_ingreso", "proveedor"), show="headings")
        
        # Configuración de encabezados
        self.tree.heading("id", text="ID")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Nombre del Producto")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("precio_compra", text="Precio de Compra")
        self.tree.heading("precio_venta", text="Precio de Venta")
        self.tree.heading("stock", text="Stock")
        self.tree.heading("fecha_ingreso", text="Fecha de Ingreso")
        self.tree.heading("proveedor", text="Proveedor")

        # Configuración de columnas
        self.tree.column("id", width=50, stretch=tk.YES)
        self.tree.column("codigo", width=100)
        self.tree.column("nombre", width=100)
        self.tree.column("categoria", width=100)
        self.tree.column("precio_compra", width=100)
        self.tree.column("precio_venta", width=100)
        self.tree.column("stock", width=100)
        self.tree.column("fecha_ingreso", width=100)
        self.tree.column("proveedor", width=100)

        # Colocar el Treeview en el grid
        self.tree.grid(row=0, column=0, sticky="nsew")

        # Configurar el frame para que la tabla también se expanda
        self.frame_tabla.grid_rowconfigure(0, weight=1)
        self.frame_tabla.grid_columnconfigure(0, weight=1)

        # Cargar los datos al iniciar
        self.cargar_datos()

        # Botón para cargar productos en el frame de la tabla
        btn_cargar = ttk.Button(self.frame_tabla, text="Cargar Productos", command=self.cargar_datos)
        btn_cargar.grid(row=1, column=0, padx=10, pady=10)

        # Botón para cargar productos en el frame de la tabla
        btn_cargar = ttk.Button(self.frame_tabla, text="Cargar Productos", command=self.cargar_datos)
        btn_cargar.grid(row=1, column=0, padx=10, pady=10)

    def cargar_datos(self):
            # Llamar a cargar_productos y pasarle el Treeview
            productos = cargar_productos(self.tree)
            
            # Limpiar el Treeview antes de cargar nuevos datos
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Insertar productos en el Treeview
            for producto in productos:
                self.tree.insert("", tk.END, values=producto)

            # Llenar el Combobox con los proveedores al inicio
            self.cargar_proveedores_en_combobox()
            self.cargar_categorias_en_combobox()


    def cargar_proveedores_en_combobox(self):
        proveedores = cargar_proveedores()  # Debería devolver una lista de tuplas (id, nombre)
        self.proveedores_dict = {nombre: id_ for id_, nombre in proveedores}
        self.combo_proveedor['values'] = list(self.proveedores_dict.keys())  # Solo nombres

    def cargar_categorias_en_combobox(self):
        categorias = cargar_categorias()  # Debería devolver una lista de tuplas (id, nombre)
        self.categorias_dict = {nombre: id_ for id_, nombre in categorias}
        self.combo_categoria['values'] = list(self.categorias_dict.keys())  # Solo nombres
 
    def agregar_producto(self):
        # Obtener los datos de los widgets
        nombre = self.entry_nombre.get()
        proveedor_nombre = self.combo_proveedor.get()
        categoria_nombre = self.combo_categoria.get()

        # Verificar que no haya campos vacíos
        if not nombre or not proveedor_nombre or not categoria_nombre:
            messagebox.showerror("Error", "Todos los campos son obligatorios")
            return

        # Manejar errores en las entradas numéricas
        try:
            precio_compra = int(self.entry_precio_compra.get())
            precio_venta = int(self.entry_precio_venta.get())
            stock = int(self.entry_stock.get())
            codigo_barra = int(self.entry_cod_barra.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa valores numéricos válidos en los campos de precio, stock y código de barra")
            return

        # Obtener los ids de proveedor y categoría
        id_proveedor = self.proveedores_dict.get(proveedor_nombre)
        id_categoria = self.categorias_dict.get(categoria_nombre)

        # Verificar que se hayan seleccionado proveedor y categoría correctamente
        if id_proveedor is None or id_categoria is None:
            messagebox.showerror("Error", "Selecciona un proveedor y una categoría válidos")
            return

        # Código para insertar el producto
        try:
            enviar_producto(nombre, precio_compra, precio_venta, stock, codigo_barra, id_categoria, id_proveedor)
            messagebox.showinfo("Éxito", "Producto agregado exitosamente")

        except Exception as e:
            print(f"Error inesperado: {e}")
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")


    def eliminar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar este producto?")
            if confirmacion:
                producto_id = self.tree.item(selected_item)['values'][0]
                eliminar_producto_db(producto_id)  # Llamada a la función de eliminación
                self.tree.delete(selected_item)
                messagebox.showinfo("Éxito", "producto eliminado correctamente.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, seleccione un producto para eliminar.")

    def modificar_producto(self):
        selected_item = self.tree.selection()
        if selected_item:
            id_producto = self.tree.item(selected_item)['values'][0]  
            # Obtener los datos actuales
            cod_barra_actual = self.tree.item(selected_item)['values'][1]
            nombre_actual = self.tree.item(selected_item)['values'][2]
            categoria_actual = self.tree.item(selected_item)['values'][3]
            precio_compra_actual = self.tree.item(selected_item)['values'][4]
            precio_venta_actual = self.tree.item(selected_item)['values'][5]
            stock_actual = self.tree.item(selected_item)['values'][6]
            proveedor_actual = self.tree.item(selected_item)['values'][8]

            # Establecer valores iniciales en los Combobox
            self.combo_categoria.set(categoria_actual)
            self.combo_proveedor.set(proveedor_actual)

            self.cargar_proveedores_en_combobox()
            self.cargar_categorias_en_combobox()

            # Asegurarse de que los Combobox sean visibles y actualizados
            self.combo_categoria.update_idletasks()
            self.combo_proveedor.update_idletasks()

            # Mostrar un cuadro de diálogo para ingresar nuevos datos
            nuevo_codigo = simpledialog.askstring("Modificar producto", "Nuevo código:", initialvalue=cod_barra_actual)
            nuevo_nombre = simpledialog.askstring("Modificar producto", "Nuevo nombre del producto:", initialvalue=nombre_actual)
            nueva_categoria = self.combo_categoria.get()
            nuevo_precio_compra = simpledialog.askstring("Modificar producto", "Nuevo precio de compra:", initialvalue=precio_compra_actual)
            nuevo_precio_venta = simpledialog.askstring("Modificar producto", "Nuevo precio de venta:", initialvalue=precio_venta_actual)
            nuevo_stock = simpledialog.askstring("Modificar producto", "Nuevo stock:", initialvalue=stock_actual)
            nuevo_proveedor = self.combo_proveedor.get()

            # Verificar que no haya campos vacíos
            if not nuevo_codigo or not nuevo_nombre or not nueva_categoria or not nuevo_precio_compra or not nuevo_precio_venta or not nuevo_stock or not nuevo_proveedor:
                messagebox.showerror("Error", "Todos los campos son obligatorios")
                return

            # Convertir valores a tipos adecuados
            try:
                nuevo_precio_compra = float(nuevo_precio_compra)
                nuevo_precio_venta = float(nuevo_precio_venta)
                nuevo_stock = int(nuevo_stock)
            except ValueError:
                messagebox.showerror("Error", "Precio y stock deben ser números válidos")
                return

            # Actualiza el producto en la base de datos
            try:
                modificar_producto_db(id_producto, nuevo_codigo, nuevo_nombre, self.categorias_dict[nueva_categoria], nuevo_precio_compra, nuevo_precio_venta, nuevo_stock, self.proveedores_dict[nuevo_proveedor])
                messagebox.showinfo("Éxito", "Producto modificado exitosamente")
                self.cargar_datos()  # Recargar datos para mostrar los cambios
            except Exception as e:
                print(f"Error inesperado: {e}")
                messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")



# Aquí deberías inicializar la ventana principal de la aplicación
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # Cambia el tema según tus preferencias
    app = GenerarProducto(root)
    root.mainloop()
