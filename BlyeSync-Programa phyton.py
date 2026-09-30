"""
SISTEMA DIGITAL DH PROYECTOS Y CONTRATISTAS S.A.C. - BLUESYNC
Nivel: Fundamentos de Programación (2do Ciclo)
Código Base para Trabajo Colaborativo en Grupo (5 Funciones Pendientes)
"""
from datetime import datetime
import os

NOMBRE_ARCHIVO = "comprobantes_dhproyectos.txt"

# Catálogos base del sistema
PRECIO_CONSTRUCCION = {"Básico": 900.0, "Premium": 1200.0}

PRECIO_MANO_OBRA = {
    "1": {"nombre": "Cuadrilla Bási-k (3 personas)", "costo_dia": 150.0},
    "2": {"nombre": "Cuadrilla Estándar (5 personas)", "costo_dia": 250.0},
    "3": {"nombre": "Cuadrilla Pro-Master (8 personas)", "costo_dia": 400.0}
}

PRECIO_MANTENIMIENTO = {"Tarifa Hora": 50.0, "Kit Quimicos": 80.0}

CATALOGO_MATERIALES = {
    "1": {"nombre": "Bomba Centrífuga 2HP", "precio": 450.0, "stock": 5},
    "2": {"nombre": "Filtro Cilíndrico Industrial", "precio": 120.0, "stock": 12},
    "3": {"nombre": "Válvula de Comporta 1/2", "precio": 85.0, "stock": 8},
    "4": {"nombre": "Tubería de Cobre 3/4", "precio": 110.0, "stock": 15}
}

def obtener_fecha_hora():
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d"), ahora.strftime("%H:%M:%S")

# ==========================================
# 5 FUNCIONES PENDIENTES DE IMPLEMENTAR
# ==========================================

# --- piero (2 Funciones) ---
def capturar_datos_cliente():
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    print("\n[Aviso] Función capturar_datos_cliente pendiente.")
    return "Cliente Temporal", "999999999", "correo@ejemplo.com", "Boleta", "12345678"

def servicio_mantenimiento(comprobantes):
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    print("\n[Aviso] Servicio de mantenimiento pendiente.")

# --- franklin (2 Funciones) ---
def buscar_comprobantes(comprobantes):
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    print("\n[Aviso] Búsqueda de comprobantes pendiente.")

def configurar_catalogos():
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    print("\n[Aviso] Configuración de precios pendiente.")

# --- valentino  (1 Función / Persistencia) ---
def cargar_comprobantes():
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    print("[Aviso] Carga de archivos pendiente.")
    return []

def guardar_comprobantes(comprobantes):
    # TODO: PENDIENTE DE IMPLEMENTACIÓN
    pass


# ==========================================
# FUNCIONES YA INTEGRADAS
# ==========================================
def servicio_construccion(comprobantes):
    print("\n=== SERVICIO DE CONSTRUCCIÓN ===")
    cliente, telefono, correo, tipo_comp, documento = capturar_datos_cliente()
    area = float(input("\nLargo (m): ")) * float(input("Ancho (m): "))
    acabado = "Premium" if input("Acabado (1. Básico | 2. Premium): ").strip() == "2" else "Básico"
    for k, v in PRECIO_MANO_OBRA.items(): print(f"{k}. {v['nombre']} - S/ {v['costo_dia']:.2f}/día")
    opc = input("Cuadrilla (1-3): ").strip()
    while opc not in PRECIO_MANO_OBRA: opc = input(" [Error] Opción 1-3: ").strip()
    monto = (area * PRECIO_CONSTRUCCION[acabado]) + (PRECIO_MANO_OBRA[opc]["costo_dia"] * int(input("Días: ")))
    fecha, hora = obtener_fecha_hora()
    nro_comp = f"B001-{len(comprobantes)+1:06d}"
    comprobantes.append({"nro_comp": nro_comp, "tipo_comp": tipo_comp, "cliente": cliente, "documento": documento, "telefono": telefono, "servicio": f"Construcción {acabado} ({area:.1f}m²)", "monto": monto, "fecha": fecha, "hora": hora})
    guardar_comprobantes(comprobantes)
    print(f"\n[Éxito] {nro_comp} generado | Total: S/ {monto:,.2f}")

