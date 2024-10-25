import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

class ProductoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modificar Producto")

        # Treeview para mostrar los productos
        self.tree = ttk.Treeview(root, columns=("id", "codigo", "nombre", "categoria", "precio_compra", "precio_venta", "stock", "proveedor"), show='headings')
        self.tree.heading('id', text="ID")
        self.tree.heading('codigo', text="Código de Barras")
        self.tree.heading('nombre', text="Nombre")
        self.tree.heading('categoria', text="Categoría")
        self.tree.heading('precio_compra', text="Precio de Compra")
        self.tree.heading('precio_venta', text="Precio de Venta")
        self.tree.heading('stock', text="Stock")
        self.tree.heading('proveedor', text="Proveedor")
        self.tree.pack()

        # Agregar algunos productos de ejemplo
        self.tree.insert('', 'end', values=(1, '12345', 'Producto A', 'Categoria A', 100, 150, 50, 'Proveedor 1'))
       
