import datos


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
    # Pide el monto cobrado, lo suma a lo pagado y muestra el saldo restante
    montoPago = input("cuanto pago el cliente? (precio total: $" + str(trabajo["precio"]) + "): ")
    while not montoPago.isdigit():
        montoPago = input("ingresa un numero valido: ")

    trabajo["pagado"] += int(montoPago)
    datos.guardarTrabajos()

    saldo = saldoDeudor(trabajo)
    if saldo > 0:
        print("pago parcial registrado. todavia debe: $" + str(saldo))
    else:
        print("pago completo! no debe nada :)")


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
