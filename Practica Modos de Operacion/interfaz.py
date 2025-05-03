from tkinter import Tk, Label, Button, Entry, StringVar, Frame, filedialog, Radiobutton
from pathlib import Path
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# funciones de selección de archivo
def seleccionar_archivo():
    archivo = filedialog.askopenfilename(filetypes=[("Archivos BMP", "*.bmp")])
    if archivo:
        label_archivo.config(text=archivo)

# ejecutar acción de cifrado/descifrado según opciones
def ejecutar_accion():
    accion = modo_accion.get()
    modo_aes_sel = modo_aes.get()  # 'ECB', 'CBC', 'CFB', 'OFB'
    clave = valor_llave.get()
    iv = valor_iv.get()
    ruta = label_archivo.cget("text")
    extension = os.path.splitext(ruta)[1]

    if ruta == "Sin seleccionar" or not clave:
        mostrar_error("Selecciona un archivo y proporciona una clave")
        return

    if extension.lower() != ".bmp":
        mostrar_error("Solo se soportan archivos BMP")
        return
    if len(clave.encode('utf-8')) != 16:
        mostrar_error("Clave AES debe tener 16, 24 o 32 caracteres")
        return

    if len(iv) != 16:
        mostrar_error("El IV debe tener exactamente 16 caracteres")
        return

    if accion == 'cifrar':
        cifrar_imagen(ruta, clave, modo_aes_sel, iv)
    else:
        descifrar_imagen(ruta, clave, modo_aes_sel, iv)

# cifrado de imagen BMP con diferentes modos AES
def cifrar_imagen(ruta_imagen, clave, modo_aes_sel, iv_usuario):
    try:
        with open(ruta_imagen, 'rb') as f:
            datos = f.read()
        pixel_offset = int.from_bytes(datos[10:14], 'little')
        encabezado = datos[:pixel_offset]
        pixeles = datos[pixel_offset:]

        key_bytes = clave.encode('utf-8')
        modo_map = {
            'ECB': AES.MODE_ECB,
            'CBC': AES.MODE_CBC,
            'CFB': AES.MODE_CFB,
            'OFB': AES.MODE_OFB
        }
        modo_const = modo_map[modo_aes_sel]

        if modo_aes_sel == 'ECB':
            cipher = AES.new(key_bytes, modo_const)
            iv = b''
        else:
            iv = iv_usuario.encode('utf-8') if iv_usuario else None
            cipher = AES.new(key_bytes, modo_const, iv=iv)

        cifrado = cipher.encrypt(pad(pixeles, AES.block_size))

        original_stem = Path(ruta_imagen).stem
        nuevo_nombre = f"{original_stem}_e_{modo_aes_sel.lower()}.bmp"

        with open(nuevo_nombre, 'wb') as out:
            out.write(encabezado)
            if iv:
                out.write(iv)
            out.write(cifrado)

        print(f"Imagen cifrada ({modo_aes_sel}) guardada como: {nuevo_nombre}")
        return nuevo_nombre
    except Exception as e:
        print(f"Error al cifrar: {e}")

# descifrado de imagen BMP con diferentes modos AES
def descifrar_imagen(ruta_cifrada, clave, modo_aes_sel, iv_usuario):
    try:
        with open(ruta_cifrada, 'rb') as f:
            datos = f.read()
        pixel_offset = int.from_bytes(datos[10:14], 'little')
        encabezado = datos[:pixel_offset]

        if modo_aes_sel == 'ECB':
            iv = b''
            datos_cifrados = datos[pixel_offset:]
        else:
            iv = iv_usuario.encode('utf-8') if iv_usuario else datos[pixel_offset:pixel_offset+16]
            datos_cifrados = datos[pixel_offset+16:]

        key_bytes = clave.encode('utf-8')
        modo_map = {
            'ECB': AES.MODE_ECB,
            'CBC': AES.MODE_CBC,
            'CFB': AES.MODE_CFB,
            'OFB': AES.MODE_OFB
        }
        modo_const = modo_map[modo_aes_sel]

        cipher = AES.new(key_bytes, modo_const, iv=iv)
        datos_desc = unpad(cipher.decrypt(datos_cifrados), AES.block_size)

        cifrado_stem = Path(ruta_cifrada).stem
        nuevo_nombre = f"{cifrado_stem}_d_{modo_aes_sel.lower()}.bmp"

        with open(nuevo_nombre, 'wb') as out:
            out.write(encabezado)
            out.write(datos_desc)

        print(f"Imagen descifrada ({modo_aes_sel}) guardada como: {nuevo_nombre}")
        return nuevo_nombre
    except ValueError as ve:
        print(f"Error de padding/clave incorrecta: {ve}")
    except Exception as e:
        print(f"Error al descifrar: {e}")

