from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, filedialog, Radiobutton, Text
from pathlib import Path
import os
from PIL import Image

#ejecutar accion
def ejecutar_accion():
    a = int(valor_a.get())
    b = int(valor_b.get())
    n = int(valor_n.get())
    borrar_resultado()
    if not a or not b or not n:
        mostrar_error("Favor de llenar todos los campos")
        return
    if b >= n:
        mostrar_error("Elige un valor de β menor a n")
        return
    # calcular mcd para a y n
    resultado = euclides(a, n)
    if resultado != 1:
        mostrar_error("El MCD de α y n debe ser 1")
        return
    # para C
    mensaje = "***** Funcion de Cifrado ******\n"
    mensaje += f"C = {a}p + {b} mod {n}\n\n"
    # para p
    mensaje += "***** Funcion de Descifrado ******\n"
    mensaje += f"p = {a}^-1 * (C + (- {b}) mod {n}\n"
    # calcular inverso mult de a
    inverso_a = 0
    for i in range(1, int(n)):
        r = ((n * i) + 1) / a
        if r%1 == 0:
            inverso_a = int(r)
            break

    # encontrar valroes restantes
    inverso_b = -b % n
    ba = int(inverso_a) * inverso_b
    ba_mod = ba % n
    mensaje += f"p = {inverso_a}C + {ba_mod} mod {n}"

    mostrar_resultado(mensaje)

def euclides(a, b):
    while b != 0:  # Mientras el residuo no sea 0
        a, b = b, a % b  # Se asigna b a a, y el residuo a b
    return a  # Cuando b es 0, a es el MCD


def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=6, column=0, columnspan=2, pady=10)
    error_label.after(2000, error_label.destroy)

def mostrar_resultado(mensaje):
    global resultado_label
    resultado_label = Label(main_frame, text=mensaje, font=("Helvetica", 14), fg="#00913F", bg="#F0F0F0")
    resultado_label.grid(row=6, column=0, columnspan=2, pady=10)

def borrar_resultado() :
    global resultado_label
    if resultado_label:
        resultado_label.destroy()

root = Tk()
root.title("Práctica 2: Afin")
root.geometry("900x700")
root.configure(bg="#F0F0F0")

header_frame = Frame(root, bg="#800020", bd=1, relief="solid")
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Práctica 2: Afin", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#800020")
header_label.pack(pady=5)

# agregando subtitulo con mi nombre decorado
subheader_frame = Frame(root, bg="#700010")
subheader_frame.pack(fill="x")
subheader_label = Label(subheader_frame, text="Equipo:\n\nAbsalón Cortés Sebastian\nFernandez Villar Cuauhtemoc\nTaboada Montiel Enrique", font=("Helvetica", 12, "italic"), fg="#FFFFFF", bg="#700010")
subheader_label.pack(pady=5)


main_frame = Frame(root, bg="#F0F0F0")
main_frame.pack(pady=20)

# Numero alfa
Label(main_frame, text="Valor de α:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
valor_a = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_a.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# Numero Beta
Label(main_frame, text="Valor de β:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
valor_b = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_b.grid(row=3, column=1, padx=10, pady=20, sticky="w")

# Numero n
Label(main_frame, text="Valor de n:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
valor_n = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_n.grid(row=4, column=1, padx=10, pady=20, sticky="w")

resultado_label = Label(main_frame, text=f"", font=("Helvetica", 14), fg="#FF0000", bg="#F0F0F0")

# Mostrar resultado
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=5, column=0, columnspan=2, pady=30)

root.mainloop()
