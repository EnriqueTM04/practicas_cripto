from tkinter import (
    Tk, Label, Button, Text, StringVar, Frame, LabelFrame,
    filedialog, Radiobutton, Scrollbar, LEFT, RIGHT, BOTH, X, Y, NSEW, END,
    Entry, messagebox
)
from pathlib import Path
import os
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad
import secrets
import base64

# Variables globales
archivo_seleccionado = ""
modo_operacion = None


def generar_clave_dh(g, n, a):
    """Genera la clave pública de Diffie-Hellman"""
    return pow(g, a, n)


def calcular_secreto_compartido(clave_publica, clave_privada, n):
    """Calcula el secreto compartido de Diffie-Hellman"""
    return pow(clave_publica, clave_privada, n)


def derivar_clave_aes(secreto_compartido):
    """Deriva una clave AES de 256 bits del secreto compartido"""
    hash_obj = hashlib.sha256(str(secreto_compartido).encode())
    return hash_obj.digest()


def generar_parametros_dh():
    """Genera automáticamente las claves privadas de Diffie-Hellman"""
    # Generar claves privadas aleatorias
    a = secrets.randbelow(100) + 1  # Entre 1 y 100
    b = secrets.randbelow(100) + 1  # Entre 1 y 100

    # Actualizar la interfaz con los valores generados
    entry_a.delete(0, END)
    entry_a.insert(0, str(a))
    entry_b.delete(0, END)
    entry_b.insert(0, str(b))

    return a, b


def seleccionar_archivo():
    global archivo_seleccionado
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=[("Todos los archivos", "*.*"), ("Archivos de texto", "*.txt")]
    )
    if archivo:
        archivo_seleccionado = archivo
        label_archivo.config(text=f"Archivo: {os.path.basename(archivo)}")
        log_text.insert(END, f"Archivo seleccionado: {archivo}\n")


def seleccionar_clave_privada():
    archivo = filedialog.askopenfilename(
        title="Seleccionar clave privada RSA",
        filetypes=[("Archivos de texto", "*.txt"), ("Archivos PEM", "*.pem")]
    )
    if archivo:
        entry_clave_privada.delete(0, END)
        entry_clave_privada.insert(0, archivo)


def seleccionar_clave_publica():
    archivo = filedialog.askopenfilename(
        title="Seleccionar clave pública RSA",
        filetypes=[("Archivos de texto", "*.txt"), ("Archivos PEM", "*.pem")]
    )
    if archivo:
        entry_clave_publica.delete(0, END)
        entry_clave_publica.insert(0, archivo)


def obtener_parametros_dh():
    """Obtiene los parámetros de Diffie-Hellman de la interfaz"""
    try:
        g = int(entry_g.get())
        p = int(entry_n.get())
        a = int(entry_a.get())
        b = int(entry_b.get())
        return g, p, a, b
    except ValueError:
        messagebox.showerror("Error", "Los parámetros de Diffie-Hellman deben ser números enteros")
        return None


