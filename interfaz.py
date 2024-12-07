import tkinter as tk
from tkinter import scrolledtext
from lexico import lexer
from sintactico import Parser, ast_to_string

ventana = tk.Tk()

anchoVentana = 1400
altoVentana = 750

anchoPantalla = ventana.winfo_screenwidth()
altoPantalla = ventana.winfo_screenheight()

posX = (anchoPantalla - anchoVentana) // 2
posY = (altoPantalla - altoVentana) // 2

ventana.geometry(f"{anchoVentana}x{altoVentana}+{posX}+{posY}")
ventana.title("Compilador Final")

labelCodigo = tk.Label(ventana, text="Introducir código")
labelCodigo.place(x=20, y=20)

entradaText = scrolledtext.ScrolledText(ventana, width=40, height=10)
entradaText.place(x=20, y=50)

def obtenerCodigo():
    codigo = entradaText.get("1.0", tk.END).strip()
    print(f"Código ingresado: {codigo}")

    # Aquí llamamos el analizador léxico para procesar el código introducido.
    tokens = lexer(codigo)
    print('Tokens:', tokens)

    # Mostrar los tokens en el campo de salida léxico.
    salidaLexico.delete('1.0', tk.END)
    for token in tokens:
        salidaLexico.insert(tk.END, f"{token}\n")

    # Aquí llamamos el analizador sintáctico para procesar los tokens.
    try:
        parser = Parser(tokens)
        ast = parser.parse()
        ast_str = ast_to_string(ast)
        print('AST:', ast_str)

        # Mostrar el AST en el campo de salida sintáctico.
        salidaSintactico.delete('1.0', tk.END)
        salidaSintactico.insert(tk.END, ast_str)
    except Exception as e:
        print(f"Error en el análisis sintáctico: {e}")
        salidaSintactico.delete('1.0', tk.END)
        salidaSintactico.insert(tk.END, f"Error en el análisis sintáctico: {e}")

capturar = tk.Button(ventana, text="Analizar", command=obtenerCodigo)
capturar.place(x=150, y=16)

resultadoLexico = tk.Label(ventana, text="Analizador Léxico")
resultadoLexico.place(x=20, y=350)

salidaLexico = scrolledtext.ScrolledText(ventana, width=30, height=20)
salidaLexico.place(x=20, y=370)

resultadoSintactico = tk.Label(ventana, text="Analizador Sintáctico")
resultadoSintactico.place(x=300, y=16)

# Crear un campo de texto con scroll para mostrar los resultados sintácticos.
salidaSintactico = scrolledtext.ScrolledText(ventana, width=50, height=30)
salidaSintactico.place(x=300, y=370)

ventana.mainloop()
