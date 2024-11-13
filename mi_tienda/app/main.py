from gui.login import Login
import ttkbootstrap as ttk
from settings import create_connection

def main():
    # Inicializa la conexión a la base de datos y guarda la conexión
    conn = create_connection()

    # Configura la ventana principal de la aplicación con ttkbootstrap
    root = ttk.Window(themename="superhero")
    app = Login(root)

    # Inicia el bucle principal de la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()
