import ttkbootstrap as ttk
import tkinter as tk
from tkinter import messagebox

class VentaPago:
    def __init__(self, root, total, productos_vendidos):
        self.root = root
        self.total = total
        self.productos_vendidos = productos_vendidos
        self.ventana = tk.Toplevel(root)
        self.ventana.title("Pago en Efectivo")
        self.ventana.state("zoomed")
        self.ventana.minsize(1000, 400)
        self.ventana.transient(root)  # Asociar la ventana a la principal

        self.total = total  # Total de la venta
        self.monto_recibido = tk.DoubleVar()  # Variable para el monto recibido

        # Etiqueta de instrucciones
        ttk.Label(self.ventana, text=f"Total a pagar: ${self.total}", font=("Helvetica", 14)).pack(pady=10)
        ttk.Label(self.ventana, text="Ingrese el monto recibido:", font=("Helvetica", 12)).pack(pady=10)

        # Entry para el monto
        ttk.Entry(self.ventana, textvariable=self.monto_recibido, font=("Helvetica", 12)).pack(pady=10)

        # Botones para procesar o cancelar
        ttk.Button(self.ventana, text="Procesar", command=lambda: self.procesar_pago(self.monto_recibido.get())).pack(pady=10)
        ttk.Button(self.ventana, text="Cancelar", command=self.ventana.destroy).pack(pady=5)

    def procesar_pago(self, monto_recibido):
        if monto_recibido < self.total:
            messagebox.showerror("Error", "El monto recibido es insuficiente.")
            return

        vuelto = monto_recibido - self.total
        if vuelto > 0:
            messagebox.showinfo("Vuelto", f"El vuelto es: ${vuelto}")

        # Registrar la venta en la base de datos
        try:
            from db.ventana_caja_bd import registrar_venta
            registrar_venta(self.total, "efectivo", self.productos_vendidos)
            messagebox.showinfo("Éxito", "Venta completada con éxito.")
            self.root.destroy()  # Cierra la ventana
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al registrar la venta: {str(e)}")

    def finalizar_venta(self):
        # Agrega aquí la lógica para guardar la venta en la base de datos y cerrar la ventana
        messagebox.showinfo("Éxito", "Venta registrada correctamente.")
        self.ventana.destroy()
