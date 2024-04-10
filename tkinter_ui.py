import tkinter as tk
from tkinter import messagebox
from main import execute_python#, execute_lexico
import sys
from io import StringIO

def procesar():
    entrada = text_area_entrada.get('1.0', tk.END)
    try:
        interpreter = execute_python(entrada)
        codigo_python = interpreter.output

        # Redireccionar stdout para capturar la salida
        old_stdout = sys.stdout
        redirected_output = sys.stdout = StringIO()
        exec(codigo_python)  # Ejecutar el código Python generado
        sys.stdout = old_stdout  # Restaurar stdout

        text_area_python.delete('1.0', tk.END)
        text_area_python.insert(tk.END, redirected_output.getvalue())
        
        #text_area_lexico.delete('1.0', tk.END)
        #text_area_lexico.insert(tk.END, execute_lexico(entrada))

        #text_area_sintactico.delete('1.0', tk.END)
        #text_area_sintactico.insert()

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

label_python = tk.Label(root, text="Salida en Python")
label_python.pack()
text_area_python = tk.Text(root, height=10, width=100)
text_area_python.pack(padx=10, pady=10)

#label_lexico = tk.Label(root, text="Salida Lexica")
#label_lexico.pack()
#text_area_lexico = tk.Text(root, height=5, width=50)
#text_area_lexico.pack(padx=10, pady=10)

#label_sintactico = tk.Label(root, text="Salida Sintactica")
#label_sintactico.pack()
#text_area_sintactico = tk.Text(root, height=5, width=50)
#text_area_sintactico.pack(padx=10, pady=10)

root.mainloop()
