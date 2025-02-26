import tkinter as tk
from tkinter import filedialog, messagebox

def shift_letter(char, shift):
    """Aplica un cifrado César solo a letras del alfabeto."""
    if 'a' <= char <= 'z': 
        return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    return char  
# Otros caracteres no cambian

def shift_text(input_file, output_file, shift):
    """Cifra un archivo desplazando solo letras del alfabeto y guarda el desplazamiento."""
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        # Guarda el desplazamiento en la primera línea
        outfile.write(f"{shift}\n")

        for line in infile: #lee la linea
            shifted_line = ''.join(shift_letter(char, shift) for char in line) #cifra la linea
            outfile.write(shifted_line) #escribe la linea cifrada

def unshift_text(input_file, output_file):
    """Descifra un archivo usando el desplazamiento guardado en la primera línea."""
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()
    
    shift = int(lines[0].strip())  # Recupera el desplazamiento
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines[1:]:  # Omite la primera línea con el desplazamiento
            unshifted_line = ''.join(shift_letter(char, -shift) for char in line)
            outfile.write(unshifted_line)

def open_file(mode):
    """Gestiona la selección de archivos y llama a las funciones adecuadas."""
    input_file = filedialog.askopenfilename(title="Selecciona un archivo", filetypes=[("Text files", "*.txt")])
    if not input_file:
        return
    
    output_file = filedialog.asksaveasfilename(title="Guardar archivo", defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if not output_file:
        return

    if mode == "encrypt":
        try:
            shift = int(shift_entry.get())  # Obtener el valor de la entrada de texto
            if 0 <= shift <= 26:
                shift_text(input_file, output_file, shift)
                messagebox.showinfo("Éxito", f"Archivo cifrado con desplazamiento {shift} y guardado con éxito.")
            else:
                messagebox.showerror("Error", "Solo puede ser el desplazamiento entre 0 y 26")
        except ValueError:
            messagebox.showerror("Error", "Cambia el numero.")
    
    elif mode == "decrypt":
        unshift_text(input_file, output_file)
        messagebox.showinfo("Éxito", "Archivo descifrado y guardado con éxito.")

# Configurar la GUI
root = tk.Tk()
root.title("Cifrador César (Solo Letras)")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Ingrese el desplazamiento (0-26):").pack()
shift_entry = tk.Entry(frame)
shift_entry.pack(pady=5)

encrypt_button = tk.Button(frame, text="Cifrar Archivo", command=lambda: open_file("encrypt"))
encrypt_button.pack(pady=5)

decrypt_button = tk.Button(frame, text="Descifrar Archivo", command=lambda: open_file("decrypt"))
decrypt_button.pack(pady=5)

root.mainloop()