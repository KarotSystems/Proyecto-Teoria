import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import re
import os

#Configuracion de la ventana
root = tk.Tk()
root.title("Analizador Léxico, Sintáctico y Semántico")
root.geometry("950x600")

# Palabras reservadas y operadores
palabras_reservadas = ["entero", "decimal", "booleano", "cadena", 
                       "si", "sino", "mientras", "hacer", "funcion",
                       "verdadero", "falso", "retornar"]

operadores = ["+", "-", "*", "/", "%", "=", "==", "!=", "<", ">", "<=", ">="]
signos = ["(", ")", "{", "}", ";", ","]

#Funcion: Clasificar cada token
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
    elif re.fullmatch(r'"[^"]*"', token):
        return "Cadena"
    else:
        return "Error Léxico"

#Funcion: Analiza el codigo/texto ingresado
def analizar_contenido(texto):
    # Limpiar tablas
    for tabla in [tabla_texto, tabla_tokens, tabla_errores, tabla_sintactico]:
        for item in tabla.get_children():
            tabla.delete(item)

    lineas = texto.split("\n")
    errores_lexicos = []
    tokens_globales = []
    variables_declaradas = set()
    errores_sintacticos = []

    #Analisis lexico
    for i, linea in enumerate(lineas, start=1):
        if not linea.strip():
            continue
        tabla_texto.insert("", tk.END, values=(i, linea.strip()))

        # Detectar TODO (tokens válidos + inválidos)
        tokens = re.findall(r'[a-zA-Z_]\w*|\d+(?:\.\d+)?|==|!=|<=|>=|[+\-*/%=<>(){},;"$@#]', linea)

        for token in tokens:
            tipo = clasificar_token(token)
            if tipo == "Error Léxico":
                errores_lexicos.append((i, token))
                tabla_errores.insert("", tk.END, values=(i, token, "Error Léxico"))
            else:
                tokens_globales.append((i, token, tipo))
                tabla_tokens.insert("", tk.END, values=(i, token, tipo))

    #Análisis Sintáctico y Semántico
    for i, linea in enumerate(lineas, start=1):
        codigo = linea.strip()
        if not codigo:
            continue

        # Reglas básicas de validación
        if re.match(r"^(entero|decimal|booleano|cadena)\s+[a-zA-Z_]\w*\s*(=\s*[\w\d\+\-\*/]+)?;$", codigo):
            nombre = re.findall(r"[a-zA-Z_]\w*", codigo)[1]
            variables_declaradas.add(nombre)
            resultado = "Declaración de variable válida"
        elif re.match(r"^si\s*\(.*\)\s*\{", codigo):
            resultado = "Estructura condicional (si) detectada"
        elif re.match(r"^sino\s*\{", codigo):
            resultado = "Bloque 'sino' detectado"
        elif re.match(r"^mientras\s*\(.*\)\s*\{", codigo):
            resultado = "Bucle 'mientras' detectado"
        elif re.match(r"^(entero|decimal|booleano|cadena)\s+[a-zA-Z_]\w*\s*\(.*\)\s*\{", codigo):
            resultado = "Declaración de función detectada"
        elif re.match(r"^[a-zA-Z_]\w*\s*=\s*.*;$", codigo):
            nombre = codigo.split("=")[0].strip()
            if nombre not in variables_declaradas:
                errores_sintacticos.append((i, codigo, "Variable no declarada antes de su uso"))
                continue
            resultado = "Asignación válida"
        else:
            errores_sintacticos.append((i, codigo, "Estructura no reconocida"))
            continue

        tabla_sintactico.insert("", tk.END, values=(i, codigo, resultado))

    for linea, codigo, error in errores_sintacticos:
        tabla_sintactico.insert("", tk.END, values=(linea, codigo, f"❌ {error}"))

    messagebox.showinfo("Análisis completado", "El análisis ha finalizado correctamente.")

#Funcion: Analizar texto desde el editor
def analizar_editor():
    texto = text_editor.get("1.0", tk.END).strip()
    if not texto:
        messagebox.showwarning("Vacío", "Escribe o pega el código que deseas analizar.")
        return
    analizar_contenido(texto)

