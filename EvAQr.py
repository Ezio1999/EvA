import tkinter as tk
from tkinter import messagebox
import qrcode
import os
from pathlib import Path
from tkinter import ttk
import json

#Ventana
def abrir_Ventana_qr():
    # Ventana Qr
    root = tk.Tk()
    root.title("EvA - Creación de Qr")
    root.geometry("400x150")

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
    tk.Label(entrada_frame, text="Matricula", fg="black").grid(row=3, column=0, padx=(0, 5), pady=5, sticky="w")
    matricula = ttk.Entry(entrada_frame)
    matricula.grid(row=3, column=1, padx=(0, 5), pady=5)


    # Frame de botones
    botones_frame = tk.Frame(root)
    botones_frame.pack(side="right", padx=10, fill="both", expand=True, pady=10)

    # Botones
    tk.Button(botones_frame, text="Crear QR", bg="gray", fg="black",command=lambda: main(nombre.get(), aPaterno.get(), aMaterno.get(), matricula.get())).pack(pady=10)
    # Funciones

    #Creacion de Qr
    def creacion_Qr(nombre, aPaterno, aMaterno, matricula):
        if not nombre or not aPaterno or not aMaterno or not matricula:
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        data = f"{nombre} {aPaterno} {aMaterno} - Matrícula: {matricula}" 

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

        # Crear un nombre de archivo usando el nombre completo
        nombre_archivo = f"{nombre}_{aPaterno}_{aMaterno}.png"
        ruta_completa = os.path.join(carpeta_imagenes, nombre_archivo)
        
        try:
            img.save(ruta_completa, format='PNG')
            messagebox.showinfo("Éxito", f"QR guardado en:\n{ruta_completa}")
            img.show()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el archivo: {str(e)}")

    #Limpiar campos de texto
    def limpiar_campos():
        nombre.delete(0, tk.END)
        aPaterno.delete(0, tk.END)
        aMaterno.delete(0, tk.END)
        matricula.delete(0, tk.END)

    def main(nombre, aPaterno, aMaterno, matricula):
        creacion_Qr(nombre, aPaterno, aMaterno, matricula)
        limpiar_campos()

    root.mainloop()

#llamado Prueva
#abrir_Ventana_qr()