import json
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import folium
import webbrowser
from algoritmo_rutas import algoritmo_json

class Ubicacion:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class NodoUbicacion:
    def __init__(self, peso, ubicacion, anterior, siguiente):
        self.peso = peso
        self.ubicacion = ubicacion
        self.anterior = anterior
        self.siguiente = siguiente

class AplicacionBienvenida(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bienvenida")
        self.geometry("600x400")

        imagen = Image.open("bienvenida_imagen.png")
        imagen = imagen.resize((400, 200), Image.LANCZOS)
        imagen = ImageTk.PhotoImage(imagen)

        self.label_imagen = tk.Label(self, image=imagen)
        self.label_imagen.image = imagen
        self.label_imagen.pack(pady=20)

        self.label_bienvenida = tk.Label(self, text="¡Bienvenido al programa de gestión de puntos de entrega!")
        self.label_bienvenida.pack(pady=20)

        self.boton_siguiente = tk.Button(self, text="Siguiente", command=self.abrir_aplicacion_agregar_puntos)
        self.boton_siguiente.pack(pady=10)

    def abrir_aplicacion_agregar_puntos(self):
        self.destroy()
        app_agregar_puntos = AplicacionAgregarPuntos()
        app_agregar_puntos.mainloop()

class AplicacionAgregarPuntos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Añadir Puntos de Entrega")
        self.geometry("600x600")

        self.puntos_entrega = []

        self.label_instrucciones = tk.Label(self, text="Ingrese las coordenadas de los puntos de entrega (x, y):")
        self.label_instrucciones.pack(pady=10)

        self.entry_coordenadas = tk.Entry(self)
        self.entry_coordenadas.pack(pady=10)

        self.label_nombre_destino = tk.Label(self, text="Nombre del Destino:")
        self.label_nombre_destino.pack(pady=10)

        self.entry_nombre_destino = tk.Entry(self)
        self.entry_nombre_destino.pack(pady=10)

        self.boton_agregar_punto = tk.Button(self, text="Agregar Punto", command=self.agregar_punto)
        self.boton_agregar_punto.pack(pady=10)

        self.listbox_coordenadas = tk.Listbox(self, height=10, width=40)
        self.listbox_coordenadas.pack(pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar Puntos", command=self.guardar_puntos)
        self.boton_guardar.pack(pady=20)

        self.boton_mostrar_rutas = tk.Button(self, text="Mostrar Rutas", command=self.obtener_y_mostrar_rutas)
        self.boton_mostrar_rutas.pack(pady=20)
        
        self.boton_mostrar_mapa = tk.Button(self, text="Mostrar Mapa", command=self.mostrar_mapa)
        self.boton_mostrar_mapa.pack(pady=20)

    def mostrar_rutas(self, rutas_data):
        if not rutas_data:
            messagebox.showwarning("Advertencia", "No hay rutas para mostrar.")
            return

        ventana_rutas = tk.Toplevel(self)
        ventana_rutas.title("Rutas Calculadas")

        label_titulo = tk.Label(ventana_rutas, text="Rutas Calculadas:")
        label_titulo.pack(pady=10)
                
        for nombre_ruta, info_ruta in rutas_data.items():
            label_ruta = tk.Label(ventana_rutas, text=f'{nombre_ruta}:', font=("Helvetica", 12, "bold"))
            label_ruta.pack()

            direcciones = info_ruta['direcciones']
            peso = info_ruta['peso']

            label_peso = tk.Label(ventana_rutas, text=f'Peso de la ruta: {peso}', font=("Helvetica", 10, "italic"))
            label_peso.pack()

            for direccion in direcciones:
                nombre = direccion['nombre']
                coordenadas = direccion['coordenadas']
                label_direccion = tk.Label(ventana_rutas, text=f'{nombre}: {coordenadas}', wraplength=300)
                label_direccion.pack()

        ventana_rutas.mainloop()

    def agregar_punto(self):
        try:
            coordenadas = tuple(map(float, self.entry_coordenadas.get().split(',')))
            nombre_destino = self.entry_nombre_destino.get()

            if not nombre_destino:
                messagebox.showerror("Error", "Ingrese un nombre para el destino.")
                return

            ubicacion = Ubicacion(coordenadas[0], coordenadas[1])
            nodo_anterior = None
            nodo_siguiente = None
            nuevo_nodo = NodoUbicacion(0, ubicacion, nodo_anterior, nodo_siguiente)
            nuevo_nodo.nombre_destino = nombre_destino

            if self.puntos_entrega:
                self.puntos_entrega[-1].siguiente = nuevo_nodo
                nuevo_nodo.anterior = self.puntos_entrega[-1]

            self.puntos_entrega.append(nuevo_nodo)
            messagebox.showinfo("Éxito", "Punto agregado correctamente.")
            self.entry_coordenadas.delete(0, tk.END)
            self.entry_nombre_destino.delete(0, tk.END)
            self.actualizar_lista_coordenadas()
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese coordenadas válidas (x, y).")

    def actualizar_lista_coordenadas(self):
        self.listbox_coordenadas.delete(0, tk.END)
        for nodo in self.puntos_entrega:
            ubicacion = nodo.ubicacion
            nombre_destino = nodo.nombre_destino
            self.listbox_coordenadas.insert(tk.END, f"{nombre_destino} ({ubicacion.x}, {ubicacion.y})")

    def guardar_puntos(self):
        if not self.puntos_entrega:
            messagebox.showwarning("Advertencia", "No hay puntos para guardar.")
            return

        try:
            puntos_data = []
            for nodo in self.puntos_entrega:
                ubicacion = nodo.ubicacion
                nombre_destino = nodo.nombre_destino
                puntos_data.append({
                    'nombre': nombre_destino,
                    'coordenadas': {'latitud': ubicacion.x, 'longitud': ubicacion.y}
                })

            with open('puntos_entrega.json', 'w') as json_file:
                json.dump(puntos_data, json_file, indent=2)

            messagebox.showinfo("Éxito", "Puntos guardados en 'puntos_entrega.json'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los puntos: {e}")

    def obtener_y_mostrar_rutas(self):
        
        try:
            algoritmo_json()
            # Leer rutas desde el archivo JSON
            with open('rutas.json', 'r') as json_file:
                rutas_data = json.load(json_file)
    
            # Mostrar rutas en una ventana
            self.mostrar_rutas(rutas_data)
    
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron obtener las rutas: {e}")
            
    def mostrar_mapa(self):
        try:
            # Leer direcciones desde el archivo JSON
            with open('rutas.json', 'r') as json_file:
                rutas_data = json.load(json_file)

            if not rutas_data:
                messagebox.showwarning("Advertencia", "No hay rutas para mostrar.")
                return

            # Crear un archivo HTML con el mapa utilizando la biblioteca folium
            mapa = folium.Map(location=[rutas_data['Ruta_1']['direcciones'][0]['coordenadas']['latitud'],
                                        rutas_data['Ruta_1']['direcciones'][0]['coordenadas']['longitud']],
                              zoom_start=14)

            for nombre_ruta, info_ruta in rutas_data.items():
                direcciones = info_ruta['direcciones']

                for direccion in direcciones:
                    coordenadas = direccion['coordenadas']
                    folium.Marker([coordenadas['latitud'], coordenadas['longitud']], popup=direccion['nombre']).add_to(mapa)

            mapa.save("mapa.html")

            # Abrir el archivo HTML en el navegador predeterminado
            webbrowser.open("mapa.html")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar el mapa: {e}")

if __name__ == "__main__":
    app_bienvenida = AplicacionBienvenida()
    app_bienvenida.mainloop()
