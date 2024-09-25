import ttkbootstrap as ttk

class Reg_nuevo_prod:
    def __init__(self, root):
        self.root = root
        self.root.title("Ingresar producto nuevo")


if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = Reg_nuevo_prod(root)
    root.mainloop()