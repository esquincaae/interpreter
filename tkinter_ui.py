import tkinter as tk
from tkinter import messagebox
from main import execute 

def procesar():
    entrada = text_area_entrada.get('1.0', tk.END)
    try:
        script = execute(entrada)
        text_area_resultado.delete('1.0', tk.END)
        text_area_resultado.insert(tk.END, script)
        messagebox.showinfo("Éxito", "Entrada válida.")
    except Exception as e:
        messagebox.showerror("Error de ejecucion", str(e))

root = tk.Tk()
root.title("Lyra: Analizador semantico")

text_area_entrada = tk.Text(root, height=10, width=100)
text_area_entrada.pack(padx=10, pady=10)

boton_procesar = tk.Button(root, text="PROCESAR", command=procesar)
boton_procesar.pack(padx=10, pady=10)

text_area_resultado = tk.Text(root, height=15, width=100)
text_area_resultado.pack(padx=10, pady=10)

root.mainloop()