def servicio_suministro(comprobantes):
    print("\n=== SERVICIO DE SUMINISTRO ===")
    cliente, telefono, correo, tipo_comp, documento = capturar_datos_cliente()
    for k, v in CATALOGO_MATERIALES.items(): print(f"{k}. {v['nombre']} - S/ {v['precio']:.2f} (Stock: {v['stock']})")
    monto, items = 0.0, []
    while True:
        sel = input("\nProducto (0 para terminar): ").strip()
        if sel == "0": break
        if sel in CATALOGO_MATERIALES and CATALOGO_MATERIALES[sel]["stock"] > 0:
            cant = int(input(f"Cantidad: "))
            if cant <= CATALOGO_MATERIALES[sel]["stock"]:
                CATALOGO_MATERIALES[sel]["stock"] -= cant
                monto += cant * CATALOGO_MATERIALES[sel]["precio"]
                items.append(f"{cant}x {CATALOGO_MATERIALES[sel]['nombre']}")
            else: print(" [Error] Stock insuficiente.")
    if monto > 0:
        fecha, hora = obtener_fecha_hora()
        nro_comp = f"B001-{len(comprobantes)+1:06d}"
        comprobantes.append({"nro_comp": nro_comp, "tipo_comp": tipo_comp, "cliente": cliente, "documento": documento, "telefono": telefono, "servicio": "Suministro: " + ", ".join(items), "monto": monto, "fecha": fecha, "hora": hora})
        guardar_comprobantes(comprobantes)
        print(f"\n[Éxito] {nro_comp} generado | Total: S/ {monto:,.2f}")

def reporte_ventas(comprobantes):
    if not comprobantes: return print("\n [Aviso] No hay ventas.")
    filtro = input("Fecha a filtrar (AAAA-MM-DD o ENTER para todos): ").strip()
    filtrados = [c for c in comprobantes if not filtro or c["fecha"] == filtro]
    print("\n" + "-"*55 + f"\n{'NRO':<12} | {'FECHA':<10} | {'CLIENTE':<15} | {'MONTO':<10}\n" + "-"*55)
    for c in filtrados: print(f"{c['nro_comp']:<12} | {c['fecha']:<10} | {c['cliente'][:15]:<15} | S/ {c['monto']:>7,.2f}")
    print("-"*55 + f"\nTOTAL RECAUDADO: S/ {sum(c['monto'] for c in filtrados):,.2f}")

# ==========================================
# MENÚ PRINCIPAL
# ==========================================
def main():
    comprobantes = cargar_comprobantes()

    while True:
        print("\n" + "=" * 52)
        print("         DH PROYECTOS CONTRATISTAS - BLUESYNC      ")
        print("                    MENÚ PRINCIPAL                 ")
        print("=" * 52)
        print(" 1. Servicio de construcción")
        print(" 2. Servicio de mantenimiento")
        print(" 3. Servicio de suministro de materiales")
        print(" 4. Configurar catálogos y precios")
        print(" 5. Buscar historial de comprobantes")
        print(" 6. Reportes de Ventas")
        print(" 7. Salir")
        print("=" * 52)

        opcion = input("Seleccione una opción (1-7): ").strip()

        if opcion == "1":
            servicio_construccion(comprobantes)
        elif opcion == "2":
            servicio_mantenimiento(comprobantes)
        elif opcion == "3":
            servicio_suministro(comprobantes)
        elif opcion == "4":
            configurar_catalogos()
        elif opcion == "5":
            buscar_comprobantes(comprobantes)
        elif opcion == "6":
            reporte_ventas(comprobantes)
        elif opcion == "7":
            guardar_comprobantes(comprobantes)
            print("\n  ¡Gracias por utilizar el sistema BlueSync!")
            break
        else:
            print("  [Error] Opción no válida.")

if __name__ == "__main__":
    main()