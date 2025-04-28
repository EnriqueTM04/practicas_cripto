from tkinter import Tk, Label, Button, Entry, StringVar, IntVar, Frame, filedialog, Radiobutton, Text
from pathlib import Path
import os
from PIL import Image
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

#seleccionar archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos BMP", "*.bmp")])
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

    if extension == ".bmp":
        if len(key.encode('utf-8')) not in [16, 24, 32]:
            mostrar_error("Clave AES debe tener 16, 24 o 32 caracteres")
            return
        if modo == "corrimiento":
            cifrar_imagen(archivo, key)
        else:
            descifrar_imagen(archivo, key)
    else:
        mostrar_error("Archivo no soportado")

def cifrar_imagen(ruta_imagen, clave):
    try:
        # Leer todo el archivo BMP
        with open(ruta_imagen, 'rb') as archivo:
            datos = archivo.read()

        # Obtener el offset donde comienzan los datos de píxeles (bytes 10 a 14)
        pixel_offset = int.from_bytes(datos[10:14], byteorder='little')
        encabezado = datos[:pixel_offset]
        pixeles = datos[pixel_offset:]

        # Crear cifrador AES y obtener IV
        clave_bytes = clave.encode('utf-8')
        cipher = AES.new(clave_bytes, AES.MODE_CBC)
        iv = cipher.iv

        # Cifrar los datos de píxeles con padding
        pixeles_cifrados = cipher.encrypt(pad(pixeles, AES.block_size))

        # Guardar la imagen cifrada: encabezado, IV y datos cifrados
        nuevo_archivo = Path(ruta_imagen).stem + "_c.bmp"
        with open(nuevo_archivo, 'wb') as archivo_cifrado:
            archivo_cifrado.write(encabezado + iv + pixeles_cifrados)

        print(f"Imagen cifrada guardada como: {nuevo_archivo}")
        return nuevo_archivo

    except Exception as e:
        print(f"Error al cifrar la imagen: {e}")


def descifrar_imagen(nombre_imagen, clave):
    try:
        # Leer todo el archivo cifrado BMP
        with open(nombre_imagen.replace(".bmp", "_c.bmp"), 'rb') as archivo:
            datos = archivo.read()

        # Extraer el offset de los datos de píxeles (se mantiene igual que en el cifrado)
        pixel_offset = int.from_bytes(datos[10:14], byteorder='little')
        # El encabezado es hasta el offset
        encabezado = datos[:pixel_offset]
        # Leer el IV que se guardó a continuación del encabezado (16 bytes)
        iv = datos[pixel_offset:pixel_offset+16]
        # El resto son los datos cifrados
        pixeles_cifrados = datos[pixel_offset+16:]

        # Crear descifrador AES usando la misma clave y IV
        clave_bytes = clave.encode('utf-8')
        cipher = AES.new(clave_bytes, AES.MODE_CBC, iv)

        # Descifrar y quitar el padding
        pixeles_descifrados = unpad(cipher.decrypt(pixeles_cifrados), AES.block_size)

        # Guardar la imagen descifrada. Si el nombre original terminaba en "_cifrada", lo cambiamos.
        nuevo_archivo = nombre_imagen.replace(".bmp", "_c_d.bmp")
        with open(nuevo_archivo, 'wb') as archivo_descifrado:
            archivo_descifrado.write(encabezado + pixeles_descifrados)

        print(f"Imagen descifrada guardada como: {nuevo_archivo}")
        return nuevo_archivo

    except ValueError as ve:
        # Esto suele ocurrir cuando la clave es incorrecta o los datos se corrompen
        print(f"Error de padding: {ve}")
    except Exception as e:
        print(f"Error al descifrar la imagen: {e}")


def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=4, column=0, columnspan=2, pady=10)
    error_label.after(2000, error_label.destroy)

root = Tk()
root.title("Práctica 5: Modos de operacion")
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

# tipo de

# Numero Llave
Label(main_frame, text="Valor de la llave:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
valor_llave = Entry(main_frame, width=30, font=("Helvetica", 11))
valor_llave.grid(row=2, column=1, padx=10, pady=20, sticky="w")

# Crear archivos
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=3, column=0, columnspan=2, pady=30)

root.mainloop()
