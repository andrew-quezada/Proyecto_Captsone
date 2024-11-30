import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db.manejo_solicitudes import obtener_stock_por_paquete,cargar_proveedores, obtener_codigo_unico , cargar_productos_por_proveedor_combobox
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import os


class MenuSolicitudes:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestión de Solicitudes de Stock")

        # Configuración de ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)

        # Título
        title_label = ttk.Label(self.root, text="Gestión de Solicitudes de Stock", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)

        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Frame para crear solicitudes
        frame_crear_solicitud = ttk.Labelframe(main_frame, text="Crear Nueva Solicitud", padding=10)
        frame_crear_solicitud.pack(side=LEFT, fill=BOTH, expand=True, padx=10, pady=10)

        # Entrada para el código de solicitud
        ttk.Label(frame_crear_solicitud, text="Código de Solicitud").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_codigo = ttk.Entry(frame_crear_solicitud)
        self.entry_codigo.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        # Obtener el código único incremental y manejar errores
        codigo_unico = obtener_codigo_unico()
        if codigo_unico:
            self.entry_codigo.insert(0, codigo_unico)  # Insertar el código único al iniciar
        else:
            messagebox.showerror("Error", "No se pudo generar el código único.")


        # Proveedores y productos
        ttk.Label(frame_crear_solicitud, text="Proveedor:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.combo_proveedor = ttk.Combobox(frame_crear_solicitud, state="readonly")
        self.combo_proveedor.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

        ttk.Label(frame_crear_solicitud, text="Producto:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.combo_producto = ttk.Combobox(frame_crear_solicitud, state="readonly")
        self.combo_producto.grid(row=5, column=0, padx=5, pady=5, sticky="ew")

        # Cantidad solicitada
        ttk.Label(frame_crear_solicitud, text="Cantidad Solicitada:").grid(row=6, column=0, padx=5, pady=5, sticky="e")
        self.entry_cantidad = ttk.Entry(frame_crear_solicitud)
        self.entry_cantidad.grid(row=7, column=0, padx=5, pady=5, sticky="ew")

        # Crear los botones para sumar y restar stock
        btn_sumar = ttk.Button(frame_crear_solicitud, text="+", command=lambda: self.sumar_stock())
        btn_sumar.grid(row=7, column=2, padx=5, pady=5)

        btn_restar = ttk.Button(frame_crear_solicitud, text="-", command=lambda: self.restar_stock())
        btn_restar.grid(row=7, column=3, padx=5, pady=5)


        # Botón para agregar producto
        btn_agregar = ttk.Button(frame_crear_solicitud, text="Agregar Producto", command=self.agregar_producto)
        btn_agregar.grid(row=8, column=0, columnspan=2, pady=10, sticky="ew")

        # Botón para generar solicitud
        btn_generar_pdf = ttk.Button(frame_crear_solicitud,text="Generar PDF",command=self.preparar_datos_y_generar_pdf)
        btn_generar_pdf.grid(row=9, column=0, pady=10, padx=10, columnspan=2)

        # Tabla para mostrar los productos agregados
        frame_tabla = ttk.Labelframe(main_frame, text="Productos Seleccionados", padding=10)
        frame_tabla.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.treeview_tabla = ttk.Treeview(frame_tabla, columns=("Producto", "Cantidad"), show="headings")
        self.treeview_tabla.heading("Producto", text="Producto")
        self.treeview_tabla.heading("Cantidad", text="Cantidad")
        self.treeview_tabla.pack(fill=BOTH, expand=True)

        # Cargar proveedores
        self.cargar_proveedores_en_combobox()
        self.combo_proveedor.bind("<<ComboboxSelected>>", self.cargar_productos_segun_proveedor)
        self.combo_producto.bind("<<ComboboxSelected>>", self.seleccionar_producto)

    def cargar_proveedores_en_combobox(self):
        proveedores = cargar_proveedores()
        self.proveedores_dict = {f"{id_} - {nombre}": id_ for id_, nombre in proveedores}
        self.combo_proveedor['values'] = list(self.proveedores_dict.keys())

    def cargar_productos_segun_proveedor(self, event):
        proveedor_seleccionado = self.combo_proveedor.get()
        if proveedor_seleccionado not in self.proveedores_dict:
            return
        proveedor_id = self.proveedores_dict[proveedor_seleccionado]
        productos = cargar_productos_por_proveedor_combobox(proveedor_id)
        self.productos_dict = {nombre: id_ for id_, nombre in productos}
        self.combo_producto['values'] = list(self.productos_dict.keys())

    def seleccionar_producto(self, event):
        producto_nombre = self.combo_producto.get()  # Nombre del producto seleccionado
        if producto_nombre not in self.productos_dict:
            return  # Si el producto no está en el diccionario, salimos de la función
        producto_id = self.productos_dict[producto_nombre]  # Obtenemos el ID del producto seleccionado

        stock_por_paquete = obtener_stock_por_paquete(producto_id)  # Obtener el stock por paquete usando el ID del producto

        if stock_por_paquete:
            self.entry_cantidad.delete(0, ttk.END)  # Limpiar el campo de cantidad
            self.entry_cantidad.insert(0, str(stock_por_paquete))  # Insertar el stock por paquete en el campo de cantidad


    def obtener_stock_por_paquete(self, producto_id):
        # Llamamos a la consulta que nos da el stock por paquete
        stock_por_paquete = obtener_stock_por_paquete(producto_id)  # Llama a la función definida antes
        return stock_por_paquete

    def sumar_stock(self):
        try:
            # Obtener el stock actual desde el campo de entrada
            stock_actual = int(self.entry_cantidad.get())

            # Llamar a la función para obtener el stock por paquete, se debe pasar el ID del producto
            producto_id = 1  # Este es un ejemplo, aquí deberías pasar el ID del producto que estás seleccionando
            stock_por_paquete = self.obtener_stock_por_paquete(producto_id)
            
            if stock_por_paquete is None:
                messagebox.showerror("Error", "No se pudo obtener el stock por paquete.")
                return

            # Sumar el stock por paquete al stock actual
            stock_nuevo = stock_actual + stock_por_paquete
            self.entry_cantidad.delete(0, ttk.END)  # Limpiar el campo de cantidad
            self.entry_cantidad.insert(0, str(stock_nuevo))  # Mostrar el nuevo stock

        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un valor válido para el stock.")

    # Función para restar al stock actual
    def restar_stock(self):
        try:
            stock_actual = int(self.entry_cantidad.get())  # Obtener el valor actual del stock
            stock_por_paquete = int(self.entry_cantidad.get())  # Suponemos que el valor en el campo es el stock por paquete

            # Restar el stock por paquete al stock actual
            stock_nuevo = stock_actual - stock_por_paquete
            if stock_nuevo < 0:
                messagebox.showerror("Error", "El stock no puede ser negativo.")
                return
            self.entry_cantidad.delete(0, ttk.END)  # Limpiar el campo
            self.entry_cantidad.insert(0, str(stock_nuevo))  # Mostrar el nuevo stock
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingresa un valor válido para el stock.")



    def agregar_producto(self):
        producto = self.combo_producto.get()
        cantidad = self.entry_cantidad.get()
        if not producto or not cantidad.isdigit():
            messagebox.showerror("Error", "Seleccione un producto y una cantidad válida.")
            return
        self.treeview_tabla.insert("", "end", values=(producto, cantidad))
        self.entry_cantidad.delete(0, "end")

    def preparar_datos_y_generar_pdf(self):
        # Obtener los datos de la tabla
        datos = []
        for item in self.treeview_tabla.get_children():
            valores = self.treeview_tabla.item(item, "values")
            # Agregar los valores como tupla, incluyendo precio si es necesario
            producto, cantidad = valores[:2]
            precio = 0  # Si no tienes el precio, agrega un valor por defecto o cámbialo según tu lógica
            datos.append((producto, cantidad, precio))
        
        # Verificar si hay datos antes de generar el PDF
        if not datos:
            messagebox.showwarning("Advertencia", "No hay datos en la tabla para generar el PDF.")
            return

        # Llamar a generar_pdf con los datos
        self.generar_pdf(datos, "solicitud.pdf")



    def generar_pdf(self, datos, nombre_pdf):
        """Genera un PDF con los datos proporcionados, incluyendo el código único."""
        try:
            # Obtener el código único
            codigo_unico = obtener_codigo_unico()

            if not codigo_unico:
                messagebox.showerror("Error", "No se pudo obtener el código único.")
                return  # Si no se pudo obtener el código, salir de la función

            c = canvas.Canvas(nombre_pdf, pagesize=letter)
            c.setFont("Helvetica", 12)

            # Título del PDF
            c.drawString(100, 750, "Solicitud de Productos")

            # Código de solicitud
            c.drawString(50, 730, f"Código de Solicitud: {codigo_unico}")

            # Encabezados de la tabla
            c.drawString(50, 700, "Producto")
            c.drawString(250, 700, "Cantidad")
            c.drawString(350, 700, "Precio")

            y = 680  # Coordenada inicial
            for producto, cantidad, precio in datos:
                c.drawString(50, y, producto)
                c.drawString(250, y, str(cantidad))
                c.drawString(350, y, f"${precio}")
                y -= 20  # Mover hacia abajo para la siguiente fila

            c.save()

            # Abrir el PDF automáticamente
            self.abrir_pdf(nombre_pdf)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo generar el PDF: {e}")


    def abrir_pdf(self, nombre_pdf):
        """Abre el PDF generado usando el visor predeterminado."""
        try:
            if os.name == "nt":  # Windows
                os.startfile(nombre_pdf)
            elif os.name == "posix":  # Linux y macOS
                os.system(f"open '{nombre_pdf}'")
            else:
                messagebox.showinfo("Información", f"El PDF '{nombre_pdf}' se ha generado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el PDF: {e}")




if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MenuSolicitudes(root)
    root.mainloop()
