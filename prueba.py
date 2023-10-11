import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog

# Función para abrir un archivo y mostrar su contenido
def abrir_archivo():
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            contenido = archivo.read()
            texto.delete('1.0', tk.END)
            texto.insert('1.0', contenido)

# Función para guardar el contenido actual en un archivo
def guardar_archivo():
    contenido = texto.get('1.0', tk.END)
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])

    if ruta_archivo:
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(contenido)
        messagebox.showinfo("Guardado", "Archivo guardado exitosamente.")

# Función para copiar el texto seleccionado
def copiar():
    texto.clipboard_clear()
    texto.clipboard_append(texto.get(tk.SEL_FIRST, tk.SEL_LAST))

# Función para pegar el texto desde el portapapeles
def pegar():
    texto.insert(tk.INSERT, texto.clipboard_get())

# Crear la ventana principal
ventana = tk.Tk()
ventana.title("Editor de Texto")

# Menú principal
menu = tk.Menu(ventana)
ventana.config(menu=menu)

# Menú Archivo
menu_archivo = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Archivo", menu=menu_archivo)
menu_archivo.add_command(label="Abrir", command=abrir_archivo)
menu_archivo.add_command(label="Guardar", command=guardar_archivo)

# Menú Editar
menu_editar = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Editar", menu=menu_editar)
menu_editar.add_command(label="Copiar", command=copiar)
menu_editar.add_command(label="Pegar", command=pegar)

# Widget de texto
texto = tk.Text(ventana)
texto.pack()

ventana.mainloop()
