import tkinter as tk
from tkinter import messagebox, ttk
from config import QUERY_BASE
from mainAvanzado import buscar_dns_expuestos, verificar_ip, resolver_con_ip
import os

# Página global para paginación
pagina_actual = 1
RESULTADOS_POR_PAGINA = 15

def iniciar_gui():
    global pagina_actual

    ventana = tk.Tk()
    ventana.title("Auditoría DNS con Shodan")
    ventana.geometry("800x540")

    frame = tk.Frame(ventana)
    frame.pack(pady=10, fill="x")

    # Entrada IP
    tk.Label(frame, text="IP a verificar:").grid(row=0, column=0, sticky="w", padx=5)
    entry_ip = tk.Entry(frame, width=25)
    entry_ip.grid(row=0, column=1, padx=5)

    # Entrada dominios
    tk.Label(frame, text="Dominios (separados por coma):").grid(row=1, column=0, sticky="w", padx=5)
    entry_dominios = tk.Entry(frame, width=50)
    entry_dominios.insert(0, "www.google.com, www.microsoft.com")
    entry_dominios.grid(row=1, column=1, columnspan=2, pady=5, padx=5, sticky="we")

    # Función Verificar IP
    def verificar_ip_input():
        ip = entry_ip.get()
        dominios = entry_dominios.get()
        if not ip:
            messagebox.showwarning("Campo vacío", "Por favor ingresa una IP.")
            return
        resultado_shodan = verificar_ip(ip)
        resultado_dns = resolver_con_ip(ip, dominios)
        resultado_total = f"""
🔎 Verificación de IP: {ip}

📡 Estado del puerto DNS (53):
{resultado_shodan}

🌐 Resolución de dominios:
{resultado_dns}
        """
        messagebox.showinfo("Resultado de Verificación DNS", resultado_total.strip())

    # Botón de verificación
    tk.Button(frame, text="Verificar IP", command=verificar_ip_input).grid(row=0, column=2, padx=10)

    # Botón para iniciar búsqueda
    tk.Button(frame, text="Buscar DNS Expuestos", command=lambda: ejecutar_busqueda()).grid(row=2, column=1, pady=10)

    # Botón para ver IPs en blacklist
    def mostrar_blacklist():
        if os.path.exists("coincidencias_blacklist.txt"):
            with open("coincidencias_blacklist.txt", "r") as f:
                contenido = f.read()
            messagebox.showinfo("IPs en la Blacklist", contenido)
        else:
            messagebox.showinfo("Blacklist", "No hay coincidencias registradas todavía.")

    tk.Button(frame, text="Ver IPs en Blacklist", command=mostrar_blacklist).grid(row=2, column=2, pady=10, padx=5)

    # Botón para mostrar texto de ética
    def mostrar_etica():
        texto = (
            "Este programa ha sido creado con fines exclusivamente educativos y defensivos.\n\n"
            "El uso de la API de Shodan se realiza de forma responsable y respetando sus términos.\n"
            "No se realiza ningún tipo de intrusión o explotación, únicamente análisis de información pública.\n\n"
            "El usuario final es responsable del uso de esta herramienta. Se recomienda su uso sólo en entornos autorizados,"
            " como laboratorios de práctica o redes propias.\n\n"
            "Fuente de datos: https://www.shodan.io"
        )
        messagebox.showinfo("Ética y Uso Responsable", texto)

    tk.Button(frame, text="Ver Declaración Ética", command=mostrar_etica).grid(row=2, column=0, pady=10, padx=5)

    # Tabla de resultados (máximo 15 por página)
    columnas = ("IP", "Organización", "País")
    tree = ttk.Treeview(ventana, columns=columnas, show='headings', height=RESULTADOS_POR_PAGINA)
    for col in columnas:
        tree.heading(col, text=col)
        tree.column(col, width=260 if col == "Organización" else 150, anchor="w")
    tree.pack(pady=10, expand=True, fill="both")

    # Etiqueta de cantidad de IPs encontradas
    label_resultado = tk.Label(ventana, text="Total de IPs encontradas: 0")
    label_resultado.pack(pady=2)

    # Paginación
    pagination_frame = tk.Frame(ventana)
    pagination_frame.pack(pady=5, fill="x")

    label_pagina = tk.Label(pagination_frame, text=f"Página: {pagina_actual}")
    label_pagina.pack(side="left", padx=10)

    def ejecutar_busqueda():
        global pagina_actual
        label_pagina.config(text=f"Página: {pagina_actual}")
        resultados = buscar_dns_expuestos(QUERY_BASE, pagina_actual)
        label_resultado.config(text=f"Total de IPs encontradas: {len(resultados)}")
        for item in tree.get_children():
            tree.delete(item)
        for ip, org, pais in resultados[:RESULTADOS_POR_PAGINA]:
            tree.insert("", "end", values=(ip, org, pais))

    def siguiente_pagina():
        global pagina_actual
        pagina_actual += 1
        ejecutar_busqueda()

    def pagina_anterior():
        global pagina_actual
        if pagina_actual > 1:
            pagina_actual -= 1
            ejecutar_busqueda()

    # Botones de paginación
    tk.Button(pagination_frame, text="← Página anterior", command=pagina_anterior).pack(side="left")
    tk.Button(pagination_frame, text="Siguiente página →", command=siguiente_pagina).pack(side="left")

    ventana.mainloop()

if __name__ == "__main__":
    iniciar_gui()
