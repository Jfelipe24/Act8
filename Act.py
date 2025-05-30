import tkinter as t
from tkinter import messagebox, simpledialog
import json
import csv
import pandas as p
import matplotlib.pyplot as plt

estructura = {}


def CrearEstructura():
    try:
        salones = int(entry_salones.get())
        mesas = int(entry_mesas.get())  
        jurados = int(entry_jurados.get())

        if salones <= 0 or mesas <= 0 or jurados <= 0:  
            raise ValueError

        for limwindow in frame_estructura.winfo_children():
            limwindow.destroy()  

        estructura.clear()  

        for s in range(1, salones + 1):
            salonNombre = f"salon{s}"  
            estructura[salonNombre] = {}

            t.Label(frame_estructura, text=salonNombre).pack()  # muestra el salon

            for m in range(1, mesas + 1):
                mesaNombre = f"mesa{m}" 
                estructura[salonNombre][mesaNombre] = {"jurados": []}

                boton_mesa = t.Button(frame_estructura, text=mesaNombre,
                                      command=lambda s=salonNombre, m=mesaNombre: verjurados(s, m))
                boton_mesa.pack(padx=10, pady=2)  
                for j in range(1, jurados + 1):
                    boton_jurado = t.Button(frame_estructura, text=f"{mesaNombre} - Jurado {j}",
                                            command=lambda s=salonNombre, m=mesaNombre: RegistroDeJurados(s, m))
                    boton_jurado.pack(padx=20, pady=1)  
    except ValueError:  
        messagebox.showerror("error", "solo puedes ingresar numeros enteros positivos")

# esta funcion sirve para registrar a los jurados 
def RegistroDeJurados(salon, mesa):
    nombre = simpledialog.askstring("nombre", "ingrese el nombre")
    cedula = simpledialog.askstring("cedula", "ingrese la cedula")
    telefono = simpledialog.askstring("telefono", "ingrese el telefono")
    direccion = simpledialog.askstring("direccion", "ingrese la direccion")

    if not all([nombre, cedula, telefono, direccion]):
        messagebox.showerror("error", "tienes que llenar todos los campos es obligatorio")
        return  # esto verifica que no quede ningun valor sin llenar 

    jurado = {"nombre": nombre, "cedula": cedula, "telefono": telefono, "direccion": direccion}
    estructura[salon][mesa]["jurados"].append(jurado)  
    messagebox.showinfo("exito", "el jurado fue registrado con exito")


def verjurados(salon, mesa):
    jurados = estructura[salon][mesa]["jurados"]

    if not jurados:  
        messagebox.showinfo("informacion", f"no hay jurados en {mesa}")
    else:  
        texto = "\n".join([f"{j['nombre']}, cedula: {j['cedula']}" for j in jurados])
        messagebox.showinfo("jurados", f"jurados en {mesa}:\n{texto}")

def guardarEstructura():
    with open("estructura.json", "w", encoding="utf-8") as folder:
        json.dump(estructura, folder, indent=4)
    messagebox.showinfo("guardado", "el archivo fue guardado exitosamente")


def cargarEstructura():
    global estructura
    try:
        with open("estructura.json", "r", encoding="utf-8") as folder:
            estructura = json.load(folder)
        messagebox.showinfo("cargado", "el archivo fue cargado exitosamente")
    except FileNotFoundError:
        messagebox.showerror("error", "archivo no encontrado")
def cargarvotantescsv():
    try:
        with open("votantes.csv", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            for fila in lector:
                nombre = fila["nombre"]
                cedula = fila["cedula"]
                salon = fila ["salon"]
                mesa = fila ["mesa"]
                
                if salon not in estructura:
                    messagebox.showerror("error",f"el salon {salon} no existe")
                    continue
                if mesa not in estructura[salon]:
                    messagebox.showerror("error",f"la mesa {mesa} no existe en {salon}")
                    continue
                if "votantes" not in estructura[salon][mesa]:
                    estructura[salon][mesa]["votantes"]= []
                existentes= [v["cedula"]for v in estructura[salon][mesa]["votantes"]]    
                if cedula in existentes:
                    continue
                estructura[salon][mesa]["votantes"].append({"nombre":nombre, "cedula":cedula})
                messagebox.showinfo("exito","el votante fue cargado con exito")
    except FileNotFoundError:
        messagebox.showerror("error","el archivo de votantes.csv no se encontro")

