from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, filedialog, Radiobutton, Text
from pathlib import Path
import os
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

#seleccionar archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos BMP", "*.bmp"), ("Archivos TXT", "*.txt")])
    if archivo:
        label_archivo.config(text=archivo)

#ejecutar accion
def ejecutar_accion():
    modo = modo_corrimiento.get()
    key = valor_llave.get()
    archivo = label_archivo.cget("text")
    extension = os.path.splitext(archivo)[1]

    if archivo == "Sin seleccionar" or not key:
        mostrar_error("Selecciona un archivo y proporciona una clave")
        return

    # Si es imagen, mantenemos el corrimiento de bits
    if extension == ".bmp":
        try:
            bits = int(key)
            if bits < 1 or bits >= 256:
                mostrar_error("Número de bits inválido (1-255)")
                return
            if modo == "corrimiento":
                corrimiento_imagen(archivo, bits)
            else:
                regresar_imagen(archivo, bits)
        except:
            mostrar_error("Valor de bits inválido (debe ser numérico)")
            return
    # Si es texto, usamos AES
    elif extension == ".txt":
        if len(key.encode('utf-8')) not in [16, 24, 32]:
            mostrar_error("Clave AES debe tener 16, 24 o 32 caracteres")
            return
        if modo == "corrimiento":
            corrimiento_texto(archivo, key)
        else:
            regresar_texto(archivo, key)
    else:
        mostrar_error("Archivo no soportado")



def corrimiento_texto(nombre_archivo, bits):
    try:
        key = valor_llave.get().encode('utf-8')
        if len(key) not in [16, 24, 32]:
            mostrar_error("La clave debe tener 16, 24 o 32 caracteres")
            return

        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            texto = archivo.read().encode('utf-8')

        cipher = AES.new(key, AES.MODE_CBC)
        ciphertext = cipher.encrypt(pad(texto, AES.block_size))

        ruta_archivo = Path(nombre_archivo)
        nuevo_archivo = ruta_archivo.stem + "_c.txt"

        with open(nuevo_archivo, 'wb') as archivo_codificado:
            archivo_codificado.write(cipher.iv + ciphertext)  # Guardamos IV + datos cifrados
    except Exception as e:
        mostrar_error("Error al cifrar texto")
        print(e)


def regresar_texto(nombre_archivo, bits):
    try:
        key = valor_llave.get().encode('utf-8')
        if len(key) not in [16, 24, 32]:
            mostrar_error("La clave debe tener 16, 24 o 32 caracteres")
            return

        with open(nombre_archivo.replace(".txt", "_c.txt"), 'rb') as archivo:
            data = archivo.read()
            iv = data[:16]
            ciphertext = data[16:]

        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

        nuevo_archivo = Path(nombre_archivo).stem + "_r.txt"
        with open(nuevo_archivo, 'w', encoding='utf-8') as texto_original:
            texto_original.write(plaintext.decode('utf-8'))
    except Exception as e:
        mostrar_error("Error al descifrar texto")
        print(e)


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
                r_corrido = (r + bits) % 256
                g_corrido = (g + bits) % 256
                b_corrido = (b + bits) % 256
                pixeles[x, y] = (r_corrido, g_corrido, b_corrido)
        imagen_rgb.save(nuevo_archivo + '_c.bmp')
    except Exception as e:
        mostrar_error("Error al abrir imagen")
        return

def regresar_imagen(archivo, bits):
    try:
        ruta_archivo = Path(archivo)
        nuevo_archivo = ruta_archivo.stem
        nuevo_archivo += "_c"
        imagen = Image.open(nuevo_archivo+'.bmp')
        imagen_rgb = imagen.convert('RGB')
        pixeles = imagen_rgb.load()
        ancho, alto = imagen.size
        for x in range(ancho):
            for y in range(alto):
                r, g, b = pixeles[x, y]
                r_corrido = (r - bits) % 256
                g_corrido = (g - bits) % 256
                b_corrido = (b - bits) % 256
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

# Numero Llave
Label(main_frame, text="Valor de la llave:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
valor_llave = Entry(main_frame, width=10, font=("Helvetica", 11))
valor_llave.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# Crear archivos
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=3, column=0, columnspan=2, pady=30)

root.mainloop()
