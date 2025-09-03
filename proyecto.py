import tkinter as tk  
from tkinter import filedialog, colorchooser, messagebox  
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

    salida.delete("1.0", tk.END)
    resumen = {}
    errores = []

    for i, linea in enumerate(lineas, start=1):
        tokens = re.findall(r"[a-zA-Z_]\w*|\d+(\.\d+)?|==|>=|<=|[+\-*/%=<>(){};]", linea)
        for token in tokens:
            tipo = clasificar_token(token)
            if tipo == "Error Léxico":
                errores.append(f"Línea {i}: Token inválido '{token}'")
            else:
                resumen[tipo] = resumen.get(tipo, {})
                resumen[tipo][token] = resumen[tipo].get(token, 0) + 1

    if errores:
        salida.insert(tk.END, "Errores léxicos encontrados:\n")
        for err in errores:
            salida.insert(tk.END, err + "\n")
    else:
        salida.insert(tk.END, "Tokens válidos encontrados:\n")
        for tipo, tokens in resumen.items():
            for token, cantidad in tokens.items():
                salida.insert(tk.END, f"{token:<10} {tipo:<20} {cantidad}\n")

def guardar_archivo():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt")
    if archivo:
        contenido = salida.get("1.0", tk.END)
        with open(archivo, "w", encoding="utf-8") as f:
            f.write(contenido)
        messagebox.showinfo("Guardado", "Archivo guardado correctamente.")

## Main ##
root = tk.Tk()
root.title("Analizador Léxico")
root.geometry("600x400")

cargar_config()

tk.Label(root, text="Bienvenido, Analizador Léxico", font=("Arial", 16, "bold")).pack(pady=10)

# Botones
abrir = tk.Button(root, text="Abrir", command = abrir_archivo).pack(pady=10)
guardar = tk.Button(root, text="Guardar", command = guardar_archivo).pack(pady=10)

# Área de texto para mostrar resultados
salida = tk.Text(root, wrap="word", font=("Arial", config["tamaño_fuente"]))
salida.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()