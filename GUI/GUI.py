import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  #libreria Pillow para insertar imágenes

class AplicacionBienvenida(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Bienvenida")
        self.geometry("600x400")

        # Cargar la imagen
        imagen = Image.open("bienvenida_imagen.png")  # Cambiar "bienvenida_imagen.png" al nombre de la imagen que se guardo
        imagen = imagen.resize((400, 200), Image.ANTIALIAS)
        imagen = ImageTk.PhotoImage(imagen)

        # Mostrar la imagen en un Label
        self.label_imagen = tk.Label(self, image=imagen)
        self.label_imagen.image = imagen
        self.label_imagen.pack(pady=20)

        self.label_bienvenida = tk.Label(self, text="¡Bienvenido al programa de gestión de puntos de entrega!")
        self.label_bienvenida.pack(pady=20)

        self.boton_siguiente = tk.Button(self, text="Siguiente", command=self.abrir_aplicacion_agregar_puntos)
        self.boton_siguiente.pack(pady=10)

    def abrir_aplicacion_agregar_puntos(self):
        self.destroy()  # Cierra la ventana actual
        app_agregar_puntos = AplicacionAgregarPuntos()
        app_agregar_puntos.mainloop()

class AplicacionAgregarPuntos(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Añadir Puntos de Entrega")
        self.geometry("400x400")

        self.puntos_entrega = []

        self.label_instrucciones = tk.Label(self, text="Ingrese las coordenadas de los puntos de entrega (x, y):")
        self.label_instrucciones.pack(pady=10)

        self.entry_coordenadas = tk.Entry(self)
        self.entry_coordenadas.pack(pady=10)

        self.boton_agregar_punto = tk.Button(self, text="Agregar Punto", command=self.agregar_punto)
        self.boton_agregar_punto.pack(pady=10)

        self.listbox_coordenadas = tk.Listbox(self, height=10, width=40)
        self.listbox_coordenadas.pack(pady=10)

        self.boton_guardar = tk.Button(self, text="Guardar Puntos", command=self.guardar_puntos)
        self.boton_guardar.pack(pady=20)

    def agregar_punto(self):
        try:
            coordenadas = tuple(map(float, self.entry_coordenadas.get().split(',')))
            self.puntos_entrega.append(coordenadas)
            messagebox.showinfo("Éxito", "Punto agregado correctamente.")
            self.entry_coordenadas.delete(0, tk.END)  # Limpia la entrada después de agregar el punto
            self.actualizar_lista_coordenadas()  # Llama a la función para actualizar la lista de coordenadas
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese coordenadas válidas (x, y).")

    def actualizar_lista_coordenadas(self):
        # Borra el contenido actual de la Listbox
        self.listbox_coordenadas.delete(0, tk.END)
        # Agrega las nuevas coordenadas a la Listbox
        for punto in self.puntos_entrega:
            self.listbox_coordenadas.insert(tk.END, f"{punto[0]}, {punto[1]}")

    def guardar_puntos(self):
        if not self.puntos_entrega:
            messagebox.showwarning("Advertencia", "No hay puntos para guardar.")
            return

        try:
            with open('puntos_entrega.txt', 'w') as f:
                for punto in self.puntos_entrega:
                    f.write(f"{punto[0]}, {punto[1]}\n")
            messagebox.showinfo("Éxito", "Puntos guardados en 'puntos_entrega.txt'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar los puntos: {e}")

if __name__ == "__main__":
    app_bienvenida = AplicacionBienvenida()
    app_bienvenida.mainloop()
