# =================================================================
# SISTEMA: Gestión de Nómina "1.0.0" - Fase 3
# MÓDULO: Interfaz Gráfica de Usuario (Vista con Validaciones)
# AUTOR: Jorge Hernán Castro Colmenares
# INSTITUCIÓN: UNAD - ECBTI
# =================================================================


# =================================================================
# TEMÁTICA: LÓGICA DE NEGOCIO Y ESTRUCTURAS
# =================================================================
from collections import deque

pila_afiliados = []
cola_afiliados = deque()
lista_afiliados = []

def calcular_tarifa(ingresos, modalidad, servicio):
    base = 0
    # 1. Determinamos la base según modalidad y rango
    if modalidad == "Empleado":
        if ingresos <= 2000000: base = 45000
        elif ingresos <= 3000000: base = 60000
        elif ingresos <= 4000000: base = 75000
        elif ingresos <= 5000000: base = 90000
        else: base = 150000
    else: # Independiente
        if ingresos <= 2000000: base = 10000
        elif ingresos <= 3000000: base = 20000
        elif ingresos <= 4000000: base = 30000
        elif ingresos <= 5000000: base = 40000
        else: base = 80000

    # 2. Aplicamos recargos (Convertimos a minúsculas para evitar errores)
    servicio_buscado = servicio.lower()
    
    if "medicina preventiva" in servicio_buscado:
        base = base + (ingresos * 0.10)
    
    # Valores fijos adicionales
    adicionales = {
        "recreación": 2500,
        "educación": 7500,
        "crédito": 0,
        "cultura": 10000
    }
    
    # Retornamos la base + el adicional (si existe en la lista)
    return base + adicionales.get(servicio_buscado, 0)