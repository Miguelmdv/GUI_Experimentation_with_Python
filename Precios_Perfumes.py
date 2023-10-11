import pandas as pd
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import messagebox
import os

ruta_valida = False
nombre_archivo = "data/Precios_Perfumes.csv"
ruta_reciente = "content/rutas_recientes.txt"
# Obtiene la ruta de origen del archivo actual
ruta_origen = os.path.dirname(__file__)

def crear_df(ruta):
    df = pd.DataFrame(
        columns=[
            "Marca",
            "Nombre",
            "Precio_actual",
            "Precio_por_100_ml",
            "ml",
            "Fecha",
            "Hora",
        ],
        index=[0],
    )

    df.drop(df.index[0], inplace=True)  ## Elimina la primera fila vacia
    df.to_csv(ruta, index=False)

    return df

def escribir_df(df, precio, calc, ml, marca, nombre):
    now = datetime.today()
    fecha, hora = now.strftime("%d-%m-%Y %H:%M:%S").split(" ")
    nueva_fila = [marca, nombre, precio, calc, ml, fecha, hora]
    # df = pd.concat([df, pd.DataFrame([nueva_fila])], ignore_index=True)
    df.loc[len(df)] = nueva_fila  # only use with a RangeIndex!

    return df

def crear_archivo():
    # Abre un cuadro de diálogo para que el usuario seleccione la ubicación y el nombre del archivo
    nombre_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos de datos", "*.csv")])

    if nombre_archivo:
        crear_df(nombre_archivo)
        escribir_reciente(nombre_archivo)

        messagebox.showinfo("Éxito", f"Archivo '{nombre_archivo}' creado y contenido guardado.")
        
        return nombre_archivo

def abrir_archivo():
    ruta_valida = False

    # Crea una ventana principal para que el cuadro de diálogo sea modal
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal

    # Abre el cuadro de diálogo para seleccionar un archivo en la ruta de origen
    nombre_archivo = filedialog.askopenfilename(initialdir=ruta_origen)

    if nombre_archivo:
        _, extension = os.path.splitext(nombre_archivo)
        if extension.lower() != ".csv":
            print("El archivo seleccionado no es un archivo CSV.")
        else:
            print("Archivo CSV seleccionado:", nombre_archivo)
            escribir_reciente(nombre_archivo)
            ruta_valida = True
            
    else:
        print("Ningún archivo seleccionado")

    root.destroy()
    return nombre_archivo, ruta_valida


def ver_df(ruta, ventana):
    # ventana = tk.Tk()
    ventana.title("Visualización de DataFrame")

    # Leer el DataFrame del archivo
    df = pd.read_csv(ruta, sep=",")

    # Crear un Treeview para mostrar el DataFrame
    tree = ttk.Treeview(ventana, columns=list(df.columns), show='headings')

    # Configurar encabezados
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # Establecer el ancho de las columnas

    # Llenar el Treeview con los datos del DataFrame
    for i, row in df.iterrows():
        tree.insert('', 'end', values=list(row))

    tree.pack()
    
def leer_reciente():
    with open(ruta_reciente, 'r') as archivo:
        linea = ""
        try:
            linea = archivo.readlines()[-1]
            linea = linea[:-1]
            print("Primera línea del archivo:", linea)
            
            return linea
        
        except IndexError:
            print("No hay archivos recientes")
            messagebox.showinfo("Fallo", "No hay archivos recientes")
            return None
        
def leer_lista_recientes():
    lineas = []
    with open(ruta_reciente, 'r') as archivo:
        for linea in archivo:
            lineas.append(linea[:-1])
        if not lineas:
            print("El archivo está vacío o no se encontraron más líneas.")

    return lineas
    
    
def escribir_reciente(ruta):
    with open(ruta_reciente, 'a+') as archivo:
        rutas = leer_lista_recientes()
        if ruta not in rutas: 
            linea = archivo.write(f"{ruta}\n")
            print(linea)
            if not linea:
                print("No se pudo escribir el archivo")
            else:
                print("Linea a escribir:", ruta)
        else:
            print("Ya existe ese archivo, no se va a añadir a recientes otra vez")

