"""
SISTEMA DIGITAL DH PROYECTOS Y CONTRATISTAS S.A.C. - BLUESYNC
Nivel: Fundamentos de Programación (2do Ciclo)
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
# ==========================================
# 1. VALIDACIONES Y CAPTURA DE DATOS DEL CLIENTE
# ==========================================
def obtener_fecha_hora():
    ahora = datetime.now()
    return ahora.strftime("%Y-%m-%d"), ahora.strftime("%H:%M:%S")

def capturar_datos_cliente():
    print("\n--- DATOS DEL CLIENTE ---")

    # 1. Nombre completo
    cliente = input("Nombre completo: ").strip().title()
    while not cliente.replace(" ", "").isalpha():
        cliente = input("  [Error] Ingrese un nombre válido (solo letras): ").strip().title()

    # 2. Teléfono
    telefono = input("Teléfono: ").strip()
    while not (telefono.isdigit() and len(telefono) == 9):
        telefono = input("  [Error] Ingrese un teléfono válido (9 dígitos): ").strip()

    # 3. Correo electrónico
    correo = input("Correo electrónico: ").strip().lower()
    dominios = ("@gmail.com", "@hotmail.com", "@outlook.com", "@yahoo.com", ".com", ".pe")
    while "@" not in correo or " " in correo or not correo.endswith(dominios):
        correo = input("  [Error] Ingrese correo válido (@gmail.com, @hotmail.com, etc): ").strip().lower()

    # 4. Tipo de Comprobante
    print("\nTipo de Comprobante: 1. Boleta | 2. Factura")
    tipo_sel = input("Seleccione (1-2): ").strip()
    while tipo_sel not in ["1", "2"]:
        tipo_sel = input("  [Error] Seleccione 1 o 2: ").strip()

    tipo_comp = "Factura" if tipo_sel == "2" else "Boleta"

   # 5. Documento según comprobante
    if tipo_comp == "Factura":
        documento = input("Ingrese RUC (11 dígitos): ").strip()
        while not (documento.isdigit() and len(documento) == 11):
            documento = input("  [Error] Ingrese un RUC válido (11 dígitos): ").strip()
    else:
        documento = input("Ingrese DNI (8 dígitos): ").strip()
        while not (documento.isdigit() and len(documento) == 8):
            documento = input("  [Error] Ingrese un DNI válido (8 dígitos): ").strip()
    return cliente, telefono, correo, tipo_comp, documento
# ==========================================
# 2. PERSISTENCIA DE DATOS (ARCHIVOS)
# ==========================================
def cargar_comprobantes():
    comprobantes = []
    if not os.path.exists(NOMBRE_ARCHIVO):
        return comprobantes

    with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            c = linea.strip().split("|")
            if len(c) == 9:
                comprobantes.append({
                    "nro_comp": c[0], "tipo_comp": c[1], "cliente": c[2],
                    "documento": c[3], "telefono": c[4], "servicio": c[5],
                    "monto": float(c[6]), "fecha": c[7], "hora": c[8]
                })
    return comprobantes

def guardar_comprobantes(comprobantes):
    with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
        for c in comprobantes:
            linea = f"{c['nro_comp']}|{c['tipo_comp']}|{c['cliente']}|{c['documento']}|{c['telefono']}|{c['servicio']}|{c['monto']:.2f}|{c['fecha']}|{c['hora']}\n"
            archivo.write(linea)
# ==========================================
# 3. SERVICIOS DEL SISTEMA
# ==========================================
def servicio_construccion(comprobantes):
    print("\n==================================================")
    print("      1. SERVICIO DE CONSTRUCCIÓN DE PISCINAS      ")
    print("==================================================")
    cliente, telefono, correo, tipo_comp, documento = capturar_datos_cliente()

    print("\n--- REQUERIMIENTOS DEL SERVICIO ---")
    largo = float(input("Largo (m): "))
    ancho = float(input("Ancho (m): "))
    area = largo * ancho

    print("\nSeleccione Tipo de Acabado:")
    print(f"1. Básico (S/ {PRECIO_CONSTRUCCION['Básico']:.2f} x m²)")
    print(f"2. Premium (S/ {PRECIO_CONSTRUCCION['Premium']:.2f} x m²)")
    opc_acabado = input("Opción (1-2): ").strip()

    acabado_nombre = "Premium" if opc_acabado == "2" else "Básico"
    costo_material = area * PRECIO_CONSTRUCCION[acabado_nombre]

    print("\n--- SELECCIÓN DE MANO DE OBRA ---")
    for k, v in PRECIO_MANO_OBRA.items():
        print(f"{k}. {v['nombre']} - S/ {v['costo_dia']:.2f} por día")

    opc_mo = input("Seleccione cuadrilla (1-3): ").strip()
    while opc_mo not in ["1", "2", "3"]:
        opc_mo = input("  [Error] Ingrese opción 1, 2 o 3: ").strip()

    cuadrilla = PRECIO_MANO_OBRA[opc_mo]
    dias = int(input("Días estimados de construcción: "))
    costo_mo = cuadrilla["costo_dia"] * dias

    monto_total = costo_material + costo_mo
    fecha, hora = obtener_fecha_hora()
    nro_comp = f"B001-{len(comprobantes)+1:06d}"
    detalle = f"Construcción {acabado_nombre} ({area:.1f}m²)"

    nuevo = {
        "nro_comp": nro_comp, "tipo_comp": tipo_comp, "cliente": cliente,
        "documento": documento, "telefono": telefono, "servicio": detalle,
        "monto": monto_total, "fecha": fecha, "hora": hora
    }
    comprobantes.append(nuevo)
    guardar_comprobantes(comprobantes)
    print(f"\n[Éxito] Comprobante {nro_comp} generado el {fecha} a las {hora}")
    print(f"        Total a pagar: S/ {monto_total:,.2f}")

def servicio_mantenimiento(comprobantes):
    print("\n==================================================")
    print("      2. SERVICIO DE MANTENIMIENTO DE PISCINAS    ")
    print("==================================================")
    cliente, telefono, correo, tipo_comp, documento = capturar_datos_cliente()

    print("\n--- REQUERIMIENTOS DEL SERVICIO ---")
    horas = float(input("Horas de trabajo: "))
    costo_base = horas * PRECIO_MANTENIMIENTO["Tarifa Hora"]

    incluir = input(f"¿Incluir Kit de Químicos (S/ {PRECIO_MANTENIMIENTO['Kit Quimicos']:.2f})? (S/N): ").strip().upper()
    costo_kit = PRECIO_MANTENIMIENTO["Kit Quimicos"] if incluir == "S" else 0.0

    monto_total = costo_base + costo_kit
    fecha, hora = obtener_fecha_hora()
    nro_comp = f"B001-{len(comprobantes)+1:06d}"
    detalle = f"Mantenimiento ({horas:.0f} hrs)"

    nuevo = {
        "nro_comp": nro_comp, "tipo_comp": tipo_comp, "cliente": cliente,
        "documento": documento, "telefono": telefono, "servicio": detalle,
        "monto": monto_total, "fecha": fecha, "hora": hora
    }
    comprobantes.append(nuevo)
    guardar_comprobantes(comprobantes)
    print(f"\n[Éxito] Comprobante {nro_comp} generado el {fecha} a las {hora}")
    print(f"        Total a pagar: S/ {monto_total:,.2f}")


def servicio_suministro(comprobantes):
    print("\n==================================================")
    print("      3. SERVICIO DE SUMINISTRO DE MATERIALES     ")
    print("==================================================")
    cliente, telefono, correo, tipo_comp, documento = capturar_datos_cliente()

    print("\n--- CATÁLOGO DE MATERIALES ---")
    for k, v in CATALOGO_MATERIALES.items():
        print(f"{k}. {v['nombre']} - S/ {v['precio']:.2f} (Stock: {v['stock']})")

    monto_total = 0.0
    items_comprados = []
    ##empieza a comprar los sumistros
    while True:
        sel = input("\nSeleccione producto a comprar (0 para finalizar): ").strip()
        if sel == "0":
            break

        if sel in CATALOGO_MATERIALES:
            prod = CATALOGO_MATERIALES[sel]
            if prod["stock"] <= 0:
                print("  [Aviso] Producto sin stock disponible.")
                continue

            cant = int(input(f"Cantidad para '{prod['nombre']}': "))
            if cant > prod["stock"]:
                print(f"  [Error] Solo quedan {prod['stock']} unidades.")
                continue

            prod["stock"] -= cant
            subtotal = cant * prod["precio"]
            monto_total += subtotal
            items_comprados.append(f"{cant}x {prod['nombre']}")
            print(f"  -> Añadido: Subtotal S/ {subtotal:.2f}")
        else:
            print("  [Error] Opción no válida.")
##cosas compradas
    if monto_total > 0:
        fecha, hora = obtener_fecha_hora()
        nro_comp = f"B001-{len(comprobantes)+1:06d}"
        detalle = "Suministro: " + ", ".join(items_comprados)
        nuevo = {
            "nro_comp": nro_comp, "tipo_comp": tipo_comp, "cliente": cliente,
            "documento": documento, "telefono": telefono, "servicio": detalle,
            "monto": monto_total, "fecha": fecha, "hora": hora
        }
        comprobantes.append(nuevo)
        guardar_comprobantes(comprobantes)
        print(f"\n[Éxito] Comprobante {nro_comp} generado el {fecha} a las {hora}")
        print(f"        Total a pagar: S/ {monto_total:,.2f}")
# ==========================================
# 4. CONFIGURACIÓN DE PRECIOS SIMPLIFICADA
# ==========================================
def configurar_catalogos():
    print("\n--------------------------------------------------")
    print("       GESTOR DE PRECIOS DEL SISTEMA              ")
    print("--------------------------------------------------")
    print("1. Cambiar precio acabado Básico")
    print("2. Cambiar tarifa por hora de mantenimiento")
    print("3. Cambiar precio Kit de Químicos")
    print("4. Regresar")

    opc = input("Seleccione (1-4): ").strip()

    if opc == "1":
        nuevo_p = float(input("Nuevo precio x m² para Acabado Básico: S/ "))
        PRECIO_CONSTRUCCION["Básico"] = nuevo_p
        print("  [Éxito] Precio actualizado.")
    elif opc == "2":
        nuevo_p = float(input("Nueva tarifa por hora: S/ "))
        PRECIO_MANTENIMIENTO["Tarifa Hora"] = nuevo_p
        print("  [Éxito] Tarifa actualizada.")
    elif opc == "3":
        nuevo_p = float(input("Nuevo precio Kit de Químicos: S/ "))
        PRECIO_MANTENIMIENTO["Kit Quimicos"] = nuevo_p
        print("  [Éxito] Precio actualizado.")
# ==========================================
# 5. BÚSQUEDA Y REPORTES FÁCILES
# ==========================================
def buscar_comprobantes(comprobantes):
    print("\n--------------------------------------------------")
    print("         BUSCADOR DE COMPROBANTES EMITIDOS        ")
    print("--------------------------------------------------")
    doc_buscar = input("Ingrese DNI o RUC a buscar: ").strip()
    encontrados = False
    for c in comprobantes:
        if c["documento"] == doc_buscar:
            encontrados = True
            #impresion de los comprobantes encontrados
            print("=" * 50)
            print(f" Nro:     {c['nro_comp']} ({c['tipo_comp']})")
            print(f" Fecha:   {c['fecha']} - {c['hora']}")
            print(f" Cliente: {c['cliente']} | Doc: {c['documento']}")
            print(f" Detalle: {c['servicio']}")
            print(f" Monto:   S/ {c['monto']:,.2f}")
            print("=" * 50)
    if not encontrados:
        print(f"  [Aviso] No hay registros para '{doc_buscar}'.")

def reporte_ventas(comprobantes):
    print("\n--------------------------------------------------")
    print("                REPORTE DE VENTAS                 ")
    print("--------------------------------------------------")
    if not comprobantes:
        print("  No hay ventas registradas.")
        return

    print("1. Ver todas las ventas")
    print("2. Filtrar ventas por fecha (AAAA-MM-DD)")
    opc = input("Seleccione (1-2): ").strip()

    fecha_filtro = ""
    if opc == "2":
        fecha_filtro = input("Ingrese fecha (Ejemplo: 2026-09-28): ").strip()
#impresion de los comprobantes, los numeros son  el ancho fijo de caracteres de las columnas
    total_recaudado = 0.0
    print("\n" + "-" * 60)
    print(f"{'NRO':<12} | {'FECHA':<10} | {'CLIENTE':<15} | {'MONTO':<10}")
    print("-" * 60)

    for c in comprobantes:
        if fecha_filtro == "" or c["fecha"] == fecha_filtro:
            print(f"{c['nro_comp']:<12} | {c['fecha']:<10} | {c['cliente'][:15]:<15} | S/ {c['monto']:>7,.2f}")
            total_recaudado += c["monto"]

    print("-" * 60)
    print(f"TOTAL RECAUDADO: S/ {total_recaudado:,.2f}")
# ==========================================
# 6. MENÚ PRINCIPAL
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