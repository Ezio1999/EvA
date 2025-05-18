import tkinter as tk
from tkinter import messagebox
import qrcode
import os
from pathlib import Path
from tkinter import ttk
import json

# Cargar carreras desde archivo
def cargar_carreras():
    try:
        with open('carreras.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return ["Estilismo", "Inglés"]

# Guardar carreras en archivo
def guardar_carreras(carreras):
    with open('carreras.json', 'w') as file:
        json.dump(carreras, file)

opciones = cargar_carreras()

#Ventana
def abrir_Ventana_qr():
    # Ventana Qr
    root = tk.Tk()
    root.title("EvA - Creación de Qr")
    root.geometry("400x200")

    # Frame para los campos de texto
    entrada_frame = tk.Frame(root)
    entrada_frame.pack(side="left", padx=10, fill="both", expand=True, pady=10)

    # Etiquetas y campos de texto
    tk.Label(entrada_frame, text="Nombre", fg="black").grid(row=0, column=0, padx=(0, 5), pady=5, sticky="w")
    nombre = tk.Entry(entrada_frame)
    nombre.grid(row=0, column=1, padx=(0, 5), pady=5)

    tk.Label(entrada_frame, text="Apellido Paterno", fg="black").grid(row=1, column=0, padx=(0, 5), pady=5, sticky="w")
    aPaterno = tk.Entry(entrada_frame)
    aPaterno.grid(row=1, column=1, padx=(0, 5), pady=5)

    tk.Label(entrada_frame, text="Apellido Materno", fg="black").grid(row=2, column=0, padx=(0, 5), pady=5, sticky="w")
    aMaterno = tk.Entry(entrada_frame)
    aMaterno.grid(row=2, column=1, padx=(0, 5), pady=5)

    # ComboBox de Carreras
    tk.Label(entrada_frame, text="Carrera", fg="black").grid(row=3, column=0, padx=(0, 5), pady=5, sticky="w")
    combo = ttk.Combobox(entrada_frame, values=opciones)
    combo.current(0)
    combo.grid(row=3, column=1, padx=(0, 5), pady=5)

    # Frame para gestionar carreras
    gestion_frame = tk.Frame(entrada_frame)
    gestion_frame.grid(row=4, column=0, columnspan=2, pady=5)

    # Campo para nueva carrera
    nueva_carrera = tk.Entry(gestion_frame, width=20)
    nueva_carrera.grid(row=0, column=0, padx=5)

    # Botones para gestionar carreras
    tk.Button(gestion_frame, text="Agregar", command=lambda: agregar_carrera(nueva_carrera.get())).grid(row=0, column=1, padx=5)
    tk.Button(gestion_frame, text="Eliminar", command=lambda: eliminar_carrera(combo.get())).grid(row=0, column=2, padx=5)

    # Frame de botones
    botones_frame = tk.Frame(root)
    botones_frame.pack(side="right", padx=10, fill="both", expand=True, pady=10)

    # Botones
    tk.Button(botones_frame, text="Crear QR", bg="gray", fg="black",command=lambda: main(nombre.get(), aPaterno.get(), aMaterno.get(), combo.get())).pack(pady=10)
    # Funciones

    #Creacion de Qr
    def creacion_Qr(nombre, aPaterno, aMaterno, carrera):
        if not nombre or not aPaterno or not aMaterno:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        data = f"{nombre} {aPaterno} {aMaterno} - {carrera}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )

        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")

        # Guardar imagen en la carpeta Imágenes
        carpeta_imagenes = os.path.join(Path.home(), "Pictures")
        if not os.path.exists(carpeta_imagenes):
            os.makedirs(carpeta_imagenes)

        ruta_completa = os.path.join(carpeta_imagenes, f"{data}.png")
        img.save(ruta_completa)

        messagebox.showinfo("Éxito", f"QR guardado en:\n{ruta_completa}")
        img.show()

    #Limpiar campos de texto
    def limpiar_campos():
        nombre.delete(0, tk.END)
        aPaterno.delete(0, tk.END)
        aMaterno.delete(0, tk.END)
        combo.current(0)
        nueva_carrera.delete(0, tk.END)

    def agregar_carrera(carrera):
        if carrera and carrera not in opciones:
            opciones.append(carrera)
            combo["values"] = opciones
            combo.current(len(opciones) - 1)
            nueva_carrera.delete(0, tk.END)
            guardar_carreras(opciones)  # Guardar después de agregar
            messagebox.showinfo("Éxito", f"Carrera '{carrera}' agregada correctamente")
        elif carrera in opciones:
            messagebox.showwarning("Advertencia", "Esta carrera ya existe")
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingresa un nombre de carrera")

    def eliminar_carrera(carrera):
        if carrera in opciones:
            opciones.remove(carrera)
            combo["values"] = opciones
            if opciones:
                combo.current(0)
            else:
                combo.set("")
            guardar_carreras(opciones)  # Guardar después de eliminar
            messagebox.showinfo("Éxito", f"Carrera '{carrera}' eliminada correctamente")
        else:
            messagebox.showwarning("Advertencia", "Selecciona una carrera para eliminar")

    def main(nombre, aPaterno, aMaterno, carrera):
        creacion_Qr(nombre, aPaterno, aMaterno, carrera)
        limpiar_campos()

    root.mainloop()

#llamado Prueva
#abrir_Ventana_qr()