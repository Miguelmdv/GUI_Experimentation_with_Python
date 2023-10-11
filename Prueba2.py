import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import filedialog
from tkinter import messagebox

# Función para abrir un archivo CSV y cargarlo en el DataFrame
def abrir_csv():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv")])

    if ruta_archivo:
        global df
        df = pd.read_csv(ruta_archivo)
        cargar_datos_en_tabla(df)

# Función para cargar los datos del DataFrame en la tabla
def cargar_datos_en_tabla(df):
    # Limpiar la tabla
    for i in tree.get_children():
        tree.delete(i)

    # Cargar datos en la tabla
    for _, fila in df.iterrows():
        tree.insert('', 'end', values=list(fila))

# Función para agregar una fila al DataFrame
def agregar_fila(df, cuadros_texto=[]):  
    # Crear cuadros de texto para ingresar datos
    for columna in df.columns:
        label = tk.Label(ventana, text=columna)
        label.pack()
        cuadro_texto = tk.Entry(ventana)
        cuadro_texto.pack()
        cuadros_texto.append(cuadro_texto)
        nueva_fila = []
        
    for cuadro_texto in cuadros_texto:
        valor = cuadro_texto.get()
        nueva_fila.append(valor)
        cuadro_texto.delete(0, tk.END)
    if nueva_fila:
        df.loc[len(df)] = nueva_fila
        cargar_datos_en_tabla(df)

# Función para eliminar una fila del DataFrame
def eliminar_fila():
    seleccion = tree.selection()
    if seleccion:
        index = int(seleccion[0][1])  # Obtener el índice de la fila seleccionada
        df.drop(df.index[index], inplace=True)
        cargar_datos_en_tabla(df)

# Función para guardar el DataFrame en un archivo CSV
def guardar_csv():
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("Archivos CSV", "*.csv")])
    if ruta_archivo:
        df.to_csv(ruta_archivo, index=False)
        messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")
        
# Crear un DataFrame vacío inicial
df = pd.DataFrame()

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Editar DataFrame")
ventana.geometry("400x400")

# Crear un botón para abrir un archivo CSV
boton_abrir = tk.Button(ventana, text="Abrir CSV", command=abrir_csv)
boton_abrir.pack()

# Crear un Treeview para mostrar el DataFrame
tree = ttk.Treeview(ventana, columns=[], show='headings')
tree.pack()



# Botones para agregar y eliminar filas
boton_agregar = tk.Button(ventana, text="Agregar Fila", command=lambda: agregar_fila(cuadros_texto))
boton_agregar.pack()
boton_eliminar = tk.Button(ventana, text="Eliminar Fila", command=eliminar_fila)
boton_eliminar.pack()

# Botón para guardar el DataFrame en un archivo CSV
boton_guardar = tk.Button(ventana, text="Guardar CSV", command=guardar_csv)
boton_guardar.pack()



# Asociar el Treeview con el DataFrame
cargar_datos_en_tabla(df)

ventana.mainloop()
