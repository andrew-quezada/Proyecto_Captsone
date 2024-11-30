import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from db.ventana_caja_bd import obtener_producto_por_codigo  
from tkinter import simpledialog

class VentanaCaja:
    def __init__(self, root):
        self.root = root
        self.root.title("Caja de Ventas")

        # Inicializar un diccionario para llevar la cantidad de productos
        self.cantidades = {}

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}+0+0")
        self.root.resizable(True, True)
        self.root.minsize(1000, 400)

        # Título
        self.label_titulo = ttk.Label(root, text="Lectura de Código de Barras", font=("Helvetica", 16), anchor="center")
        self.label_titulo.pack(pady=10)

        # Frame izquierdo codigo de barra
        self.frame_principal = ttk.Frame(root, padding=20)
        self.frame_principal.pack(side="left", fill="y")

        # Frame derecho para los productos
        self.frame_productos = ttk.Frame(root, padding=60, borderwidth=2, relief="groove")
        self.frame_productos.pack(side="right", fill="y", padx=15, pady=10)

        # Configurar la cuadrícula para el frame
        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_rowconfigure(1, weight=1)

        # Label para el usuario (centrado en su celda)
        self.label_usuario = ttk.Label(self.frame_principal, text="Pedro", font=("Helvetica", 14))
        self.label_usuario.grid(row=0, column=0, padx=15, pady=10, sticky="nsew")

        # Entry para el código de barras (centrado en su celda)
        self.label_codigo = ttk.Label(self.frame_principal, text="Ingrese Código de Barras:", font=("Helvetica", 14))
        self.label_codigo.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        # Configura el Entry con la validación
        vcmd = (self.root.register(self.validar_codigo), '%S', '%P')
        self.entry_codigo = ttk.Entry(self.frame_principal, width=30, font=("Helvetica", 14), validate='key', validatecommand=vcmd)
        self.entry_codigo.grid(row=3, column=1, padx=10, pady=10, sticky="nsew")

        # Bind para la tecla C
        self.root.bind("<KeyPress-c>", self.activar_ingreso_cantidad)

        # Bind para detectar la tecla Enter
        self.entry_codigo.bind("<Return>", self.procesar_codigo)

        # Título en el frame productos
        self.label_titulo_derecho = ttk.Label(self.frame_productos, text="Producto Ingresado", font=("Helvetica", 14), anchor="center")
        self.label_titulo_derecho.pack(pady=10)

        # Etiqueta para mostrar el resultado del código procesado
        self.label_resultado = ttk.Label(self.frame_principal, text="", font=("Helvetica", 14), foreground="green")
        self.label_resultado.grid(row=4, column=1, padx=10, pady=10)

    def validar_codigo(self, char, entrada):
        """Validar solo números y activar ingreso de cantidad con la tecla C."""
        if char.isdigit():
            return True  # Permite números
        elif char.lower() == 'c':
            self.activar_ingreso_cantidad()
            return True  # Evita que 'C' se muestre en el Entry
        return False  # Bloquea cualquier otro carácter

    def activar_ingreso_cantidad(self):
        """Activar la entrada de cantidad y limpiar el Entry de código."""
        self.entry_codigo.delete(0, tk.END)  # Limpiar el Entry
        # ... (resto de tu lógica para activar el ingreso de cantidad)
        # Por ejemplo, habilitar un nuevo Entry para la cantidad
        self.entry_cantidad.config(state="normal")

    def activar_ingreso_cantidad(self):
        self.entry_codigo.delete(0, tk.END)
        self.entry_cantidad.focus()  # Enfocar el Entry de cantidad
        self.entry_cantidad.config(state="normal")
        self.label_resultado.config(text="Ingrese la cantidad")
    
    def obtener_producto_por_codigo_bd(self, codigo):
        """Obtiene el producto desde la base de datos por código"""
        producto = obtener_producto_por_codigo(codigo)  # Llama a la función parsa obtener el producto por código
        print("Producto obtenido de la base de datos:", producto)  # Verificar el producto
        return producto


    def mostrar_producto(self, producto):
        """Muestra el producto en el frame derecho"""
        # Borramos cualquier contenido previo
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        # Verificar qué datos estás obteniendo
        print(f"Producto a mostrar: {producto}")  # Depuración de la estructura del producto

        if producto:
            codigo = producto['cod_barra']
            nombre = producto['nombre']
            precio = producto['precio_venta']

            # Crear un frame para el producto
            frame_producto = ttk.Frame(self.frame_productos)
            frame_producto.pack(fill="x", pady=5)

            # Mostrar el código y el nombre del producto
            label_producto = ttk.Label(frame_producto, text=f"{codigo} {nombre}", font=("Helvetica", 12))
            label_producto.pack(side="left", padx=10)

            # Mostrar el precio
            label_precio = ttk.Label(frame_producto, text=f"Precio: {precio} CLP", font=("Helvetica", 12))
            label_precio.pack(side="right", padx=10)

            # Mostrar la cantidad del producto
            cantidad = self.cantidades.get(codigo, 0)
            label_cantidad = ttk.Label(frame_producto, text=f"Cantidad: {cantidad}", font=("Helvetica", 12))
            label_cantidad.pack(side="right", padx=10)
        else:
            label_error = ttk.Label(self.frame_productos, text="Producto no encontrado.", font=("Helvetica", 12), foreground="red")
            label_error.pack(pady=10)

    def procesar_codigo(self, event):
        """Función que procesa el código de barras ingresado"""
        codigo = self.entry_codigo.get().strip()
        if codigo:
            self.label_resultado.config(text=f"Código procesado: {codigo}")
            self.entry_codigo.delete(0, tk.END)  # Limpiar el campo de entrada

            # Obtener el producto por código de la base de datos y mostrarlo
            producto = self.obtener_producto_por_codigo_bd(codigo)
            if producto:
                # Si el producto ya fue ingresado, aumentamos la cantidad
                if codigo in self.cantidades:
                    self.cantidades[codigo] += 1
                else:
                    # Si es la primera vez que ingresamos este producto, la cantidad es 1
                    self.cantidades[codigo] = 1

                # Mostrar el producto con la cantidad actualizada
                self.mostrar_producto(producto)
            else:
                self.label_resultado.config(text="Producto no encontrado.")
        else:
            self.label_resultado.config(text="Por favor, ingrese un código válido.")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaCaja(root)
    root.mainloop()
