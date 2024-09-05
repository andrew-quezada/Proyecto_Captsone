import tkinter as tk
from tkinter import messagebox
from db.models import validacion_usuario, verificar_exitencia
from gui.VentanaGerente import VentanaGerente
from gui.VentanaCaja import VentanaCaja
import ttkbootstrap as ttk

class Login:
    def __init__(self, root):
        self.root = root
        self.root.title("Tienda madrileña")
        
        frame = tk.Frame(root)
        frame.pack(expand=True, fill='both')
        
        # Crear y agregar etiquetas y entradas de usuario y contraseña
        tk.Label(frame, text="Usuario:").pack(pady=(20, 5))  
        self.user_entry = tk.Entry(frame)
        self.user_entry.pack(pady=5)
        
        tk.Label(frame, text="Contraseña:").pack(pady=(20, 5))
        self.pass_entry = tk.Entry(frame, show="*")
        self.pass_entry.pack(pady=5)
        
        # Crear y agregar el botón de inicio de sesión
        button = tk.Button(frame, text="Iniciar sesión", command=self.login)
        button.pack(pady=(20, 10))  

        # Establecer el tamaño mínimo de la ventana
        self.root.minsize(300, 150)
    
    def login(self):
        username = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Por favor, ingrese todos los datos.")
            return
        
        if not verificar_exitencia(username):
            messagebox.showerror("Error", "El usuario no existe.")
            return
        
        user_id, cargo_id = validacion_usuario(username, password)
        
        if user_id is None:
            messagebox.showerror("Error", "Usuario o contraseña no coinciden.")
        elif cargo_id == 1:  # el id_cargo 1 es para gerente
            self.open_gerente_window()
        elif cargo_id == 2:  # el id_cargo 2 es para cajero
            self.open_caja_window()
    
    def open_gerente_window(self):
        self.root.withdraw()  # Oculta la ventana principal
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija
        app = VentanaGerente(new_root)
        
        # Asegúrate de que la ventana principal se muestre al cerrar la nueva ventana
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))

    def open_caja_window(self):
        self.root.withdraw()  # Oculta la ventana principal
        new_root = ttk.Toplevel(self.root)  # Crea una nueva ventana hija
        app = VentanaCaja(new_root)
        
        # Asegúrate de que la ventana principal se muestre al cerrar la nueva ventana
        new_root.protocol("WM_DELETE_WINDOW", lambda: self.on_close_window(new_root))
    
    def on_close_window(self, window):
        window.destroy()  # Cierra la ventana actual
        self.root.deiconify()  # Vuelve a mostrar la ventana principal

if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = Login(root)
    root.mainloop()
