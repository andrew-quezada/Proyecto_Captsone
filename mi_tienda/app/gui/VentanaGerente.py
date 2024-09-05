import tkinter as tk
import ttkbootstrap as ttk
from gui.Ingresar_Stock import IngresarStock

class VentanaGerente:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerencia")

        # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir el tamaño de la ventana como el 100% del tamaño de la pantalla
        window_width = screen_width
        window_height = screen_height

        # Establecer el tamaño y la posición de la ventana
        self.root.geometry(f"{window_width}x{window_height}+0+0")

        # Configurar el comportamiento de la ventana para que no se pueda redimensionar
        self.root.resizable(True, True)  # Hacer que la ventana sea redimensionable

        # Crear botones y empaquetarlos
        self.button1 = ttk.Button(root, text="Registrar Stock", bootstyle="primary", command=self.open_ingresar_stock_window)
        self.button2 = ttk.Button(root, text="Funcion por definir", bootstyle="primary", command=self.mantencion_productos)
        self.button3 = ttk.Button(root, text="funcion por definir", bootstyle="primary", command=self.ventas)

        # Organizando los botones
        self.button1.grid(row=1, column=1, sticky="ew", padx=10, pady=10)
        self.button2.grid(row=1, column=3, sticky="ew", padx=10, pady=10)
        self.button3.grid(row=1, column=5, sticky="ew", padx=10, pady=10)

        # Organizando las columnas vacías
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)
        root.grid_columnconfigure(4, weight=1)
        root.grid_columnconfigure(5, weight=1)
        root.grid_columnconfigure(6, weight=1)

        # Organizando las filas vacías
        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=1)
        root.grid_rowconfigure(2, weight=1)

    def open_ingresar_stock_window(self):
        self.root.withdraw()  # Oculta la ventana actual (VentanaGerente)
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija para Ingresar Stock
        IngresarStock(new_root)

        # Asegúrate de que al cerrar la ventana de Ingresar Stock, regrese a VentanaGerente
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def on_close_window(self, window):
        window.destroy()  # Cierra la ventana de Ingresar Stock
        self.root.deiconify()  # Muestra la ventana de gerente de nuevo

    def mantencion_productos(self):
        print("Mantención de productos")

    def ventas(self):
        print("Ventas")

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaGerente(root)
    root.mainloop()