def get_prompt(titulo, objetivo):
    result = simpledialog.askstring(titulo, objetivo)
    if result:
        print(objetivo, result)
    return result
            
def nueva_entrada(ruta_valida, nombre_archivo):
    if ruta_valida:
        n_incorrecto = True
        precio = None
        ml = None
        calc = 0
        try:
            df = pd.read_csv(nombre_archivo, sep=",")
        except FileNotFoundError:
            df = crear_df(nombre_archivo)
        
        marca = get_prompt("Marca", "Marca del producto: ")
        if marca:
            nombre = get_prompt("Nombre","Nombre del producto: ")
            if nombre:
                while n_incorrecto:
                    precio = get_prompt("Precio", "Precio actual: ")
                    if precio:
                        try:
                            precio = float(precio)
                        except ValueError:
                            print(precio, "no son numeros válidos")
                            messagebox.showinfo("Fallo", f"{precio} no son numeros válidos")
                        if precio is float:
                            while n_incorrecto:
                                ml = get_prompt("ml", "ml del bote: ")
                                if ml:
                                    try:
                                        ml = float(ml)
                                    except ValueError:
                                        print(ml, "no son numeros válidos")
                                        messagebox.showinfo("Fallo", f"{ml} no son numeros válidos")

                                    if ml is float:
                                        n_incorrecto = False   
                                        calc = 100.0 * precio / ml

                                        df = escribir_df(df, precio, calc, ml, marca, nombre)
                                        df.to_csv(nombre_archivo, index=False, sep=",")



    # Funciones para las opciones
def opcion_nuevo():
    nombre_archivo = crear_archivo()
    ver_df(nombre_archivo, ventana)

def opcion_abrir():
    global nombre_archivo, ruta_valida
    nombre_archivo, ruta_valida = abrir_archivo()
    ver_df(nombre_archivo, ventana)

def opcion_ultimo():
    ruta = leer_reciente()
    if ruta:
        ver_df(ruta, ventana)
def opcion_recientes(ruta):
    if ruta:
        ver_df(ruta, ventana)

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Comparador de precios de perfumes")

# Cambiar el tamaño inicial de la ventana
ventana.geometry("400x300")  # Cambia el tamaño a 400 píxeles de ancho y 300 píxeles de alto

# Crear el menú
menu = tk.Menu(ventana)
ventana.config(menu=menu)


filemenu = tk.Menu(menu, tearoff=0)
editmenu = tk.Menu(menu, tearoff=0)
helpmenu = tk.Menu(menu, tearoff=0)
recentmenu = tk.Menu(menu, tearoff=0)

# Agregar el submenú al menú principal
menu.add_cascade(label="Archivo", menu=filemenu)
menu.add_cascade(label="Editar", menu=editmenu)
menu.add_cascade(label="Ayuda", menu=helpmenu)

# Crear un submenú

filemenu.add_command(label="Nueva base de datos", command=opcion_nuevo)
filemenu.add_command(label="Abrir csv", command=opcion_abrir)
filemenu.add_command(label="Ultimo archivo", command=opcion_ultimo)

rutas_recientes = []
with open(ruta_reciente, 'a+') as archivo:
        rutas_recientes = leer_lista_recientes()
filemenu.add_cascade(label="Archivos recientes", menu=recentmenu)

for element in rutas_recientes:
    recentmenu.add_command(label=element, command=lambda: opcion_recientes(element))

filemenu.add_separator()
filemenu.add_command(label="Salir", command=menu.quit)

editmenu.add_command(label="Añadir", command=lambda: nueva_entrada(ruta_valida, nombre_archivo))

helpmenu.add_command(label="Versión",  command=lambda: messagebox.showinfo("By me", "v0.1"))


# Asociar el menú con la ventana
ventana.config(menu=menu)

ventana.mainloop()