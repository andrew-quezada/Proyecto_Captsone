import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
from gui.generar_proveedor import GenerarProveedor

class MenuNuevosIngresos:
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

        # Crear un contenedor para los botones
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(expand=True, fill=tk.BOTH, pady=20, padx=20)

        # Crear una fuente personalizada para el botón específico
        fuente_personalizada_boton_salida = tkFont.Font(family="Arial", size=10, weight="bold")

        # Crear y configurar un estilo personalizado para el botón de salida
        style = ttk.Style()
        style.configure("Custom.TButton", font=("Arial", 10, "bold"))
        style.configure("Salida.TButton", font=fuente_personalizada_boton_salida)

        # Crear una fuente personalizada
        fuente_personalizada = tkFont.Font(family="Arial", size=14, weight="bold")

        # Crear y configurar un estilo personalizado para el botón
        style = ttk.Style()
        style.configure("Custom.TButton", font=fuente_personalizada, anchor="center")

        # Cargar y redimensionar el ícono usando Pillow
        imagen1 = Image.open("mi_tienda/app/img/boxes.png")
        imagen_redimensionada = imagen1.resize((50, 50)) 
        icono1 = ImageTk.PhotoImage(imagen_redimensionada)

        imagen2 = Image.open("mi_tienda/app/img/user-add.png")
        imagen_redimensionada = imagen2.resize((50, 50))  
        icono2 = ImageTk.PhotoImage(imagen_redimensionada)

        # Crear el botón con el ícono y el estilo personalizado
        boton1 = ttk.Button(self.contenedor, text="Nuevo producto", image=icono1, compound="top", style="Custom.TButton", bootstyle=SUCCESS)
        boton2 = ttk.Button(self.contenedor, text="Nuevo proveedor", image=icono2, compound="top", style="Custom.TButton", bootstyle=SUCCESS, command=self.open_window_generar_Proveedor)
        
        boton1.grid(row=1, column=0, padx=20, pady=40, ipadx=80, ipady=150)
        boton2.grid(row=1, column=1, padx=20, pady=40, ipadx=80, ipady=150)

        self.contenedor.columnconfigure([0, 1], weight=1)
        self.contenedor.rowconfigure([0, 1], weight=0)

        # Mantener la referencia del ícono
        boton1.image = icono1
        boton2.image = icono2

    def open_window_generar_Proveedor(self):
        self.root.withdraw()  
        new_root = ttk.Toplevel(self.root)  
        GenerarProveedor(new_root)
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def open_window_generar_producto(self):
        self.root.withdraw()  
        new_root = ttk.Toplevel(self.root)  
        #agregar clase (new_root)
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def on_close_window(self, window):
        window.destroy()  # Cierra la ventana
        self.root.deiconify()  # Muestra la ventana de gerente de nuevo

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MenuNuevosIngresos(root)
    root.mainloop()
