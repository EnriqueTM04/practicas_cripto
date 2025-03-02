from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, filedialog, Radiobutton, Text
from pathlib import Path
import os
from PIL import Image

#seleccionar archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos BMP", "*.bmp"), ("Archivos TXT", "*.txt")])
    if archivo:
        label_archivo.config(text=archivo)

#ejecutar accion
def ejecutar_accion():
    modo = modo_corrimiento.get()
    bits = entrada_bits.get()
    archivo = label_archivo.cget("text")
    extension = os.path.splitext(archivo)[1]

    if archivo == "Sin seleccionar" or not bits.isdigit():
        error_label = Label(main_frame, text="Selecciona bytes y archivos", font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
        error_label.grid(row=4, column=0, columnspan=2, pady=10)
        error_label.after(2000, error_label.destroy)
    else :
        if(extension == ".bmp"):
            if modo == "corrimiento":
                corrimiento_imagen(archivo, bits)
            else:
                regresar_imagen(archivo, bits)
        else:
            bits = int(bits)
            if bits < 1 or bits >= 26:
                mostrar_error("Número de bits inválido")
                return
            if modo == "corrimiento":
                corrimiento_texto(archivo, bits)
            else:
                regresar_texto(archivo, bits)

def corrimiento_texto(nombre_archivo, bits):
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
            texto_codificado = ""
            for caracter in texto:
                caracter_codificado = chr(ord(caracter) + bits)
                texto_codificado += (caracter_codificado)
            ruta_archivo = Path(nombre_archivo)
            nuevo_archivo = ruta_archivo.stem
            nuevo_archivo += "_c.txt"
            with open(nuevo_archivo, 'w', encoding='utf-8') as archivo_codificado:
                archivo_codificado.write(texto_codificado)
    except:
        mostrar_error("Error al hacer corrimiento")
        return

def regresar_texto(archivo, bits):
    ruta_archivo = Path(archivo)
    nuevo_archivo = ruta_archivo.stem
    nuevo_archivo += "_c"
    try:
        with open((nuevo_archivo + '.txt'), 'r', encoding='utf-8') as archivo:
            texto = archivo.read()
            texto_codificado = ""
            for caracter in texto:
                caracter_codificado = chr(ord(caracter) - bits)
                texto_codificado += caracter_codificado
            nuevo_archivo += "_r.txt"
            with open(nuevo_archivo, 'w', encoding='utf-8') as texto_original:
                texto_original.write(texto_codificado)
    except:
        mostrar_error("Error al hacer corrimiento")
        return

def corrimiento_imagen(archivo, bits):
    try:
        ruta_archivo = Path(archivo)
        nuevo_archivo = ruta_archivo.stem
        imagen = Image.open(archivo)
        imagen_rgb = imagen.convert('RGB')
        pixeles = imagen_rgb.load()
        ancho, alto = imagen.size
        for x in range(ancho):
            for y in range(alto):
                r, g, b = pixeles[x, y]
                print(r, g, b)
                r_corrido = r + bits
                g_corrido = g + bits
                b_corrido = b + bits
                pixeles[x, y] = (r_corrido, g_corrido, b_corrido)
        imagen_rgb.save(nuevo_archivo + '_c.bmp')
    except Exception as e:
        mostrar_error("Error al abrir imagen")
        return

def regresar_imagen(archivo, bits):
    try:
        ruta_archivo = Path(archivo)
        nuevo_archivo = ruta_archivo.stem
        imagen = Image.open(archivo)
        imagen_rgb = imagen.convert('RGB')
        pixeles = imagen_rgb.load()
        ancho, alto = imagen.size
        for x in range(ancho):
            for y in range(alto):
                r, g, b = pixeles[x, y]
                r_corrido = r - bits
                g_corrido = g - bits
                b_corrido = b - bits
                pixeles[x, y] = (r_corrido, g_corrido, b_corrido)
        imagen_rgb.save(nuevo_archivo + '_r.bmp')
    except Exception as e:
        mostrar_error("Error al abrir imagen")
        return

def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=4, column=0, columnspan=2, pady=10)
    error_label.after(2000, error_label.destroy)

root = Tk()
root.title("Práctica 1: Corrimiento de Bits")
root.geometry("800x600")
root.configure(bg="#F0F0F0")

header_frame = Frame(root, bg="#800020", bd=1, relief="solid")
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Práctica 1: Corrimiento de Bits", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#800020")
header_label.pack(pady=5)

# agregando subtitulo con mi nombre decorado
subheader_frame = Frame(root, bg="#700010")
subheader_frame.pack(fill="x")
subheader_label = Label(subheader_frame, text="Equipo:\n\nAbsalón Cortés Sebastian\nFernandez Villar Cuauhtemoc\nTaboada Montiel Enrique", font=("Helvetica", 12, "italic"), fg="#FFFFFF", bg="#700010")
subheader_label.pack(pady=5)


main_frame = Frame(root, bg="#F0F0F0")
main_frame.pack(pady=20)

# Seleccionar archivo
Button(main_frame, text="Ingresar archivo TXT o BMP", command=seleccionar_archivo, font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=10)
label_archivo = Label(main_frame, text="Sin seleccionar", width=40, anchor="w", bg="#FFFFFF", relief="solid", font=("Helvetica", 11))
label_archivo.grid(row=0, column=1, padx=10, pady=20)

# Selección cod/dec
modo_corrimiento = StringVar(value="corrimiento")
Radiobutton(main_frame, text="Corrimiento", variable=modo_corrimiento, value="corrimiento", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
Radiobutton(main_frame, text="Regresar", variable=modo_corrimiento, value="regresar", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Numero corrimiento
Label(main_frame, text="Número de bits para correr:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
entrada_bits = Entry(main_frame, width=10, font=("Helvetica", 11))
entrada_bits.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# Crear archivos
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=3, column=0, columnspan=2, pady=30)

root.mainloop()