def cifrar_archivo():
    if not archivo_seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un archivo")
        return

    # Generar automáticamente las claves privadas DH
    log_text.insert(END, "Generando claves privadas de Diffie-Hellman...\n")
    generar_parametros_dh()

    # Obtener parámetros DH
    params = obtener_parametros_dh()
    if not params:
        return
    g, p, a, b = params

    # Obtener clave privada RSA
    ruta_clave_privada = entry_clave_privada.get()
    if not ruta_clave_privada:
        messagebox.showerror("Error", "Debe seleccionar la clave privada RSA")
        return

    try:
        # Leer archivo original
        with open(archivo_seleccionado, 'rb') as f:
            contenido_original = f.read()

        log_text.insert(END, "Iniciando proceso de cifrado...\n")

        # 1. Diffie-Hellman para AES
        clave_publica_a = generar_clave_dh(g, p, a)
        clave_publica_b = generar_clave_dh(g, p, b)
        secreto_compartido = calcular_secreto_compartido(clave_publica_b, a, p)
        clave_aes = derivar_clave_aes(secreto_compartido)

        log_text.insert(END, f"Parámetros DH generados - g: {g}, p: {p}\n")
        log_text.insert(END, f"Claves privadas - a: {a}, b: {b}\n")
        log_text.insert(END, f"Clave pública A: {clave_publica_a}\n")
        log_text.insert(END, f"Clave pública B: {clave_publica_b}\n")
        log_text.insert(END, "Secreto compartido generado para AES\n")

        # 2. Cifrar con AES CBC
        iv = secrets.token_bytes(16)  # Vector de inicialización
        cipher_aes = AES.new(clave_aes, AES.MODE_CBC, iv)
        contenido_cifrado = cipher_aes.encrypt(pad(contenido_original, AES.block_size))

        log_text.insert(END, "Archivo cifrado con AES-CBC\n")

        # 3. Hash SHA3 del documento original
        hash_obj = SHA3_256.new()
        hash_obj.update(contenido_original)
        hash_documento = hash_obj.digest()

        log_text.insert(END, "Hash SHA3 generado\n")

        # 4. Firmar hash con RSA
        with open(ruta_clave_privada, 'r') as f:
            clave_privada_rsa = RSA.import_key(f.read())

        firma = pkcs1_15.new(clave_privada_rsa).sign(hash_obj)

        log_text.insert(END, "Firma RSA generada\n")

        # 5. Crear archivo final
        # Formato simplificado: IV (16 bytes) + Contenido cifrado + Separador + Firma
        separador = b"---FIRMA---"
        contenido_final = iv + contenido_cifrado + separador + firma

        # Guardar archivo cifrado
        base, _ = os.path.splitext(archivo_seleccionado)
        archivo_salida = f"{base}_cifrado.txt"
        with open(archivo_salida, 'wb') as f:
            f.write(contenido_final)

        log_text.insert(END, f"Archivo cifrado guardado como: {archivo_salida}\n")
        log_text.insert(END, "IMPORTANTE: Para descifrar, use los mismos parámetros DH mostrados arriba\n")
        messagebox.showinfo("Éxito",
                            f"Archivo cifrado correctamente.\nGuardado como: {os.path.basename(archivo_salida)}\n\nRECUERDE: Anote los parámetros DH mostrados en el log para poder descifrar.")

    except Exception as e:
        log_text.insert(END, f"Error durante el cifrado: {str(e)}\n")
        messagebox.showerror("Error", f"Error durante el cifrado: {str(e)}")


def descifrar_archivo():
    if not archivo_seleccionado:
        messagebox.showerror("Error", "Debe seleccionar un archivo cifrado")
        return

    # Obtener parámetros DH (deben ser los mismos usados en el cifrado)
    params = obtener_parametros_dh()
    if not params:
        return
    g, p, a, b = params

    # Obtener clave pública RSA
    ruta_clave_publica = entry_clave_publica.get()
    if not ruta_clave_publica:
        messagebox.showerror("Error", "Debe seleccionar la clave pública RSA")
        return

    try:
        # Leer archivo cifrado
        with open(archivo_seleccionado, 'rb') as f:
            contenido_cifrado_completo = f.read()

        log_text.insert(END, "Iniciando proceso de descifrado...\n")

        # Separar componentes (solo IV + contenido cifrado + firma)
        if b"---FIRMA---" not in contenido_cifrado_completo:
            raise ValueError("Formato de archivo no válido - no se encontró separador de firma")

        datos_cifrados, firma = contenido_cifrado_completo.split(b"---FIRMA---", 1)

        # Extraer IV y contenido cifrado
        if len(datos_cifrados) < 16:
            raise ValueError("Archivo demasiado pequeño - formato inválido")

        iv = datos_cifrados[:16]
        contenido_cifrado = datos_cifrados[16:]

        log_text.insert(END, "Componentes del archivo separados\n")

        # Recalcular secreto compartido con los parámetros proporcionados
        clave_publica_a = generar_clave_dh(g, p, a)
        clave_publica_b = generar_clave_dh(g, p, b)
        secreto_compartido = calcular_secreto_compartido(clave_publica_b, a, p)
        clave_aes = derivar_clave_aes(secreto_compartido)

        log_text.insert(END, f"Usando parámetros DH - g: {g}, p: {p}, a: {a}, b: {b}\n")
        log_text.insert(END, "Secreto compartido recalculado\n")

        # Descifrar con AES
        cipher_aes = AES.new(clave_aes, AES.MODE_CBC, iv)
        contenido_descifrado = unpad(cipher_aes.decrypt(contenido_cifrado), AES.block_size)

        log_text.insert(END, "Archivo descifrado con AES-CBC\n")

        # Guardar archivo descifrado
        base, _ = os.path.splitext(archivo_seleccionado)
        archivo_descifrado = f"{base}_descifrado.txt"
        with open(archivo_descifrado, 'wb') as f:
            f.write(contenido_descifrado)

        log_text.insert(END, f"Archivo descifrado guardado como: {archivo_descifrado}\n")

        # Verificar firma
        hash_obj = SHA3_256.new()
        hash_obj.update(contenido_descifrado)

        with open(ruta_clave_publica, 'r') as f:
            clave_publica_rsa = RSA.import_key(f.read())

        try:
            pkcs1_15.new(clave_publica_rsa).verify(hash_obj, firma)
            resultado_verificacion = "✓ FIRMA VÁLIDA - El documento es auténtico"
            log_text.insert(END, "Verificación de firma: ÉXITO\n")
            messagebox.showinfo("Verificación", f"Descifrado exitoso!\n\n{resultado_verificacion}")
        except:
            resultado_verificacion = "✗ FIRMA INVÁLIDA - El documento puede haber sido modificado"
            log_text.insert(END, "Verificación de firma: FALLÓ\n")
            messagebox.showwarning("Verificación", f"Descifrado completado, pero:\n\n{resultado_verificacion}")

        log_text.insert(END, f"Resultado: {resultado_verificacion}\n")

    except Exception as e:
        log_text.insert(END, f"Error durante el descifrado: {str(e)}\n")
        messagebox.showerror("Error", f"Error durante el descifrado: {str(e)}")


