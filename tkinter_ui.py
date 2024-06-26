#tkinter_ui.py
import tkinter as tk
from tkinter import messagebox
from main import execute_python, execute_lexico
import sys
from io import StringIO

def procesar():
    entrada = text_area_entrada.get('1.0', tk.END)
    try:
        interpreter = execute_python(entrada)
        codigo_python = interpreter.output

        print("Código Python generado:")
        print(codigo_python)  # Esto te permite ver el código generado.

        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(codigo_python)
        sys.stdout = old_stdout

        text_area_python.delete('1.0', tk.END)
        text_area_python.insert(tk.END, redirected_output.getvalue())
        
        text_area_lexico.delete('1.0', tk.END)
        text_area_lexico.insert(tk.END, execute_lexico(entrada))

        messagebox.showinfo("Éxito", "Script procesado y ejecutado.")
    except Exception as e:
        messagebox.showerror("Error de ejecución", str(e))


root = tk.Tk()
root.title("Lyra: Analizador semantico")
label_entrada = tk.Label(root, text="Entrada en Lyra")
label_entrada.pack()
text_area_entrada = tk.Text(root, height=10, width=100)
text_area_entrada.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

label_lexico = tk.Label(root, text="Salida Lexica")
label_lexico.pack()
text_area_lexico = tk.Text(root, height=10, width=100)
text_area_lexico.pack(padx=10, pady=10)

label_python = tk.Label(root, text="Salida en Python")
label_python.pack()
text_area_python = tk.Text(root, height=10, width=100)
text_area_python.pack(padx=10, pady=10)

root.mainloop()
