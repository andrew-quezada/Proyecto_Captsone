import ttkbootstrap as ttk
import tkinter as tk
from db.ventana_caja_bd import obtener_producto_por_codigo
from tkinter import messagebox
from gui.venta_pago import VentaPago


class VentanaCaja:
    def __init__(self, root, nombre_empleado="Empleado"):
        self.root = root
        self.nombre_empleado = nombre_empleado  # Obtener nombre empleado de inicio sesión
        self.root.title("Caja de Ventas")
        self.root.state("zoomed")
        self.root.minsize(1000, 400)

        self.total = 0
        self.productos_vendidos = []
        self.fila_actual_productos = 0
        self.cantidad_inicial = tk.IntVar(value=1)  # Inicializamos cantidad en 1

        # Constantes de espaciado
        PADDING_X = 10
        PADDING_Y = 10

        # Frame superior: datos del usuario
        self.frame_titulo = ttk.Frame(root, padding=20)
        self.frame_titulo.pack(fill="x", padx=PADDING_X, pady=PADDING_Y)

        self.label_titulo = ttk.Label(self.frame_titulo, text="Venta Caja", font=("Helvetica", 16))
        self.label_titulo.pack(pady=5)

        self.label_usuario = ttk.Label(self.frame_titulo, text=f"Bienvenido: {self.nombre_empleado}", font=("Helvetica", 12))
        self.label_usuario.pack(pady=5)

        # Contenedor principal para organizar los frames
        frame_contenedor = ttk.Frame(root, padding=15)
        frame_contenedor.pack(side="right", fill="both", expand=False, padx=10, pady=10)

        # Frame para productos
        self.frame_productos = ttk.Frame(frame_contenedor, padding=5, borderwidth=2, relief="groove")
        self.frame_productos.pack(side="top", fill="y", padx=10, pady=10, expand=True)

        # Frame total
        self.frame_total = ttk.Frame(frame_contenedor, padding=5, borderwidth=2, relief="ridge")
        self.frame_total.pack(side="bottom", fill="both", padx=10, pady=10)

        self.canvas = tk.Canvas(self.frame_productos)
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)

        self.scrollbar = ttk.Scrollbar(self.frame_productos, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame_productos_inner = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame_productos_inner, anchor="nw")
        self.frame_productos_inner.pack(fill="both", expand=True)
        self.frame_productos_inner.bind("<Configure>", self.actualizar_scrollregion)

        self.label_total = ttk.Label(self.frame_total, text=f"Total: $0", font=("Helvetica", 14, "bold"))
        self.label_total.pack(side="right", padx=10)

        # Frame para ingresar productos
        self.frame_ingreso_producto = ttk.Frame(root, padding=10)
        self.frame_ingreso_producto.pack(fill="x", padx=PADDING_X, pady=PADDING_Y, side="top")

        self.label_cantidad = ttk.Label(self.frame_ingreso_producto, text="Ingresar cantidad", font=("Helvetica", 12))
        self.label_cantidad.pack(pady=15)
        self.entry_cantidad = ttk.Entry(self.frame_ingreso_producto, textvariable=self.cantidad_inicial)
        self.entry_cantidad.pack(pady=10)

        self.label_codigo = ttk.Label(self.frame_ingreso_producto, text="Ingresar código", font=("Helvetica", 12))
        self.label_codigo.pack(pady=15)
        self.entry_codigo = ttk.Entry(self.frame_ingreso_producto)
        self.entry_codigo.pack(pady=10)

        self.entry_codigo.bind("<Return>", self.procesar_codigo)
        self.root.bind("t", self.abrir_ventana_pago)

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
        cantidad = self.entry_cantidad.get().strip()

        # Verificar que la cantidad sea un número válido
        if not cantidad.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese una cantidad válida.")
            return

        cantidad = int(cantidad)  # Convertir la cantidad a entero
        codigo = int(producto['cod_barra'])
        nombre = producto['nombre']
        precio = int(producto['precio_venta'])
        sub_total = int(precio * cantidad)

        # Crear un nuevo Frame para mostrar el producto
        fila_frame = ttk.Frame(self.frame_productos_inner)
        fila_frame.pack(fill="x", pady=5)

        # Mostrar los detalles del producto
        ttk.Label(fila_frame, text=codigo, font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Label(fila_frame, text=nombre, font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Label(fila_frame, text=f"${precio}", font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Label(fila_frame, text="x", font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Label(fila_frame, text=cantidad, font=("Helvetica", 12)).pack(side="left", padx=10)
        ttk.Label(fila_frame, text=f"${sub_total}", font=("Helvetica", 12)).pack(side="left", padx=10)

        # Actualizar el total de la venta
        self.total += sub_total
        self.label_total.config(text=f"Total: ${self.total}")

        # Agregar el producto a la lista de productos vendidos
        self.productos_vendidos.append({
            "codigo": codigo,
            "nombre": nombre,
            "cantidad": cantidad,
            "precio_unitario": precio,
            "subtotal": sub_total
        })

        # Reiniciar la cantidad del producto a 1
        self.cantidad_inicial.set(1)


    def actualizar_scrollregion(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def abrir_ventana_pago(self, event=None):
        ventana_pago = tk.Toplevel(self.root)
        ventana_pago.title("Método de Pago")
        ventana_pago.geometry("300x200")
        ventana_pago.transient(self.root)

        etiqueta = ttk.Label(ventana_pago, text="Seleccione el método de pago", font=("Helvetica", 14))
        etiqueta.pack(pady=20)

        btn_efectivo = ttk.Button(
            ventana_pago, text="1. Efectivo",
            command=lambda: self.seleccionar_pago("efectivo", ventana_pago)
        )
        btn_efectivo.pack(pady=10)

        btn_transbank = ttk.Button(
            ventana_pago, text="2. Transbank",
            command=lambda: self.seleccionar_pago("transbank", ventana_pago)
        )
        btn_transbank.pack(pady=10)

    def seleccionar_pago(self, opcion, ventana_pago):
        ventana_pago.destroy()
        if opcion == "efectivo":
            VentaPago(self.root, self.total, self.productos_vendidos)
        elif opcion == "transbank":
            messagebox.showinfo("Pago", "Has seleccionado Transbank.")


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaCaja(root)
    root.mainloop()
