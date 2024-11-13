import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
import tkinter as tk
from gui.Ingresar_Stock import IngresarStock
from gui.menu_solicitudes import MenuSolicitudes
from gui.menu_nuevos_ingreso import MenuNuevosIngresos

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

        # Crear un contenedor para los botones principales
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(expand=True, fill=tk.BOTH, pady=20, padx=20)

        # Crear un contenedor separado para el botón de "Cerrar sesión"
        self.contenedor_salida = tk.Frame(self.root)
        self.contenedor_salida.pack(fill=tk.Y, pady=10, padx=10, side=tk.TOP)

        # Crear una fuente personalizada para el botón específico
        fuente_personalizada_boton_salida = tkFont.Font(family="Arial", size=10, weight="bold")

        # Crear y configurar un estilo personalizado para el botón de salida
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Arial", 10, "bold"))
        style.configure("Salida.TButton", font=fuente_personalizada_boton_salida)

        # Crear una fuente personalizada
        fuente_personalizada = tkFont.Font(family="Arial", size=14, weight="bold")

        # Crear y configurar un estilo personalizado para los botones principales
        style.configure("Custom.TButton", font=fuente_personalizada, anchor="center")

        # Cargar y redimensionar los íconos usando Pillow
        imagen1 = Image.open("app/img/list-check.png")
        imagen_redimensionada = imagen1.resize((50, 50))
        icono1 = ImageTk.PhotoImage(imagen_redimensionada)

        imagen2 = Image.open("app/img/completed.png")
        imagen_redimensionada = imagen2.resize((50, 50))
        icono2 = ImageTk.PhotoImage(imagen_redimensionada)

        imagen3 = Image.open("app/img/document.png")
        imagen_redimensionada = imagen3.resize((50, 50))
        icono3 = ImageTk.PhotoImage(imagen_redimensionada)

        imagen4 = Image.open("app/img/exit.png")
        imagen_redimensionada = imagen4.resize((15, 15))
        icono4 = ImageTk.PhotoImage(imagen_redimensionada)

        # Crear los botones principales
        boton1 = ttk.Button(self.contenedor, text="Gestion\n    de \n Stock", image=icono1, compound="top", style="Custom.TButton", bootstyle=SUCCESS, command=self.open_ingresar_stock_window)
        boton2 = ttk.Button(self.contenedor, text=" Consultas\n         y\nSolicitudes", image=icono2, compound="top", style="Custom.TButton", bootstyle=SUCCESS, command=self.open_menu_solicitudes_peticiones_window)
        boton3 = ttk.Button(self.contenedor, text="Nuevos\ningresos\n", image=icono3, compound="top", style="Custom.TButton", bootstyle=SUCCESS, command=self.open_nuevos_ingresos)

        # Botón "Cerrar sesión" en un frame aparte
        boton_salida = ttk.Button(self.contenedor_salida, text="Cerrar sesión", image=icono4, compound="left", style="Salida.TButton", bootstyle=SUCCESS)

        # Organizar el menú y los botones en la cuadrícula del frame principal
        boton1.grid(row=1, column=0, padx=20, pady=40, ipadx=80, ipady=150)
        boton2.grid(row=1, column=1, padx=20, pady=40, ipadx=80, ipady=150)
        boton3.grid(row=1, column=2, padx=20, pady=40, ipadx=80, ipady=150)

        # Botón de "Cerrar sesión" en el frame aparte, en la parte inferior
        boton_salida.pack(anchor="e")

        self.contenedor.columnconfigure([0, 1, 2], weight=1)
        self.contenedor.rowconfigure([0, 1], weight=1)

        # Mantener la referencia de los íconos
        boton1.image = icono1
        boton2.image = icono2
        boton3.image = icono3
        boton_salida.image = icono4

    def open_ingresar_stock_window(self):
        self.root.withdraw()  # Oculta la ventana actual (VentanaGerente)
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija para Ingresar Stock
        IngresarStock(new_root)

        # Asegúrate de que al cerrar la ventana de Ingresar Stock, regrese a VentanaGerente
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def open_menu_solicitudes_peticiones_window(self):
        self.root.withdraw()  # Oculta la ventana actual (VentanaGerente)
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija para Ingresar nuevo producto
        MenuSolicitudes(new_root)

        # Asegúrate de que al cerrar la ventana de Ingresar nuevo producto, regrese a VentanaGerente
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def open_nuevos_ingresos(self):
        self.root.withdraw()  # Oculta la ventana actual (VentanaGerente)
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija para Ingresar nuevo producto y proveedor
        MenuNuevosIngresos(new_root)

        # Asegúrate de que al cerrar la ventana de Ingresar nuevo producto, regrese a VentanaGerente
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def on_close_window(self, window):
        window.destroy()  # Cierra la ventana
        self.root.deiconify()  # Muestra la ventana de gerente de nuevo

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = VentanaGerente(root)
    root.mainloop()
