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
        # Variable para la cantidad
        self.cantidades_inicial = {}  # Valor inicial de cantidad

        # Pesos de filas y columnas
        self.root.rowconfigure(0, weight=0)  # Fila superior: Título
        self.root.rowconfigure(1, weight=1)  # Fila inferior: Frames principales
        self.root.columnconfigure(0, weight=1)  # Columna izquierda
        self.root.columnconfigure(1, weight=2)  # Columna derecha

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
        self.frame_productos = ttk.Frame(root, padding=20, borderwidth=2, relief="groove")
        self.frame_productos.grid(row=1, column=1, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)

        # Frame izquierdo inferior: código de barra
        self.frame_ingreso_producto = ttk.Frame(root, padding=20)
        self.frame_ingreso_producto.grid(row=1, column=0, sticky="nsew", padx=PADDING_X, pady=PADDING_Y)

        self.frame_ingreso_producto.grid_rowconfigure(0, weight=1)  
        self.frame_ingreso_producto.grid_rowconfigure(1, weight=0)  
        self.frame_ingreso_producto.grid_rowconfigure(2, weight=0)  
        self.frame_ingreso_producto.grid_rowconfigure(3, weight=0)
        self.frame_ingreso_producto.grid_rowconfigure(4, weight=0)

        self.frame_ingreso_producto.grid_columnconfigure(0, weight=1)
        self.frame_ingreso_producto.grid_columnconfigure(1, weight=0)  
        self.frame_ingreso_producto.grid_columnconfigure(2, weight=1)  

        # Widgets dentro de frame_productos
        self.label_cantidad = ttk.Label(self.frame_ingreso_producto,text="Cantidad: 0",font=("Helvetica", 16))
        self.label_cantidad.grid(row=1,column=1, pady=15, padx=10)

        self.label_codigo = ttk.Label(self.frame_ingreso_producto, text="Ingresar código", font=("Helvetica", 12))
        self.label_codigo.grid(row=2, column=1, pady=15, padx=10)

        self.entry_codigo = ttk.Entry(self.frame_ingreso_producto)
        self.entry_codigo.grid(row=3, column=1, pady=10, padx=10)

        # Bind para detectar la tecla c 
        self.root.bind("<c>", self.ingresar_cantidad)
        # Bind para detectar la tecla Enter
        self.entry_codigo.bind("<Return>", self.procesar_codigo)

    def ingresar_cantidad(self, event):
        """Abrir popup para ingresar cantidad con control por teclado."""
        popup = ttk.Toplevel(self.root)
        popup.title("Ingresar cantidad")
        popup.geometry("300x150")
        popup.transient(self.root)  # Mantener popup encima de la ventana principal
        popup.grab_set()  # Modal, bloquea interacciones con la ventana principal

        # Etiqueta de mensaje
        label = ttk.Label(popup, text="Ingrese la cantidad de productos:", font=("Helvetica", 12))
        label.pack(pady=10)

        # Entrada para la cantidad
        entry_cantidad = ttk.Entry(popup, justify="center")
        entry_cantidad.pack(pady=10)
        entry_cantidad.focus()  # Enfocar entrada

        # Botón de aceptar (por si necesitas clic, pero será controlado con Enter)
        btn_aceptar = ttk.Button(popup, text="Aceptar", command=lambda: self.aceptar_cantidad(popup, entry_cantidad))
        btn_aceptar.pack(pady=5)

        # Vincular teclas al popup
        popup.bind("<Return>", lambda event: self.aceptar_cantidad(popup, entry_cantidad))  # Enter
        popup.bind("<Escape>", lambda event: self.cancelar_popup(popup))  # Esc

    def aceptar_codigo(self, popup, entry_codigo):
        """Acción al aceptar el código del producto."""
        codigo = entry_codigo.get().strip()  # Obtener el código ingresado
        
        if codigo.isdigit():  # Validar si el código contiene solo números
            self.codigo_ingresado = codigo  # Guardar el código
            self.label_codigo.config(text=f"Código: {codigo}")  # Actualizar la UI con el código
            self.entry_codigo.config(state="disabled")  # Deshabilitar el campo de código
            self.entry_cantidad.config(state="normal")  # Habilitar el campo de cantidad
            self.label_cantidad.config(text="Ingrese la cantidad:")  # Cambiar el texto de la etiqueta
        else:
            messagebox.showerror("Error", "Código inválido. Ingrese solo números.")
            popup.destroy()
            
    def aceptar_cantidad(self, popup, entry_cantidad):
        """Acción al aceptar la cantidad."""
        cantidad = entry_cantidad.get()  # Obtener la cantidad ingresada
            
        if cantidad.isdigit():  # Validar si la cantidad es un número
            cantidad = int(cantidad)
        else:
            messagebox.showerror("Error", "Cantidad no válida. Ingrese un número.")
            popup.destroy()  # Cerrar la ventana emergente

    def cancelar_popup(self, popup):
        """Cerrar el popup sin realizar ninguna acción."""
        print("Operación cancelada")
        popup.destroy()

    def obtener_producto_por_codigo_bd(self, codigo):
        """Obtiene el producto desde la base de datos por código"""
        producto = obtener_producto_por_codigo(codigo)  # Llama a la función parsa obtener el producto por código
        print("Producto obtenido de la base de datos:", producto)  # Verificar el producto
        return producto

    #Mostrar productos en la tabla 
    def mostrar_productos(self):
        """Muestra todos los productos y sus cantidades en el frame derecho."""
        for widget in self.frame_productos.winfo_children():
            widget.destroy()

        for codigo, cantidad in self.cantidades.items():
            producto = self.obtener_producto_por_codigo_bd(codigo)
            if producto:
                frame_producto = ttk.Frame(self.frame_productos)
                frame_producto.pack(fill="x", pady=5)

                label_producto = ttk.Label(frame_producto, text=f"{producto['nombre']} ({codigo})", font=("Helvetica", 12))
                label_producto.pack(side="left", padx=10)

                label_precio = ttk.Label(frame_producto, text=f"Precio: {producto['precio_venta']} CLP", font=("Helvetica", 12))
                label_precio.pack(side="right", padx=10)

                label_cantidad = ttk.Label(frame_producto, text=f"Cantidad: {cantidad}", font=("Helvetica", 12))
                label_cantidad.pack(side="right", padx=10)

    def procesar_codigo(self, event):
        """Función que procesa el código de barras ingresado."""
        codigo = self.entry_codigo.get().strip()
        if codigo:
            self.entry_codigo.delete(0, ttk.END)
            producto = self.obtener_producto_por_codigo_bd(codigo)
            if producto:
                if codigo in self.cantidades:
                    self.cantidades[codigo] += 1
                else:
                    self.cantidades[codigo] = 1
                self.mostrar_productos()
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese un código válido.")



if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaCaja(root)
    root.mainloop()
