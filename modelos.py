# =================================================================
# SISTEMA: Gestión de Nómina "1.0.0" - Fase 3
# MÓDULO: Interfaz Gráfica de Usuario (Vista con Validaciones)
# AUTOR: Jorge Hernán Castro Colmenares
# INSTITUCIÓN: UNAD - ECBTI
# =================================================================


# =================================================================
# TEMÁTICA: MODELO DE DATOS (POO)
# =================================================================

class EstructuraDatosAfiliado:
    """Clase que define los atributos del afiliado según la Tabla de Abstracción."""
    def __init__(self, tipo_id, numero_id, nombre_afiliado, ingresos_mensuales, 
                 modalidad_laboral, servicio_solicitado, tarifa_calculada, fecha_registro):
        self.tipo_id = tipo_id
        self.numero_id = numero_id
        self.nombre_afiliado = nombre_afiliado
        self.ingresos_mensuales = ingresos_mensuales
        self.modalidad_laboral = modalidad_laboral
        self.servicio_solicitado = servicio_solicitado
        self.tarifa_calculada = tarifa_calculada
        self.fecha_registro = fecha_registro