def procesar():
    if modo_operacion.get() == "cifrar":
        cifrar_archivo()
    elif modo_operacion.get() == "descifrar":
        descifrar_archivo()
    else:
        messagebox.showerror("Error", "Debe seleccionar una operación")


def limpiar_log():
    log_text.delete(1.0, END)
    # Restaurar mensaje inicial
    log_text.insert(END, "Programa de Criptografía Híbrida iniciado.\n")
    log_text.insert(END, "Funcionalidades:\n")
    log_text.insert(END, "- Cifrado AES-CBC con claves derivadas de Diffie-Hellman\n")
    log_text.insert(END, "- Firma digital RSA con hash SHA3\n")
    log_text.insert(END, "- Verificación de integridad y autenticidad\n")
    log_text.insert(END, "- Generación automática de claves DH para cifrado\n\n")


def generar_nuevas_claves_dh():
    """Botón para generar nuevas claves DH manualmente"""
    generar_parametros_dh()
    log_text.insert(END, f"Nuevas claves DH generadas - a: {entry_a.get()}, b: {entry_b.get()}\n")


# Crear ventana principal
root = Tk()
root.title("Práctica Criptografía Híbrida - DH Automático")
root.geometry("900x750")
root.configure(bg="#F0F0F0")

# Header
header = Frame(root, bg="#800020", bd=1, relief="solid")
header.pack(fill=X)
Label(
    header,
    text="Práctica Criptografía Híbrida - DH Automático",
    fg="#FFF",
    bg="#800020",
    font=("Helvetica", 16, "bold"),
    pady=8
).pack()

# Equipo
sub = Frame(root, bg="#700010")
sub.pack(fill=X)
Label(
    sub,
    text="Equipo:\nAbsalón Cortés Sebastián\nFernandez Villar Cuauhtémoc\nTaboada Montiel Enrique",
    fg="#FFF",
    bg="#700010",
    font=("Helvetica", 11, "italic"),
    pady=6
).pack()

# Main area
main = Frame(root, bg="#F0F0F0")
main.pack(fill=BOTH, expand=True, padx=10, pady=10)

# Selección de archivo
frame_archivo = LabelFrame(main, text="Selección de Archivo", font=("Helvetica", 10, "bold"))
frame_archivo.pack(fill=X, pady=5)

Button(frame_archivo, text="Seleccionar Archivo", command=seleccionar_archivo, bg="#4CAF50", fg="white").pack(side=LEFT,
                                                                                                              padx=5,
                                                                                                              pady=5)
label_archivo = Label(frame_archivo, text="Ningún archivo seleccionado", fg="gray")
label_archivo.pack(side=LEFT, padx=10)

# Modo de operación
frame_modo = LabelFrame(main, text="Modo de Operación", font=("Helvetica", 10, "bold"))
frame_modo.pack(fill=X, pady=5)

