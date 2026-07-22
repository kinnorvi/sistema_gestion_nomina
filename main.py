# =================================================================
# SISTEMA: Gestión de Nómina "1.0.0" - Fase 3
# MÓDULO: Orquestador Principal (Controlador de Flujo)
# AUTOR: Jorge Hernán Castro Colmenares
# INSTITUCIÓN: UNAD - Escuela de Ciencias Básicas Tecnología e Ingeniería
# =================================================================

import tkinter as tk
from tkinter import messagebox, ttk
from interfaz import AplicacionAfiliados

def mostrar_acerca_de():
    mensaje = "Curso: Estructura de Datos (301305)\nEstudiante: Jorge Castro\nGrupo: 206"
    messagebox.showinfo("Acerca de", mensaje)

def alternar_ver_clave():
    if entry_pass.cget('show') == '*':
        entry_pass.config(show='')
        btn_ver.config(text="Ocultar clave")
    else:
        entry_pass.config(show='*')
        btn_ver.config(text="Ver clave")

def intentar_login():
    if entry_pass.get() == "Caja":
        ventana_login.withdraw()
        # CORRECCIÓN: Usar Toplevel en lugar de un segundo Tk()
        main_root = tk.Toplevel(ventana_login)
        AplicacionAfiliados(main_root)
        # Si cierras la app, se cierra el proceso completo
        main_root.protocol("WM_DELETE_WINDOW", ventana_login.destroy)
    else:
        messagebox.showerror("Error", "Clave incorrecta.")

ventana_login = tk.Tk()
ventana_login.title("Login - Compensándote")
ventana_login.geometry("350x320")

barra = tk.Menu(ventana_login)
ventana_login.config(menu=barra)
barra.add_command(label="Acerca de", command=mostrar_acerca_de)

frame = ttk.Frame(ventana_login); frame.pack(padx=20, pady=20, fill=tk.BOTH)
ttk.Label(frame, text="Contraseña:").pack(pady=5)
entry_pass = ttk.Entry(frame, show="*")
entry_pass.pack(fill=tk.X, pady=5)

btn_ver = ttk.Button(frame, text="Ver clave", command=alternar_ver_clave)
btn_ver.pack(pady=5)

ttk.Separator(frame, orient='horizontal').pack(fill='x', pady=10)
ttk.Button(frame, text="Ingresar", command=intentar_login).pack(fill=tk.X, pady=5)
ttk.Button(frame, text="Salir", command=ventana_login.destroy).pack(fill=tk.X, pady=5)

ventana_login.mainloop()