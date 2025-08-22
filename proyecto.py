#Importamos las librerías necesarias
#Librería estándar para crear interfaces gráficas
import tkinter as tk  

#Para seleccionar archivos, colores y mostrar mensajes
from tkinter import filedialog, colorchooser, messagebox  

#Módulo para trabajar con datos en formato JSON (JavaScript Object Notation)
import json  

#Módulo que permite trabajar con el sistema operativo (archivos, rutas, etc.)
import os  

#Configuracion del archivo
CONFIG_FILE = "config.json"

#Valores por defecto
config = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "claro",
    "idioma": "es-ES",
    "tamaño_fuente": 12,
    "color_menu": "#ffffff",
    "color_letra": "#000000",
    "foto_perfil": ""
}

def cargar_config():
    global config
    #os.path.exists() verifica si el archivo existe en el directorio actual
    if os.path.exists(CONFIG_FILE):
        #Abrimos el archivo en modo lectura con codificación UTF-8
        with open(CONFIG_FILE, "r", encoding="utf-8") as configuracion:
            #json.load() lee el contenido y lo convierte a Python
            config = json.load(configuracion)

def guardar_config():
    #Abrimos el archivo
    with open(CONFIG_FILE, "w", encoding="utf-8") as configuracion:
        #json.dump() convierte el diccionario de Python en texto JSON y lo guarda
        json.dump(config, configuracion, indent=4)  # indent=4 → formato más legible

def ventana_settings():
    #Nueva ventana secundaria
    settings = tk.Toplevel(root)
    settings.title("Settings")
    settings.geometry("400x400")

    #Campos del formulario (con valores actuales)
    nombre_var = tk.StringVar(value = config["nombre_usuario"])
    tema_var = tk.StringVar(value = config["tema_interfaz"])
    idioma_var = tk.StringVar(value = config["idioma"])
    fuente_var = tk.IntVar(value = config["tamaño_fuente"])

    #Campos de texto y etiquetas
    #.pack coloca los elementos uno tras otro
    tk.Label(settings, text = "Nombre de usuario:", font=("Arial", 11, "bold")).grid(row=0, column=0, padx=10, pady=10)
    tk.Entry(settings, textvariable = nombre_var).grid(row=0, column=1, padx=10, pady=10)

    tk.Label(settings, text = "Tema (claro/oscuro):", font=("Arial", 11, "bold")).grid(row=1, column=0, padx=10, pady=10)
    tk.Entry(settings, textvariable = tema_var).grid(row=1, column=1, padx=10, pady=10)

    tk.Label(settings, text = "Idioma (es-ES/en-US):", font=("Arial", 11, "bold")).grid(row=2, column=0, padx=10, pady=10)
    tk.Entry(settings, textvariable = idioma_var).grid(row=2, column=1, padx=10, pady=10)

    tk.Label(settings, text = "Tamaño de fuente:", font=("Arial", 11, "bold")).grid(row=3, column=0, padx=10, pady=10)
    tk.Entry(settings, textvariable = fuente_var).grid(row=3, column=1, padx=10, pady=10)

    #Botones para elegir colores y foto
    def elegir_color_menu():
        #colorchooser.askcolor() es un selector de color
        color = colorchooser.askcolor()[1]  #[] es el color en formato hexadecimal
        if color:
            config["color_menu"] = color  #Guardamos el color en la configuración

    def elegir_color_letra():
        color = colorchooser.askcolor()[1]
        if color:
            config["color_letra"] = color

    def elegir_foto():
        #filedialog.askopenfilename() abre un selector de archivo
        archivo = filedialog.askopenfilename(filetypes=[("Imagenes", "*.png;*.jpg;*.jpeg")])
        if archivo:
            config["foto_perfil"] = archivo

    tk.Button(settings, text = "Color de menú", command = elegir_color_menu).grid(row=4, column=1, padx=10, pady=10)
    tk.Button(settings, text = "Color de letra", command = elegir_color_letra).grid(row=5, column=1, padx=10, pady=10)
    tk.Button(settings, text = "Seleccionar foto de perfil", command = elegir_foto).grid(row=6, column=1, padx=10, pady=10)

    #Guardar cambios y cerrar ventana
    def guardar_y_cerrar():
        #Actualizamos los valores de la configuración con lo que puso el usuario
        config["nombre_usuario"] = nombre_var.get()
        config["tema_interfaz"] = tema_var.get()
        config["idioma"] = idioma_var.get()
        config["tamaño_fuente"] = fuente_var.get()
        #Guardamos el archivo
        guardar_config()
        
        #Hacemos que se note el cambio
        root.configure(bg=config["color_menu"])
        for widget in root.winfo_children():
            #Recorre los widgets (texto) dentro de 'root'
            #Y cambia su fondo y color de texto
            if isinstance(widget, (tk.Label)):
                widget.configure(bg=config["color_menu"], fg=config["color_letra"])

        settings.configure(bg=config["color_menu"])
        for widget in settings.winfo_children():
            if isinstance(widget, (tk.Label)):
                widget.configure(bg=config["color_menu"], fg=config["color_letra"])
                
        #Mensaje de confirmación
        messagebox.showinfo("Configuración", "Configuración guardada.")

        #Cerramos ventana de settings
        settings.destroy()

    tk.Button(settings, text="Guardar", command=guardar_y_cerrar).grid(row=7, column=1, padx=10, pady=10)

## Main ##
root = tk.Tk()
root.title("Aplicación Gestión de Configuración de Usuario")
root.geometry("500x300")

#Cargar configuración al iniciar
cargar_config()

#Presentacion
tk.Label(root, text=f"Bienvenido, {config['nombre_usuario']}", 
         font=("Arial", 16, "bold")).pack(pady=10)

#Crear barra de menú
menubar = tk.Menu(root, bg=config["color_menu"], fg=config["color_letra"])
root.config(menu = menubar)

#Archivo (simulado)
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label = "Abrir")
archivo_menu.add_command(label = "Guardar")
menubar.add_cascade(label = "Archivo", menu = archivo_menu)

#Edición (simulado)
edicion_menu = tk.Menu(menubar, tearoff=0)
edicion_menu.add_command(label = "Copiar")
edicion_menu.add_command(label = "Pegar")
menubar.add_cascade(label="Edición", menu = edicion_menu)

#Ver (simulado)
ver_menu = tk.Menu(menubar, tearoff=0)
ver_menu.add_command(label="Zoom")
menubar.add_cascade(label="Ver", menu = ver_menu)

#Settings
settings_menu = tk.Menu(menubar, tearoff=0)
settings_menu.add_command(label="Ajustes", command = ventana_settings)
menubar.add_cascade(label="Settings", menu = settings_menu)

# Ejecutar la aplicación
root.mainloop()