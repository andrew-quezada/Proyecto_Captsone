import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkFont
from PIL import Image, ImageTk
from gui.generar_proveedor import GenerarProveedor
from gui.generar_producto import GenerarProducto

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

        # Configurar el comportamiento de la ventana para que sea redimensionable
        self.root.resizable(True, True)

        # Crear un contenedor para los botones
        self.contenedor = tk.Frame(self.root)
        self.contenedor.pack(expand=True, fill=tk.BOTH, pady=20, padx=20)

        # Crear una fuente personalizada
        fuente_personalizada = tkFont.Font(family="Arial", size=14, weight="bold")

        # Crear y configurar un estilo personalizado para el botón
        style = ttk.Style()
        style.configure("Custom.TButton", font=fuente_personalizada, anchor="center")

        # Cargar y redimensionar íconos usando Pillow, guardándolos en el objeto self
        self.icono_producto = ImageTk.PhotoImage(Image.open("app/img/boxes.png").resize((50, 50)))
        self.icono_proveedor = ImageTk.PhotoImage(Image.open("app/img/user-add.png").resize((50, 50)))

        # Crear el botón con el ícono y el estilo personalizado
        boton1 = ttk.Button(self.contenedor, text="Nuevo producto", image=self.icono_producto, compound="top", 
                            style="Custom.TButton", bootstyle=SUCCESS, command=self.open_window_generar_producto)
        boton2 = ttk.Button(self.contenedor, text="Nuevo proveedor", image=self.icono_proveedor, compound="top", 
                            style="Custom.TButton", bootstyle=SUCCESS, command=self.open_window_generar_proveedor)
        
        boton1.grid(row=1, column=0, padx=20, pady=40, ipadx=80, ipady=150)
        boton2.grid(row=1, column=1, padx=20, pady=40, ipadx=80, ipady=150)

        self.contenedor.columnconfigure([0, 1], weight=1)
        self.contenedor.rowconfigure([0, 1], weight=0)

    def open_window_generar_proveedor(self):
        self.root.withdraw()  
        new_root = ttk.Toplevel(self.root)  
        GenerarProveedor(new_root)
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def open_window_generar_producto(self):
        self.root.withdraw()  
        new_root = ttk.Toplevel(self.root)  
        GenerarProducto(new_root)
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def on_close_window(self, window):
        window.destroy()  # Cierra la ventana
        self.root.deiconify()  # Muestra la ventana principal de nuevo

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MenuNuevosIngresos(root)
    root.mainloop()
