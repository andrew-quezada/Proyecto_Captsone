import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import font as tkFont

class MenuSolicitudes:
    def __init__(self, root):
        self.root = root
        self.root.title("Nuevo Producto")

    # Obtener el tamaño de la pantalla
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Definir el tamaño de la ventana como el 100% del tamaño de la pantalla
        window_width = screen_width
        window_height = screen_height

        # Establecer el tamaño y la posición de la ventana
        self.root.geometry(f"{window_width}x{window_height}+0+0")

        # Configurar el comportamiento de la ventana para que no se pueda redimensionar
        self.root.resizable(True, True)

        


if __name__ == "__main__":    
    root = ttk.Window(themename="superhero")
    app = MenuSolicitudes(root)
    root.mainloop()