#Funcion: Abrir archivo externo
def abrir_archivo():
    ruta = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if not ruta:
        return
    with open(ruta, "r", encoding="utf-8") as archivo:
        contenido = archivo.read()
    text_editor.delete("1.0", tk.END)
    text_editor.insert(tk.END, contenido)
    messagebox.showinfo("Archivo cargado", f"Archivo '{os.path.basename(ruta)}' cargado en el editor.")

#Funcion: Guardar resultados
def guardar_resultado():
    archivo = filedialog.asksaveasfilename(defaultextension=".txt")
    if archivo:
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("=== TOKENS DETECTADOS ===\n")
            for item in tabla_tokens.get_children():
                linea, token, tipo = tabla_tokens.item(item, "values")
                f.write(f"Línea {linea}: {token} ({tipo})\n")

            f.write("\n=== ERRORES LÉXICOS ===\n")
            for item in tabla_errores.get_children():
                linea, token, tipo = tabla_errores.item(item, "values")
                f.write(f"Línea {linea}: {token} ({tipo})\n")

            f.write("\n=== RESULTADOS SINTÁCTICOS Y SEMÁNTICOS ===\n")
            for item in tabla_sintactico.get_children():
                linea, texto, estado = tabla_sintactico.item(item, "values")
                f.write(f"Línea {linea}: {texto} -> {estado}\n")

        messagebox.showinfo("Guardado", "Archivo guardado correctamente.")

# INTERFAZ GRÁFICA
tk.Label(root, text="ANALIZADOR DE LENGUAJE - PROYECTO 2", 
         font=("Arial", 16, "bold")).pack(pady=10)

# Menú superior
menu = tk.Menu(root)
root.config(menu=menu)
archivo_menu = tk.Menu(menu, tearoff=0)
archivo_menu.add_command(label="Abrir código", command=abrir_archivo)
archivo_menu.add_command(label="Guardar resultados", command=guardar_resultado)
archivo_menu.add_separator()
archivo_menu.add_command(label="Salir", command=root.quit)
menu.add_cascade(label="Archivo", menu=archivo_menu)

#Cuaderno con pestañas
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=10, pady=10)

#Pestaña 1: Editor de Código
frame_editor = ttk.Frame(notebook)
notebook.add(frame_editor, text="Editor de Código")

tk.Label(frame_editor, text="Escribe o pega el código fuente:", font=("Arial", 12, "bold")).pack(pady=5)
text_editor = tk.Text(frame_editor, wrap="word", height=20, width=100, font=("Consolas", 11))
text_editor.pack(expand=True, fill="both", padx=10, pady=10)

ttk.Button(frame_editor, text="Analizar Código", command=analizar_editor).pack(pady=5)

#Pestaña 2: Texto original
frame_texto = ttk.Frame(notebook)
notebook.add(frame_texto, text="Texto Original")
tabla_texto = ttk.Treeview(frame_texto, columns=("Línea", "Código"), show="headings", height=15)
tabla_texto.heading("Línea", text="Línea")
tabla_texto.heading("Código", text="Código")
tabla_texto.pack(expand=True, fill="both")

#Pestaña 3: Tokens
frame_tokens = ttk.Frame(notebook)
notebook.add(frame_tokens, text="Tokens")
tabla_tokens = ttk.Treeview(frame_tokens, columns=("Línea", "Token", "Tipo"), show="headings", height=15)
for col in ("Línea", "Token", "Tipo"):
    tabla_tokens.heading(col, text=col)
tabla_tokens.pack(expand=True, fill="both")

#Pestaña 4: Errores léxicos
frame_errores = ttk.Frame(notebook)
notebook.add(frame_errores, text="Errores Léxicos")
tabla_errores = ttk.Treeview(frame_errores, columns=("Línea", "Token", "Descripción"), show="headings", height=15)
for col in ("Línea", "Token", "Descripción"):
    tabla_errores.heading(col, text=col)
tabla_errores.pack(expand=True, fill="both")

#Pestaña 5: Análisis Sintáctico y Semántico
frame_analizar = ttk.Frame(notebook)
notebook.add(frame_analizar, text="Análisis Sintáctico/Semántico")
tabla_sintactico = ttk.Treeview(frame_analizar, columns=("Línea", "Código", "Resultado"), show="headings", height=15)
for col in ("Línea", "Código", "Resultado"):
    tabla_sintactico.heading(col, text=col)
tabla_sintactico.pack(expand=True, fill="both")

root.mainloop()
