from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, filedialog, Radiobutton, Text
from pathlib import Path
import os
from PIL import Image

#ejecutar accion
def ejecutar_accion():
    a = valor_a.get()
    b = valor_b.get()
    resultado = euclides(int(a), int(b))
    mostrar_resultado(resultado)

def euclides(a, b):
    while b != 0:  # Mientras el residuo no sea 0
        a, b = b, a % b  # Se asigna b a a, y el residuo a b
    return a  # Cuando b es 0, a es el MCD


def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=5, column=0, columnspan=2, pady=10)
    error_label.after(2000, error_label.destroy)

def mostrar_resultado(valor):
    resultado_label = Label(main_frame, text=f"El MCD es: {valor}", font=("Helvetica", 14), fg="#FF0000", bg="#F0F0F0")
    resultado_label.grid(row=5, column=0, columnspan=2, pady=10)

root = Tk()
root.title("Práctica 1: Corrimiento de Bits")
root.geometry("800x600")
root.configure(bg="#F0F0F0")

header_frame = Frame(root, bg="#800020", bd=1, relief="solid")
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Práctica 1: Maximo comun Diviosor (Euclides)", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#800020")
header_label.pack(pady=5)

# agregando subtitulo con mi nombre decorado
subheader_frame = Frame(root, bg="#700010")
subheader_frame.pack(fill="x")
subheader_label = Label(subheader_frame, text="Equipo:\n\nAbsalón Cortés Sebastian\nFernandez Villar Cuauhtemoc\nTaboada Montiel Enrique", font=("Helvetica", 12, "italic"), fg="#FFFFFF", bg="#700010")
subheader_label.pack(pady=5)


main_frame = Frame(root, bg="#F0F0F0")
main_frame.pack(pady=20)

# Numero corrimiento
Label(main_frame, text="Valor de A:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
valor_a = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_a.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# Numero corrimiento
Label(main_frame, text="Valor de B:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
valor_b = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_b.grid(row=3, column=1, padx=10, pady=20, sticky="w")

# Crear archivos
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=4, column=0, columnspan=2, pady=30)

root.mainloop()
