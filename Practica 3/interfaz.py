from tkinter import Tk, Label, Button, Entry, Frame, StringVar, Radiobutton
from tkinter import messagebox
import numpy as np

# mostrar solo una o dos matrices dependiendo del modo de operacion
def actualizar_vista():
    borrar_resultado()
    modo = modo_operacion.get()
    if modo == "multiplicacion":
        label_matriz_b.grid()
        for widget in entradas_matriz_b:
            widget.grid()
    else:
        label_matriz_b.grid_remove()
        for widget in entradas_matriz_b:
            widget.grid_remove()


# Función para realizar la operación de matrices
def operacion_martrices():
    borrar_resultado()
    modo = modo_operacion.get()
    if modo == "multiplicacion":
        multiplicacion_martrices()
    else:
        inversa_matriz()

# Función para multiplicar matrices
def multiplicacion_martrices():
    try:
        # Obtener valores de las matrices
        A = np.array([[int(entry_a11.get()), int(entry_a12.get()), int(entry_a13.get())],
                      [int(entry_a21.get()), int(entry_a22.get()), int(entry_a23.get())],
                      [int(entry_a31.get()), int(entry_a32.get()), int(entry_a33.get())]])

        B = np.array([[int(entry_b11.get()), int(entry_b12.get()), int(entry_b13.get())],
                      [int(entry_b21.get()), int(entry_b22.get()), int(entry_b23.get())],
                      [int(entry_b31.get()), int(entry_b32.get()), int(entry_b33.get())]])

        # Realizar la multiplicación de matrices
        resultado = np.dot(A, B)

        modulo = int(entry_modulo.get())

        #Obtener el modulo de cada uno de los valores de la matriz
        resultado = resultado % modulo

        # Mostrar resultado
        resultado_str = "\n".join(["\t".join(map(str, row)) for row in resultado])
        mostrar_resultado(f"Resultado de la multiplicación:\n{resultado_str}")

    except ValueError:
        mostrar_error("Ingresa valores validos en las casillas de las matrices")


# Función para calcular la inversa de una matriz
def inversa_matriz():
    try:
        # Obtener valores de la matriz A
        A = np.array([[int(entry_a11.get()), int(entry_a12.get()), int(entry_a13.get())],
                      [int(entry_a21.get()), int(entry_a22.get()), int(entry_a23.get())],
                      [int(entry_a31.get()), int(entry_a32.get()), int(entry_a33.get())]])

        print("Matriz A original:")
        print(A)

        modulo = int(entry_modulo.get())

        # Calcular la inversa de la matriz A
        det = np.linalg.det(A)

        print(f"El determinante de la matriz es: {det}")
        det_mod = int(det) % modulo

        inv_mult_det = obtener_inveso_multiplicativo(det_mod, modulo)

        if inv_mult_det is None:
            mostrar_error(f"{det_mod} no tiene inverso módulo {modulo}")
            return

        if det == 0:
            mostrar_error("La matriz no tiene inversa")
            return

        print(f"El inverso multiplicativo es: {inv_mult_det}")

        # Calcular adjunta
        adjunta = np.linalg.inv(A) * det
        adjunta = np.round(adjunta).astype(int)
        print(f"La matriz adjunta es:")
        print(adjunta)

        adjunta = adjunta % modulo
        print(f"La matriz adjunta es: {adjunta}")

        A_inv = adjunta * inv_mult_det

        resultado = A_inv % modulo

        # Mostrar resultado
        resultado_str = "\n".join(["\t".join(map(str, row)) for row in resultado])
        mostrar_resultado(f"Resultado de la inversa:\n{resultado_str}")

    except ValueError:
        mostrar_error("Ingresa valores validos en las casillas de la matriz")

# Función para obtener el inverso multiplicativo
def obtener_inveso_multiplicativo(det_mod, modulo):
    t, nuevo_t = 0, 1
    r, nuevo_r = modulo, det_mod
    while nuevo_r != 0:
        cociente = r // nuevo_r
        t, nuevo_t = nuevo_t, t - cociente * nuevo_t
        r, nuevo_r = nuevo_r, r - cociente * nuevo_r
    if r > 1:
        return None
    if t < 0:
        t += modulo
    return t


def mostrar_resultado(mensaje):
    global resultado_label
    resultado_label.config(text=mensaje)

def borrar_resultado():
    global resultado_label
    resultado_label.config(text="")

def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=12, column=0, columnspan=2, pady=10)
    error_label.after(2000, error_label.destroy)

