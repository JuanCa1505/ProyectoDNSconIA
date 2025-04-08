import tkinter as tk
from tkinter import ttk, messagebox
from main import buscar_dns_expuestos, verificar_resolucion_dns

def iniciar_gui():
    ventana = tk.Tk()
    ventana.title("Auditoría DNS con Shodan")
    ventana.geometry("800x500")

    # === Frame superior ===
    frame_superior = tk.Frame(ventana)
    frame_superior.pack(pady=10)

    tk.Label(frame_superior, text="IP a verificar:").grid(row=0, column=0, padx=5)
    entry_ip = tk.Entry(frame_superior)
    entry_ip.grid(row=0, column=1, padx=5)

    btn_verificar = tk.Button(frame_superior, text="Verificar IP", command=lambda: verificar_ip(entry_ip, entry_dominio))
    btn_verificar.grid(row=0, column=2, padx=5)

    # === Entrada de dominio ===
    tk.Label(ventana, text="Dominio a resolver (por ejemplo: www.google.com):").pack()
    entry_dominio = tk.Entry(ventana, width=50)
    entry_dominio.insert(0, "www.google.com")
    entry_dominio.pack(pady=5)

    # === Botón de búsqueda ===
    btn_buscar = tk.Button(ventana, text="Buscar DNS Expuestos", command=lambda: buscar_ips(tree))
    btn_buscar.pack(pady=10)

    # === Tabla de resultados ===
    columnas = ("IP", "Organización", "País")
    tree = ttk.Treeview(ventana, columns=columnas, show="headings")
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=250 if col == "Organización" else 150)
    tree.pack(expand=True, fill='both', pady=10)

    ventana.mainloop()

def buscar_ips(tree):
    tree.delete(*tree.get_children())
    resultados = buscar_dns_expuestos()
    for ip, org, pais in resultados:
        tree.insert("", "end", values=(ip, org, pais))

def verificar_ip(entry_ip, entry_dominio):
    ip = entry_ip.get()
    dominio = entry_dominio.get()
    if not ip or not dominio:
        messagebox.showwarning("Advertencia", "Debes ingresar una IP y un dominio.")
        return
    success, resultado = verificar_resolucion_dns(ip, dominio)
    if success:
        messagebox.showinfo("Éxito", f"{ip} resolvió {dominio} a: {resultado}")
    else:
        messagebox.showerror("Error", f"{ip} no pudo resolver {dominio}.")

if __name__ == "__main__":
    iniciar_gui()