# mostrar errores en GUI
def mostrar_error(mensaje):
    error_label = Label(main_frame, text=mensaje, font=("Helvetica", 11), fg="#FF0000", bg="#F0F0F0")
    error_label.grid(row=6, column=0, columnspan=5, pady=10)
    error_label.after(2000, error_label.destroy)

# --- Configuración de la ventana principal ---
root = Tk()
root.title("Práctica 5: Modos de Operación AES")
root.geometry("800x600")
root.configure(bg="#F0F0F0")

# Encabezado
header_frame = Frame(root, bg="#800020", bd=1, relief="solid")
header_frame.pack(fill="x")
header_label = Label(header_frame, text="Práctica 5: Modos de Operación AES", font=("Helvetica", 14, "bold"), fg="#FFFFFF", bg="#800020")
header_label.pack(pady=5)

# Subencabezado con nombres
subheader_frame = Frame(root, bg="#700010")
subheader_frame.pack(fill="x")
subheader_label = Label(subheader_frame, text="Equipo:\n\nAbsalón Cortés Sebastian\nFernandez Villar Cuauhtemoc\nTaboada Montiel Enrique", font=("Helvetica", 12, "italic"), fg="#FFFFFF", bg="#700010")
subheader_label.pack(pady=5)

# Marco principal
main_frame = Frame(root, bg="#F0F0F0")
main_frame.pack(pady=20)

# Seleccionar archivo
Button(main_frame, text="Seleccionar archivo BMP", command=seleccionar_archivo, font=("Helvetica", 11)).grid(row=0, column=0, padx=10, pady=10)
label_archivo = Label(main_frame, text="Sin seleccionar", width=40, anchor="w", bg="#FFFFFF", relief="solid", font=("Helvetica", 11))
label_archivo.grid(row=0, column=1, columnspan=4, padx=10, pady=10)

# Acción: cifrar o descifrar
modo_accion = StringVar(value="cifrar")
Radiobutton(main_frame, text="Cifrar", variable=modo_accion, value="cifrar", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=0, sticky="w", padx=10)
Radiobutton(main_frame, text="Descifrar", variable=modo_accion, value="descifrar", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=1, sticky="w")

# Modo AES
Label(main_frame, text="Modo AES:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=0, sticky="w", padx=10)
modo_aes = StringVar(value="CBC")
for i, modo in enumerate(["ECB", "CBC", "CFB", "OFB"]):
    Radiobutton(main_frame, text=modo, variable=modo_aes, value=modo, bg="#F0F0F0", font=("Helvetica", 11)).grid(row=2, column=1+i, sticky="w")

# Valor de la llave AES
Label(main_frame, text="Valor de la llave:", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=3, column=0, sticky="w", padx=10)
valor_llave = Entry(main_frame, width=30, font=("Helvetica", 11))
valor_llave.grid(row=3, column=1, columnspan=3, padx=10, pady=5, sticky="w")

# Valor del vector de inicialización (IV)
Label(main_frame, text="Vector de inicialización (IV):", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=4, column=0, sticky="w", padx=10)
valor_iv = Entry(main_frame, width=30, font=("Helvetica", 11))
valor_iv.grid(row=4, column=1, columnspan=3, padx=10, pady=5, sticky="w")

# Botón de ejecución
Button(main_frame, text="Ejecutar", command=ejecutar_accion, bg="#800020", fg="#FFFFFF", font=("Helvetica", 12, 'bold'), width=10, height=2).grid(row=5, column=0, columnspan=5, pady=30)

root.mainloop()