root = Tk()
root.title("Practica 3: Calculadora de Matrices 3x3 (Modular)")
root.geometry("1200x800")
root.configure(bg="#F0F0F0")

header_frame = Frame(root, bg="#800020", bd=1, relief="solid")
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Practica 3: Calculadora de Matrices 3x3 (Modular)", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#800020")
header_label.pack(pady=5)

# agregando subtitulo con mi nombre decorado
subheader_frame = Frame(root, bg="#700010")
subheader_frame.pack(fill="x")
subheader_label = Label(subheader_frame, text="Equipo:\n\nAbsalón Cortés Sebastian\nFernandez Villar Cuauhtemoc\nTaboada Montiel Enrique", font=("Helvetica", 12, "italic"), fg="#FFFFFF", bg="#700010")
subheader_label.pack(pady=5)

main_frame = Frame(root, bg="#F0F0F0")
main_frame.pack(pady=20)

# opciones de la metodo
# Selección cod/dec
modo_operacion = StringVar(value="multiplicacion")
Radiobutton(main_frame, text="Multiplicacion", variable=modo_operacion, value="multiplicacion", bg="#F0F0F0", font=("Helvetica", 11), command=actualizar_vista).grid(row=1, column=0, padx=10, pady=5, sticky="w")
Radiobutton(main_frame, text="Inversa", variable=modo_operacion, value="inversa", bg="#F0F0F0", font=("Helvetica", 11), command=actualizar_vista).grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Entradas para la primera matriz A
Label(main_frame, text="Matriz A:", bg="#F0F0F0", font=("Helvetica", 11, "bold")).grid(row=0, column=0, columnspan=3, pady=10)

entry_a11 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a11.grid(row=2, column=0, padx=5, pady=5)

entry_a12 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a12.grid(row=2, column=1, padx=5, pady=5)

entry_a13 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a13.grid(row=2, column=2, padx=5, pady=5)

entry_a21 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a21.grid(row=3, column=0, padx=5, pady=5)

entry_a22 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a22.grid(row=3, column=1, padx=5, pady=5)

entry_a23 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a23.grid(row=3, column=2, padx=5, pady=5)

entry_a31 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a31.grid(row=4, column=0, padx=5, pady=5)

entry_a32 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a32.grid(row=4, column=1, padx=5, pady=5)

entry_a33 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_a33.grid(row=4, column=2, padx=5, pady=5)

# Entradas para la segunda matriz B
label_matriz_b = Label(main_frame, text="Matriz B:", bg="#F0F0F0", font=("Helvetica", 11, "bold"))
label_matriz_b.grid(row=5, column=0, columnspan=3, pady=10)

entry_b11 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b11.grid(row=6, column=0, padx=5, pady=5)

entry_b12 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b12.grid(row=6, column=1, padx=5, pady=5)

entry_b13 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b13.grid(row=6, column=2, padx=5, pady=5)

entry_b21 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b21.grid(row=7, column=0, padx=5, pady=5)

entry_b22 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b22.grid(row=7, column=1, padx=5, pady=5)

entry_b23 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b23.grid(row=7, column=2, padx=5, pady=5)

entry_b31 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b31.grid(row=8, column=0, padx=5, pady=5)

entry_b32 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b32.grid(row=8, column=1, padx=5, pady=5)

entry_b33 = Entry(main_frame, width=5, font=("Helvetica", 12))
entry_b33.grid(row=8, column=2, padx=5, pady=5)

# Agrupar todas las entradas de la matriz B
entradas_matriz_b = [
    entry_b11, entry_b12, entry_b13,
    entry_b21, entry_b22, entry_b23,
    entry_b31, entry_b32, entry_b33
]

# Elegir el modulo para la matriz resultante
Label(main_frame, text="Mod __ :", bg="#F0F0F0", font=("Helvetica", 11, "bold")).grid(row=9, column=0, columnspan=3, pady=10)
entry_modulo = Entry(main_frame, width=10, font=("Helvetica", 12))
entry_modulo.grid(row=10, column=0, columnspan=5, pady=10)

# Botón para ejecutar la multiplicación
Button(main_frame, text="Operacion", command=operacion_martrices, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=15, height=2).grid(row=11, column=0, columnspan=3, pady=30)

# Etiqueta para mostrar el resultado
resultado_label = Label(main_frame, text="", font=("Helvetica", 12), fg="#00913F", bg="#F0F0F0")
resultado_label.grid(row=12, column=0, columnspan=3)

actualizar_vista()

root.mainloop()
