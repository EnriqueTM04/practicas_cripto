from tkinter import (
    Tk, Label, Button, Text, StringVar, Frame, LabelFrame,
    filedialog, Radiobutton, Scrollbar, LEFT, RIGHT, BOTH, X, Y, NSEW, END
)
from pathlib import Path
import os
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def rsa_encrypt_file(path, key_pem):
    key = RSA.import_key(key_pem)
    cipher = PKCS1_OAEP.new(key)
    data = Path(path).read_bytes()
    max_blk = key.size_in_bytes() - 2*hashlib.sha256().digest_size - 2
    chunks = (data[i:i+max_blk] for i in range(0, len(data), max_blk))
    encrypted = b"".join(cipher.encrypt(c) for c in chunks)
    out = Path(path).with_name(Path(path).stem + "_c" + Path(path).suffix)
    out.write_bytes(encrypted)
    return str(out)

def rsa_decrypt_file(path, key_pem):
    key = RSA.import_key(key_pem)
    cipher = PKCS1_OAEP.new(key)
    data = Path(path).read_bytes()
    blk = key.size_in_bytes()
    chunks = (data[i:i+blk] for i in range(0, len(data), blk))
    decrypted = b"".join(cipher.decrypt(c) for c in chunks)
    stem = Path(path).stem
    if stem.endswith("_c"):
        stem = stem[:-2]
    out = Path(path).with_name(stem + "_d" + Path(path).suffix)
    out.write_bytes(decrypted)
    return str(out)

def seleccionar_archivo():
    archivo = filedialog.askopenfilename(
        filetypes=[("TXT", "*.txt")]
    )
    if archivo:
        label_archivo.config(text=archivo)

def ejecutar_accion():
    modo = modo_rsa.get()
    archivo = label_archivo.cget("text")
    key_pem = text_llave.get("1.0", END).strip()
    if archivo == "Sin seleccionar" or not key_pem:
        mostrar_error("Selecciona archivo y pega tu clave PEM")
        return
    try:
        if modo == "encrypt":
            nuevo = rsa_encrypt_file(archivo, key_pem)
            status_label.config(text=f"Cifrado → {nuevo}")
        else:
            nuevo = rsa_decrypt_file(archivo, key_pem)
            status_label.config(text=f"Descifrado → {nuevo}")
    except Exception as e:
        mostrar_error("Error al procesar con esa clave")
        print(e)

def mostrar_error(msg):
    status_label.config(text=msg, fg="#D00")

root = Tk()
root.title("Practica RSA")
root.geometry("850x650")
root.configure(bg="#F0F0F0")

# Header
header = Frame(root, bg="#800020", bd=1, relief="solid")
header.pack(fill=X)
Label(
    header, text="Practica RSA", fg="#FFF",
    bg="#800020", font=("Helvetica", 16, "bold"), pady=8
).pack()

# Equipo
sub = Frame(root, bg="#700010")
sub.pack(fill=X)
Label(
    sub, text="Equipo:\nAbsalón Cortés Sebastián\nFernandez Villar Cuauhtémoc\nTaboada Montiel Enrique",
    fg="#FFF", bg="#700010", font=("Helvetica", 11, "italic"), pady=6
).pack()

# Main area
main = Frame(root, bg="#F0F0F0")
main.pack(fill=BOTH, expand=True, padx=15, pady=10)

# Sección de archivo y modo
sec_file = LabelFrame(main, text="Archivo y Modo", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
sec_file.grid(row=0, column=0, sticky=NSEW, padx=(0,10), pady=5)
sec_file.columnconfigure(1, weight=1)

Button(sec_file, text="Seleccionar archivo", command=seleccionar_archivo, font=("Helvetica", 11)).grid(row=0, column=0, padx=5, pady=10, sticky="w")
label_archivo = Label(sec_file, text="Sin seleccionar", bg="#FFF", relief="solid", anchor="w", font=("Helvetica", 11))
label_archivo.grid(row=0, column=1, padx=5, pady=10, sticky="ew")

modo_rsa = StringVar(value="encrypt")
Radiobutton(sec_file, text="Cifrar", variable=modo_rsa, value="encrypt", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=0, padx=5, pady=5, sticky="w")
Radiobutton(sec_file, text="Descifrar", variable=modo_rsa, value="decrypt", bg="#F0F0F0", font=("Helvetica", 11)).grid(row=1, column=1, padx=5, pady=5, sticky="w")

# Sección de clave PEM
sec_key = LabelFrame(main, text="Clave PEM", font=("Helvetica", 12, "bold"), bg="#F0F0F0")
sec_key.grid(row=0, column=1, sticky=NSEW, pady=5)
sec_key.rowconfigure(0, weight=1)
sec_key.columnconfigure(0, weight=1)

text_llave = Text(sec_key, font=("Courier", 9))
text_llave.grid(row=0, column=0, sticky=NSEW, padx=(5,0), pady=5)
scroll = Scrollbar(sec_key, command=text_llave.yview)
scroll.grid(row=0, column=1, sticky="ns", pady=5, padx=(0,5))
text_llave.configure(yscrollcommand=scroll.set)

# Área de estado y botón
bottom = Frame(root, bg="#F0F0F0")
bottom.pack(fill=X, padx=15, pady=(0,15))
status_label = Label(bottom, text="", font=("Helvetica", 11), bg="#F0F0F0")
status_label.pack(side=LEFT, padx=5)

Button(
    bottom, text="Ejecutar", command=ejecutar_accion,
    bg="#800020", fg="#FFF", font=("Helvetica", 12, "bold"),
    width=14, height=1
).pack(side=RIGHT, padx=5)

# Configurar redimensionamiento
root.grid_rowconfigure(0, weight=0)
root.grid_rowconfigure(1, weight=0)
root.grid_rowconfigure(2, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

main.grid_rowconfigure(0, weight=1)
main.grid_columnconfigure(0, weight=1)
main.grid_columnconfigure(1, weight=2)

root.mainloop()
