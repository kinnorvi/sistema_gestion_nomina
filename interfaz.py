# =================================================================
# SISTEMA: Gestión de Nómina "1.0.0" - Fase 3
# MÓDULO: Interfaz Gráfica de Usuario (Vista con Validaciones)
# AUTOR: Jorge Hernán Castro Colmenares
# INSTITUCIÓN: UNAD - ECBTI
# =================================================================

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import re # Librería de Expresiones Regulares para validar texto
import logica
from modelos import EstructuraDatosAfiliado

class AplicacionAfiliados:
    def __init__(self, root):
        self.root = root
        self.root.title("Caja - Afiliados")
        self.configurar_gui()

    def configurar_gui(self):
        """Crea la interfaz con los asteriscos (*) de obligatoriedad del Anexo 3."""
        frame_datos = ttk.LabelFrame(self.root, text=" REGISTRO DE AFILIADOS ")
        frame_datos.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Labels con asteriscos según Figura 3 del Anexo
        ttk.Label(frame_datos, text="*Tipo de estructura:").pack(anchor=tk.W)
        self.combo_estructura = ttk.Combobox(frame_datos, values=["Pila (LIFO)", "Cola (FIFO)", "Lista Enlazada / Simple"], state="readonly")
        self.combo_estructura.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Tipo de identificación:").pack(anchor=tk.W)
        self.combo_tipo_id = ttk.Combobox(frame_datos, values=["CC", "CE", "NUIP", "PAS"], state="readonly")
        self.combo_tipo_id.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Nro. de identificación:").pack(anchor=tk.W)
        self.entry_id = ttk.Entry(frame_datos); self.entry_id.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Nombre completo:").pack(anchor=tk.W)
        self.entry_nombre = ttk.Entry(frame_datos); self.entry_nombre.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Ingresos actuales:").pack(anchor=tk.W)
        self.entry_ingresos = ttk.Entry(frame_datos); self.entry_ingresos.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Servicio deseado:").pack(anchor=tk.W)
        self.combo_servicio = ttk.Combobox(frame_datos, values=["Medicina Preventiva", "Recreación", "Educación", "Crédito", "Cultura"], state="readonly")
        self.combo_servicio.pack(fill=tk.X, pady=2)

        ttk.Label(frame_datos, text="*Modalidad de empleo:").pack(anchor=tk.W)
        #self.var_modalidad = tk.StringVar(value="Empleado")
        self.var_modalidad = tk.StringVar(master=self.root, value="Empleado")
        
        f_radio = ttk.Frame(frame_datos); f_radio.pack(anchor=tk.W)
        ttk.Radiobutton(f_radio, text="Empleado", variable=self.var_modalidad, value="Empleado").pack(side=tk.LEFT)
        ttk.Radiobutton(f_radio, text="Independiente", variable=self.var_modalidad, value="Independiente").pack(side=tk.LEFT)

        ttk.Label(frame_datos, text="Tarifa de afiliación ($):").pack(anchor=tk.W)
        self.var_tarifa = tk.StringVar()
        ttk.Entry(frame_datos, textvariable=self.var_tarifa, state="readonly").pack(fill=tk.X)

        ttk.Label(frame_datos, text="*Fecha de afiliación:").pack(anchor=tk.W)
        entry_f = ttk.Entry(frame_datos); entry_f.insert(0, datetime.now().strftime("%d/%m/%y"))
        entry_f.config(state="readonly"); entry_f.pack(fill=tk.X)

        btn_f = ttk.Frame(frame_datos); btn_f.pack(pady=10, fill=tk.X)
        ttk.Button(btn_f, text="Registrar", command=self.registrar_afiliado).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(btn_f, text="Limpiar", command=self.limpiar_campos).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        ttk.Label(frame_datos, text="DATOS DE AFILIADOS", font=("Arial", 10, "bold")).pack(pady=(15, 5))
        ttk.Label(frame_datos, text="*Ver estructura:").pack(anchor=tk.W)
        self.combo_ver = ttk.Combobox(frame_datos, values=["pila", "cola", "lista"], state="readonly")
        self.combo_ver.set("pila")
        self.combo_ver.bind("<<ComboboxSelected>>", lambda e: self.actualizar_tabla())
        self.combo_ver.pack(fill=tk.X)

        acc_f = ttk.Frame(frame_datos); acc_f.pack(fill=tk.X, pady=10)
        ttk.Button(acc_f, text="Reporte", command=self.generar_reporte).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(acc_f, text="Eliminar", command=self.eliminar_registro).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
        ttk.Button(acc_f, text="Salir", command=self.root.destroy).pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)

        frame_viz = ttk.LabelFrame(self.root, text=" Visualización ")
        frame_viz.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

        columnas = ("Tipo ID", "Número ID", "Nombre", "Ingresos", "Servicio", "Modalidad", "Tarifa", "Fecha")
        self.tabla = ttk.Treeview(frame_viz, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=115, anchor=tk.CENTER)
        
        sb = ttk.Scrollbar(frame_viz, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscroll=sb.set)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sb.pack(side=tk.RIGHT, fill=tk.Y)

    # =================================================================
    # TEMÁTICA: MÉTODOS DE VALIDACIÓN ESTRICTA
    # =================================================================
    def registrar_afiliado(self):
        """Aplica las validaciones del Anexo 3 antes de procesar los datos."""
        
        # 1. Validar Selección de Estructura
        if not self.combo_estructura.get():
            messagebox.showerror("Error", "Debe seleccionar un 'Tipo de estructura'.")
            return

        # 2. Validar Tipo de ID
        if not self.combo_tipo_id.get():
            messagebox.showerror("Error", "Debe seleccionar un 'Tipo de identificación'.")
            return

        # 3. Validar Nro de ID (Solo Números)
        id_val = self.entry_id.get()
        if not id_val.isdigit():
            messagebox.showerror("Error", "El 'Nro. de identificación' debe contener solo números.")
            return

        # 4. Validar Nombre (Solo Letras y Espacios)
        nombre_val = self.entry_nombre.get()
        # La expresión regular ^[a-zA-Z\s]+$ significa: solo letras y espacios desde el inicio al fin
        if not re.match("^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$", nombre_val) or not nombre_val.strip():
            messagebox.showerror("Error", "El 'Nombre completo' debe contener solo letras y no puede estar vacío.")
            return

        # 5. Validar Ingresos (Número positivo)
        try:
            ing = float(self.entry_ingresos.get())
            if ing < 0: raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Los 'Ingresos actuales' deben ser un valor numérico positivo.")
            return

        # 6. Validar Servicio
        if not self.combo_servicio.get():
            messagebox.showerror("Error", "Debe seleccionar un 'Servicio deseado'.")
            return

        # SI PASA TODAS LAS VALIDACIONES, PROCEDE AL CÁLCULO Y REGISTRO
        tar = logica.calcular_tarifa(ing, self.var_modalidad.get(), self.combo_servicio.get())
        self.var_tarifa.set(f"${tar:,.0f}")

        nuevo = EstructuraDatosAfiliado(
            self.combo_tipo_id.get(), id_val, nombre_val, ing, 
            self.var_modalidad.get(), self.combo_servicio.get(), tar,
            datetime.now().strftime("%d/%m/%y")
        )

        est = self.combo_estructura.get()
        if "Pila" in est: logica.pila_afiliados.append(nuevo)
        elif "Cola" in est: logica.cola_afiliados.append(nuevo)
        else: logica.lista_afiliados.append(nuevo)

        self.actualizar_tabla()
        messagebox.showinfo("Éxito", "Afiliado registrado exitosamente.")

    # ... (El resto de métodos: eliminar, actualizar_tabla, generar_reporte y limpiar_campos se mantienen igual)
    def eliminar_registro(self):
        if not messagebox.askyesno("Confirmar", "¿Desea eliminar el registro seleccionado?"): return
        ver = self.combo_ver.get()
        if ver == "pila" and logica.pila_afiliados: logica.pila_afiliados.pop()
        elif ver == "cola" and logica.cola_afiliados: logica.cola_afiliados.popleft()
        elif ver == "lista":
            id_b = self.entry_id.get()
            if not id_b.isdigit():
                messagebox.showwarning("Aviso", "Para eliminar en Lista, digite el Nro ID en la casilla correspondiente.")
                return
            encontrado = False
            for a in logica.lista_afiliados:
                if a.numero_id == id_b:
                    logica.lista_afiliados.remove(a)
                    encontrado = True
                    break
            if not encontrado: messagebox.showerror("Error", "No se encontró el ID en la Lista.")
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        ver = self.combo_ver.get()
        datos = logica.pila_afiliados if ver == "pila" else list(logica.cola_afiliados) if ver == "cola" else logica.lista_afiliados
        for a in datos:
            self.tabla.insert("", "end", values=(a.tipo_id, a.numero_id, a.nombre_afiliado, f"${a.ingresos_mensuales:,.0f}",
                                                 a.servicio_solicitado, a.modalidad_laboral, f"${a.tarifa_calculada:,.0f}", a.fecha_registro))

    def generar_reporte(self):
        ver = self.combo_ver.get()
        if ver == "pila":
            res = sum(a.tarifa_calculada for a in logica.pila_afiliados)
            messagebox.showinfo("Reporte Pila", f"Suma total de tarifas: ${res:,.0f}")
        elif ver == "cola":
            messagebox.showinfo("Reporte Cola", f"Cantidad total en cola: {len(logica.cola_afiliados)}")
        else:
            if not logica.lista_afiliados: return
            res = sum(a.ingresos_mensuales for a in logica.lista_afiliados) / len(logica.lista_afiliados)
            messagebox.showinfo("Reporte Lista", f"Promedio de ingresos: ${res:,.0f}")

    def limpiar_campos(self):
        self.entry_id.delete(0, tk.END); self.entry_nombre.delete(0, tk.END)
        self.entry_ingresos.delete(0, tk.END); self.var_tarifa.set("")