modo_operacion = StringVar(master=root, value="cifrar")

modo_operacion.set("cifrar")
Radiobutton(frame_modo, text="Cifrar", variable=modo_operacion, value="cifrar").pack(side=LEFT, padx=10)
Radiobutton(frame_modo, text="Descifrar", variable=modo_operacion, value="descifrar").pack(side=LEFT, padx=10)

# Parámetros Diffie-Hellman
frame_dh = LabelFrame(main, text="Parámetros Diffie-Hellman (Automáticos en cifrado)", font=("Helvetica", 10, "bold"))
frame_dh.pack(fill=X, pady=5)

Label(frame_dh, text="g:").grid(row=0, column=0, padx=5, pady=2)
entry_g = Entry(frame_dh, width=10)
entry_g.grid(row=0, column=1, padx=5, pady=2)
entry_g.insert(0, "2")

Label(frame_dh, text="p (primo):").grid(row=0, column=2, padx=5, pady=2)
entry_n = Entry(frame_dh, width=15)
entry_n.grid(row=0, column=3, padx=5, pady=2)
entry_n.insert(0, "23")

Label(frame_dh, text="a (privada):").grid(row=1, column=0, padx=5, pady=2)
entry_a = Entry(frame_dh, width=10)
entry_a.grid(row=1, column=1, padx=5, pady=2)
entry_a.insert(0, "6")

Label(frame_dh, text="b (privada):").grid(row=1, column=2, padx=5, pady=2)
entry_b = Entry(frame_dh, width=10)
entry_b.grid(row=1, column=3, padx=5, pady=2)
entry_b.insert(0, "15")

Button(frame_dh, text="Generar Nuevas Claves", command=generar_nuevas_claves_dh, bg="#9C27B0", fg="white").grid(row=1,
                                                                                                                column=4,
                                                                                                                padx=5,
                                                                                                                pady=2)

# Claves RSA
frame_rsa = LabelFrame(main, text="Claves RSA", font=("Helvetica", 10, "bold"))
frame_rsa.pack(fill=X, pady=5)

Label(frame_rsa, text="Clave Privada:").grid(row=0, column=0, padx=5, pady=2, sticky="w")
entry_clave_privada = Entry(frame_rsa, width=40)
entry_clave_privada.grid(row=0, column=1, padx=5, pady=2)
Button(frame_rsa, text="Buscar", command=seleccionar_clave_privada).grid(row=0, column=2, padx=5, pady=2)

Label(frame_rsa, text="Clave Pública:").grid(row=1, column=0, padx=5, pady=2, sticky="w")
entry_clave_publica = Entry(frame_rsa, width=40)
entry_clave_publica.grid(row=1, column=1, padx=5, pady=2)
Button(frame_rsa, text="Buscar", command=seleccionar_clave_publica).grid(row=1, column=2, padx=5, pady=2)

# Botones de acción
frame_botones = Frame(main)
frame_botones.pack(fill=X, pady=10)

Button(frame_botones, text="Procesar", command=procesar, bg="#2196F3", fg="white", font=("Helvetica", 12, "bold")).pack(
    side=LEFT, padx=5)
Button(frame_botones, text="Limpiar Log", command=limpiar_log, bg="#FF9800", fg="white").pack(side=LEFT, padx=5)

# Log de operaciones
frame_log = LabelFrame(main, text="Log de Operaciones", font=("Helvetica", 10, "bold"))
frame_log.pack(fill=BOTH, expand=True, pady=5)

log_text = Text(frame_log, height=15, wrap="word")
scrollbar = Scrollbar(frame_log, orient="vertical", command=log_text.yview)
log_text.configure(yscrollcommand=scrollbar.set)

log_text.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.pack(side=RIGHT, fill=Y)

# Mensaje inicial
log_text.insert(END, "Programa de Criptografía Híbrida iniciado.\n")
log_text.insert(END, "Funcionalidades:\n")
log_text.insert(END, "- Cifrado AES-CBC con claves derivadas de Diffie-Hellman\n")
log_text.insert(END, "- Firma digital RSA con hash SHA3\n")
log_text.insert(END, "- Verificación de integridad y autenticidad\n")
log_text.insert(END, "- Generación automática de claves DH para cifrado\n\n")

root.mainloop()