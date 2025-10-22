import tkinter as tk  
from tkinter import filedialog, colorchooser, messagebox, ttk
import json  
import os
import re

CONFIG_FILE = "config.json"

config = {
    "nombre_usuario": "Usuario",
    "tema_interfaz": "claro",
    "idioma": "es-ES",
    "tamaño_fuente": 12,
    "color_menu": "#ffffff",
    "color_letra": "#000000",
    "foto_perfil": ""
}

# Palabras reservadas
palabras_reservadas = [
    "entero", "decimal", "booleano", "cadena",
    "si", "sino", "mientras", "hacer",
    "verdadero", "falso"
]

# Operadores válidos
operadores = [
    "+", "-", "*", "/", "%", "=", "==",
    "<", ">", ">=", "<="
]

# Signos válidos
signos = ["(", ")", "{", "}", "“", ";"]

def cargar_config():
    global config
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as configuracion:
            config = json.load(configuracion)

# Clasificar token
def clasificar_token(token):
    if token in palabras_reservadas:
        return "Palabra Reservada"
    elif token in operadores:
        return "Operador"
    elif token in signos:
        return "Signo"
    elif re.fullmatch(r"\d+(\.\d+)?", token):
        return "Número"
    elif re.fullmatch(r"[a-zA-Z_]\w*", token):
        return "Identificador"
    else:
        return "Error Léxico"

def abrir_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not ruta:
        return

    with open(ruta, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    # Limpiar tablas
    for tabla in [tabla_texto, tabla_tokens, tabla_errores]:
        for item in tabla.get_children():
            tabla.delete(item)

    resumen = {}
    errores = []

    for i, linea in enumerate(lineas, start=1):
        # Tabla 1: mostrar el texto original
        tabla_texto.insert("", tk.END, values=(i, linea.strip()))

        tokens = re.findall(r"[a-zA-Z_]\w*|\d+(?:\.\d+)?|==|>=|<=|[+\-*/%=<>(){};]", linea)
        for token in tokens:
            tipo = clasificar_token(token)
            if tipo == "Error Léxico":
                errores.append((i, token))
            else:
                # Tabla 2: mostrar tokens válidos
                tabla_tokens.insert("", tk.END, values=(i, token, tipo))

    # Tabla 3: mostrar errores
    for linea, token in errores:
        tabla_errores.insert("", tk.END, values=(linea, token, "Error Léxico"))

def guardar_archivo():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt")
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("=== TOKENS VÁLIDOS ===\n")
            for item in tabla_tokens.get_children():
                linea, token, tipo = tabla_tokens.item(item, "values")
                f.write(f"Línea {linea}: {token} ({tipo})\n")

            f.write("\n=== ERRORES ===\n")
            for item in tabla_errores.get_children():
                linea, token, tipo = tabla_errores.item(item, "values")
                f.write(f"Línea {linea}: {token} ({tipo})\n")

        messagebox.showinfo("Guardado", "Archivo guardado correctamente.")

## Main ##
root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("900x600")

cargar_config()

tk.Label(root, text="Bienvenido, Analizador Léxico", font=("Arial", 16, "bold")).pack(pady=10)

#Crear barra de menú
menubar = tk.Menu(root)  
root.config(menu=menubar)  

#Archivo
archivo_menu = tk.Menu(menubar, tearoff=0)
archivo_menu.add_command(label = "Abrir", command = abrir_archivo)
archivo_menu.add_command(label = "Guardar", command = guardar_archivo)
menubar.add_cascade(label = "Archivo", menu = archivo_menu)

# Área de texto para mostrar resultados
# Tablas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# Tabla 1: Texto original
frame1 = ttk.Frame(notebook)
notebook.add(frame1, text="Texto Original")
tabla_texto = ttk.Treeview(frame1, columns=("Línea", "Texto"), show="headings", height=15)
tabla_texto.heading("Línea", text="Línea")
tabla_texto.heading("Texto", text="Texto")
tabla_texto.column("Línea", width=60, anchor="center")
tabla_texto.column("Texto", width=700, anchor="w")
tabla_texto.pack(expand=True, fill="both")

# Tabla 2: Tokens válidos
frame2 = ttk.Frame(notebook)
notebook.add(frame2, text="Tokens")
tabla_tokens = ttk.Treeview(frame2, columns=("Línea", "Token", "Tipo"), show="headings", height=15)
tabla_tokens.heading("Línea", text="Línea")
tabla_tokens.heading("Token", text="Token")
tabla_tokens.heading("Tipo", text="Tipo")
tabla_tokens.column("Línea", width=60, anchor="center")
tabla_tokens.column("Token", width=150, anchor="center")
tabla_tokens.column("Tipo", width=200, anchor="center")
tabla_tokens.pack(expand=True, fill="both")

# Tabla 3: Errores
frame3 = ttk.Frame(notebook)
notebook.add(frame3, text="Errores")
tabla_errores = ttk.Treeview(frame3, columns=("Línea", "Token", "Descripción"), show="headings", height=15)
tabla_errores.heading("Línea", text="Línea")
tabla_errores.heading("Token", text="Token")
tabla_errores.heading("Descripción", text="Descripción")
tabla_errores.column("Línea", width=60, anchor="center")
tabla_errores.column("Token", width=150, anchor="center")
tabla_errores.column("Descripción", width=300, anchor="w")
tabla_errores.pack(expand=True, fill="both")

root.mainloop()