import ttkbootstrap as ttk
from db.ventana_caja_bd import obtener_producto_por_codigo
from tkinter import messagebox
import tkinter as tk

class VentanaCaja:
    def __init__(self, root):
        self.root = root
        self.root.title("Caja de Ventas")
        self.root.state("zoomed")
        self.root.minsize(1000, 400)
        
        self.current_row = 0  # Inicializa el contador de filas para el frame_productos
        

        # Pesos de filas y columnas
        self.root.rowconfigure(0, weight=0)  # Fila superior: Título
        self.root.rowconfigure(1, weight=1)  # Fila inferior: Frames principales
        self.root.columnconfigure(0, weight=1)  # Columna izquierda
        self.root.columnconfigure(1, weight=1)  # Columna derecha

        # Constantes de espaciado
        PADDING_X = 10
        PADDING_Y = 10

        # Frame superior: datos del usuario
        self.frame_titulo = ttk.Frame(root, padding=20)
        self.frame_titulo.grid(row=0, column=0, columnspan=2, sticky="ew", padx=PADDING_X, pady=PADDING_Y)

        # Título Principal
        self.frame_titulo.columnconfigure(0, weight=1)  # Centrar etiquetas en el frame
        self.label_titulo = ttk.Label(self.frame_titulo, text="Venta Caja", font=("Helvetica", 16))
        self.label_titulo.grid(row=0, column=0, sticky="ew", pady=5)

        # Próximamente: nombre del trabajador
        self.label_usuario = ttk.Label(self.frame_titulo, text="Nombre Usuario", font=("Helvetica", 12))
        self.label_usuario.grid(row=1, column=0, sticky="ew", pady=5)

        # Frame izquierdo inferior: código de barra
        self.frame_ingreso_producto = ttk.Frame(root, padding=20)
        self.frame_ingreso_producto.grid(row=1, column=0, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)

        # Frame derecho inferior: productos
        self.frame_productos = ttk.Frame(root, padding=10, borderwidth=2, relief="groove")
        self.frame_productos.grid(row=1, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)

        # Frame izquierdo inferior: código de barra
        self.frame_ingreso_producto = ttk.Frame(root, padding=20)
        self.frame_ingreso_producto.grid(row=1, column=0, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)

        self.frame_ingreso_producto.grid_rowconfigure(0, weight=0)  
        self.frame_ingreso_producto.grid_rowconfigure(1, weight=0)  
        self.frame_ingreso_producto.grid_rowconfigure(2, weight=0)  
        self.frame_ingreso_producto.grid_rowconfigure(3, weight=0)
        self.frame_ingreso_producto.grid_rowconfigure(4, weight=0)

        self.frame_ingreso_producto.grid_columnconfigure(0, weight=1)
        self.frame_ingreso_producto.grid_columnconfigure(1, weight=0)  
        self.frame_ingreso_producto.grid_columnconfigure(2, weight=1)  

        # Widgets dentro de frame_productos
        self.label_cantidad = ttk.Label(self.frame_ingreso_producto, text="Ingresar cantidad", font=("Helvetica", 12))
        self.label_cantidad.grid(row=0, column=1, pady=15, padx=10)

        self.entry_cantidad = ttk.Entry(self.frame_ingreso_producto)
        self.entry_cantidad.grid(row=1, column=1, pady=10, padx=10)

        self.label_codigo = ttk.Label(self.frame_ingreso_producto, text="Ingresar código", font=("Helvetica", 12))
        self.label_codigo.grid(row=2, column=1, pady=15, padx=10)

        self.entry_codigo = ttk.Entry(self.frame_ingreso_producto)
        self.entry_codigo.grid(row=3, column=1, pady=10, padx=10)

        # Bind para detectar la tecla Enter
        self.entry_codigo.bind("<Return>", self.procesar_codigo)

        self.fila_actual_productos = 0

    def obtener_producto_por_codigo_bd(self, codigo):
        producto = obtener_producto_por_codigo(codigo)
        print("Producto obtenido de la base de datos:", producto)
        return producto

    def procesar_codigo(self, event):
        codigo = self.entry_codigo.get().strip()
        if codigo:
            self.entry_codigo.delete(0, tk.END)
            producto = self.obtener_producto_por_codigo_bd(codigo)
            if producto:
                self.mostrar_producto(producto)
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un código válido.")

    def mostrar_producto(self, producto):
        cantidad = self.entry_cantidad.get().strip()  # Eliminar espacios en blanco

        # Validar que cantidad sea un número
        if not cantidad.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")
            return

        cantidad = int(cantidad)  # Convertir a entero

        if producto:
            # Calcular subtotal
            codigo = producto['cod_barra']
            nombre = producto['nombre']
            precio = producto['precio_venta']  # Suponemos que precio es un número
            sub_total = precio * cantidad  # Calcular el subtotal

            # Insertar en la fila actual
            ttk.Label(self.frame_productos, text=codigo, font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos, column=0, columnspan=2, pady=10
            )
            ttk.Label(self.frame_productos, text=nombre, font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos, column=2,columnspan=3, pady=10
            )
            ttk.Label(self.frame_productos, text=f"${precio:.2f}", font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos + 1, column=0, pady=10
            )
            ttk.Label(self.frame_productos, text="x", font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos + 1, column=1, pady=10
            )
            ttk.Label(self.frame_productos, text=cantidad, font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos + 1, column=2, pady=10
            )
            ttk.Label(self.frame_productos, text=f"${sub_total:.2f}", font=("Helvetica", 12)).grid(
                row=self.fila_actual_productos + 1, column=3, pady=10
            )

            # Incrementar la fila actual para el próximo producto
            self.fila_actual_productos += 2
        else:
            messagebox.showerror("Error", "Producto no encontrado.")


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaCaja(root)
    root.mainloop()
