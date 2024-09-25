import tkinter as tk
import ttkbootstrap as ttk
from datetime import datetime

# lista de validaciones
# verificar si el producto ingresado existe en la base de datos
# si se ingresa nuevamente un producto que este se sume con el ya ingresado
# modificar la tabla de productos para que se refleje automaticamente el nombre del producto por el codigo
# agregar funcion de ingreso mediante scan de barra  
# hacer mas dinamico el ingreso de fecha 

class IngresarStock:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingreso de Stock")

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = screen_width
        window_height = screen_height
        self.root.geometry(f"{window_width}x{window_height}+0+0")

        # Crear un frame para organizar los widgets
        frame = tk.Frame(self.root)
        frame.pack(expand=True, fill="both", padx=20, pady=20)

        # Configurar el grid
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        frame.grid_columnconfigure(2, weight=1)
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=0)
        frame.grid_rowconfigure(2, weight=0)
        frame.grid_rowconfigure(3, weight=0)
        frame.grid_rowconfigure(4, weight=0)
        frame.grid_rowconfigure(5, weight=1)  # Esta fila ocupará el espacio restante para la tabla

        # Campo para ingresar el código de producto
        ttk.Label(frame, text="Código de producto:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.codigo_entry = ttk.Entry(frame)
        self.codigo_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Campo para ingresar la cantidad
        ttk.Label(frame, text="Cantidad:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.cantidad_entry = ttk.Entry(frame)
        self.cantidad_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        # Campo para la fecha de ingreso (automáticamente el día actual)
        ttk.Label(frame, text="Fecha de ingreso:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.fecha_entry = ttk.Entry(frame)
        # Inserta la fecha actual (modificable por el usuario si es necesario)
        self.fecha_entry.insert(0, datetime.now().strftime('%Y-%m-%d'))
        self.fecha_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Botón para insertar en la tabla
        insert_button = ttk.Button(frame, text="Insertar", command=self.insertar_en_tabla)
        insert_button.grid(row=3, column=1, padx=10, pady=10, sticky="w")

        # Botón para agregar stock
        agregar_button = ttk.Button(frame, text="Agregar Stock", command=self.agregar_stock)
        agregar_button.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        # Configuración de la tabla
        self.tabla = ttk.Treeview(frame, columns=("Código", "Cantidad", "Fecha"), show='headings')
        self.tabla.heading("Código", text="Código de producto")
        self.tabla.heading("Cantidad", text="Cantidad")
        self.tabla.heading("Fecha", text="Fecha de ingreso")
        self.tabla.grid(row=5, column=0, columnspan=3, padx=10, pady=10, sticky='nsew')

        # Añadir un scrollbar vertical
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=5, column=3, sticky='ns')
        self.tabla.configure(yscrollcommand=scrollbar.set)

    def insertar_en_tabla(self):
        codigo = self.codigo_entry.get()
        cantidad = self.cantidad_entry.get()
        fecha_ingreso = self.fecha_entry.get()
        
        if codigo and cantidad and fecha_ingreso:
            self.tabla.insert("", "end", values=(codigo, cantidad, fecha_ingreso))
        else:
            print("Por favor, complete todos los campos.")

    def agregar_stock(self):
        # Lógica para agregar stock
        codigo = self.codigo_entry.get()
        cantidad = self.cantidad_entry.get()
        fecha_ingreso = self.fecha_entry.get()
        
        # Aquí se añadiría la lógica para validar y agregar el stock a la base de datos
        print(f"Agregando {cantidad} unidades del producto con código {codigo} ingresado el {fecha_ingreso}")

