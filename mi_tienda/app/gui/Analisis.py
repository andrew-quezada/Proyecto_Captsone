import tkinter as tk
from tkinter import ttk
from db.predicciones import obtener_datos, procesar_datos
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from prophet import Prophet
import ttkbootstrap as ttk
import pandas as pd

class AnalisisPredictivo:
    def __init__(self, root):
        self.root = root
        self.root.title("Predicción de Demanda")
        self.root.state("zoomed")  # Ventana maximizada

        self.datos = obtener_datos()
        if self.datos is None:
            ttk.Label(self.root, text="No se pudieron cargar los datos", foreground="red").pack()
            return
        self.serie_temporal = procesar_datos(self.datos)
        
        # Crear selector de producto
        ttk.Label(self.root, text="Seleccione un producto:", font=("Helvetica", 14)).pack(pady=10)
        self.combo_producto = ttk.Combobox(self.root, values=self.serie_temporal.columns.tolist(), state="readonly", font=("Helvetica", 12))
        self.combo_producto.pack(pady=5)

        # Botón para generar predicción
        self.boton_generar = ttk.Button(self.root, text="Generar Predicción", command=self.generar_prediccion, bootstyle="primary")
        self.boton_generar.pack(pady=20)

        # Área para mostrar el gráfico
        self.grafico_frame = ttk.Frame(self.root)
        self.grafico_frame.pack(fill="both", expand=True)

    def entrenar_modelo(self, id_producto):
        """Entrena un modelo Prophet para predecir ventas."""
        print("antes", self.serie_temporal.columns)
        print(self.serie_temporal.head())
        #self.serie_temporal = self.serie_temporal.reset_index()
        #print("despues",self.serie_temporal.columns)
        #print(self.serie_temporal.head())
        try:
            # Verificar si la columna 'id_producto' está en el DataFrame
            if 'id_producto' not in self.serie_temporal.columns:
                print(f"Error: No se encuentra la columna 'id_producto' en los datos.")
                return None
            else:
                print(f"Columna 'id_producto' encontrada en los datos.")

            # Filtrar los datos según el id_producto
            datos_producto = self.serie_temporal[self.serie_temporal['id_producto'] == id_producto]

            if datos_producto.empty:
                print(f"No se encontraron datos para el id_producto {id_producto}.")
            else:
                print(f"Se han encontrado {len(datos_producto)} registros para el id_producto {id_producto}.")

            # Preparar los datos para Prophet (asegurándote de que tengan el formato correcto)
            datos_producto = datos_producto.reset_index()  # Si el índice es 'fecha', resetearlo
            datos_producto = datos_producto.rename(columns={'fecha': 'ds', 'cantidad': 'y'})  # Prophet requiere 'ds' y 'y'

            # Crear el modelo Prophet
            modelo = Prophet()

            # Ajustar el modelo con los datos
            modelo.fit(datos_producto)

            # Realizar predicciones
            futuro = modelo.make_future_dataframe(datos_producto, periods=365)  # Predecir un año de datos adicionales
            pronostico = modelo.predict(futuro)

            return pronostico

        except KeyError as e:
            print(f"Error de clave: {e}")
            return None
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")
            return None


    def mostrar_grafico(self, predicciones):
        """Muestra un gráfico con las predicciones."""
        if predicciones is None:
            print("No se pudieron generar predicciones.")
            return
        
        # Limpiar gráficos previos
        for widget in self.grafico_frame.winfo_children():
            widget.destroy()

        # Crear figura de matplotlib
        fig = Figure(figsize=(10, 6))
        ax = fig.add_subplot(111)
        ax.plot(predicciones['ds'], predicciones['yhat'], label='Predicción')
        ax.fill_between(predicciones['ds'], predicciones['yhat_lower'], predicciones['yhat_upper'], color='blue', alpha=0.2)
        ax.set_title("Predicción de Ventas")
        ax.set_xlabel("Fecha")
        ax.set_ylabel("Cantidad")
        ax.legend()

        # Mostrar gráfico en la interfaz
        canvas = FigureCanvasTkAgg(fig, self.grafico_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)


    def generar_prediccion(self):
        """Genera una predicción y muestra el gráfico."""
        id_producto = self.combo_producto.get()
        if not id_producto:
            ttk.Label(self.root, text="Seleccione un producto válido", foreground="red").pack()
            return

        predicciones = self.entrenar_modelo(id_producto)
        self.mostrar_grafico(predicciones)

# Ejecutar la aplicación
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")  # Estilo personalizado de ttkbootstrap
    app = AnalisisPredictivo(root)
    root.mainloop()
