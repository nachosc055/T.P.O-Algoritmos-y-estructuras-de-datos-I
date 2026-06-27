import datos
import validaciones


def saldoDeudor(trabajo):
    saldo = trabajo["precio"] - trabajo["pagado"]
    return saldo if saldo > 0 else 0


def estadoDePago(trabajo):
    if trabajo["pagado"] <= 0:
        return "pendiente"
    if trabajo["pagado"] < trabajo["precio"]:
        return "pago parcial"
    return "pagado"


def deudaPorCliente():
    # Devuelve un diccionario {cliente: deuda_total} solo de los que deben
    deudas = {}
    for t in datos.listaTrabajos:
        saldo = saldoDeudor(t)
        if saldo > 0:
            cliente = t["clientePorAtender"]
            deudas[cliente] = deudas.get(cliente, 0) + saldo
    return deudas


def registrarPago(trabajo):
    if trabajo["precio"] <= 0:
        print("este trabajo todavia no tiene precio cargado. cargalo primero desde el menu")
        return

    montoPago = input("cuanto pago el cliente? (precio total: $" + str(trabajo["precio"]) + "): ")
    while not montoPago.isdigit():
        montoPago = input("ingresa un numero valido: ")

    fechaPago = input("fecha del pago (DD/MM/AAAA): ")
    while not validaciones.fechaValida(fechaPago):
        fechaPago = input("formato invalido, ingrese la fecha asi (DD/MM/AAAA): ")

    trabajo["pagos"].append({"monto": int(montoPago), "fecha": fechaPago})
    trabajo["pagado"] += int(montoPago)
    datos.guardarTrabajos()

    saldo = saldoDeudor(trabajo)
    if saldo > 0:
        print("pago parcial registrado. todavia debe: $" + str(saldo))
    else:
        print("pago completo! no debe nada :)")


def cargarPrecio():
    if len(datos.listaTrabajos) == 0:
        print("no hay trabajos cargados")
        return

    print("=== trabajos ===")
    for i in range(len(datos.listaTrabajos)):
        t = datos.listaTrabajos[i]
        print(str(i + 1) + " - " + t["clientePorAtender"] + " | " + t["trabajoARealizar"] +
              " | precio actual: $" + str(t["precio"]))

    opcion = int(input("selecciona el numero del trabajo: "))
    while opcion < 1 or opcion > len(datos.listaTrabajos):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    trabajo = datos.listaTrabajos[opcion - 1]
    nuevoPrecio = input("ingrese el precio del trabajo: ")
    while not nuevoPrecio.isdigit():
        nuevoPrecio = input("ingresa un numero valido: ")

    trabajo["precio"] = int(nuevoPrecio)
    datos.guardarTrabajos()
    print("precio actualizado a: $" + str(trabajo["precio"]))


def registrarCobro():
    if len(datos.listaTrabajos) == 0:
        print("no hay trabajos cargados")
        return

    print("=== trabajos ===")
    for i in range(len(datos.listaTrabajos)):
        t = datos.listaTrabajos[i]
        print(str(i + 1) + " - " + t["clientePorAtender"] + " | " + t["trabajoARealizar"] +
              " | estado de pago: " + estadoDePago(t) + " | saldo: $" + str(saldoDeudor(t)))

    opcion = int(input("selecciona el numero del trabajo a cobrar: "))
    while opcion < 1 or opcion > len(datos.listaTrabajos):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    registrarPago(datos.listaTrabajos[opcion - 1])
