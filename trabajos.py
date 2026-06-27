import datos
import validaciones
import cobros


def asignarTrabajo():
    if len(datos.listaClientes) == 0:
        print("no hay clientes registrados, cargue uno primero")
        return

    print("=== clientes registrados ===")
    for i in range(len(datos.listaClientes)):
        print(str(i + 1) + " - " + datos.listaClientes[i]["nombre"] + " | " + datos.listaClientes[i]["direccion"])

    opcionCliente = int(input("selecciona el numero del cliente: "))
    while opcionCliente < 1 or opcionCliente > len(datos.listaClientes):
        opcionCliente = int(input("opcion invalida, elegi de nuevo: "))

    clienteSeleccionado = datos.listaClientes[opcionCliente - 1]
    clientePorAtender = clienteSeleccionado["nombre"]
    direccionAVisitar = clienteSeleccionado["direccion"]
    print("cliente seleccionado: " + clientePorAtender + " | " + direccionAVisitar)

    # descripcion en texto libre (ej: "perdida de agua en el equipo del living")
    trabajoARealizar = input("describi el trabajo a realizar: ")
    while trabajoARealizar == "":
        trabajoARealizar = input("el trabajo no puede estar vacio: ")

    if len(datos.listaTecnicos) == 0:
        print("no hay tecnicos registrados, cargue uno primero")
        return

    print("=== tecnicos disponibles ===")
    for i in range(len(datos.listaTecnicos)):
        print(str(i + 1) + " - " + datos.listaTecnicos[i]["nombre"] + " | " + datos.listaTecnicos[i]["especialidad"])

    opcionTecnico = int(input("selecciona el numero del tecnico: "))
    while opcionTecnico < 1 or opcionTecnico > len(datos.listaTecnicos):
        opcionTecnico = int(input("opcion invalida, elegi de nuevo: "))

    nombreDelTecnico = datos.listaTecnicos[opcionTecnico - 1]["nombre"]
    print("tecnico seleccionado: " + nombreDelTecnico)

    horarioDeVisita = input("ingrese el horario de la visita (HH:MM): ")
    while not validaciones.horaValida(horarioDeVisita):
        horarioDeVisita = input("formato invalido, ingrese la hora asi (HH:MM): ")

    fecha = input("ingrese la fecha del trabajo (DD/MM/AAAA): ")
    while not validaciones.fechaValida(fecha):
        fecha = input("formato invalido, ingrese la fecha asi (DD/MM/AAAA): ")

    detalles = input("ingrese algun detalle o descripcion en caso de desearlo: ")

    precio = input("ingrese el precio del trabajo (o Enter si todavia no sabe): ")
    precio = int(precio) if precio.isdigit() else 0

    nuevoTrabajo = {
        "clientePorAtender": clientePorAtender,
        "direccionAVisitar": direccionAVisitar,
        "trabajoARealizar": trabajoARealizar,
        "nombreDelTecnico": nombreDelTecnico,
        "horarioDeVisita": horarioDeVisita,
        "fecha": fecha,
        "detalles": detalles,
        "estado": "pendiente",
        "precio": precio,
        "pagado": 0,
        "pagos": [],
    }

    datos.listaTrabajos.append(nuevoTrabajo)
    datos.guardarTrabajos()
    print("trabajo asignado con exito!")


def cambioEstadoTrabajo():
    direccionBuscada = input("ingrese la direccion del cliente: ")
    indice = None

    for i in range(len(datos.listaTrabajos)):
        if datos.listaTrabajos[i]["direccionAVisitar"].lower() == direccionBuscada.lower():
            indice = i
            break

    if indice is None:
        print("no se encontro ningun trabajo para esa direccion")
        return

    t = datos.listaTrabajos[indice]
    print("trabajo encontrado: " + t["trabajoARealizar"] + " | cliente: " + t["clientePorAtender"] + " | estado actual: " + t["estado"])

    print("estados disponibles:")
    for i in range(len(datos.ESTADOS_TRABAJO)):
        print(str(i + 1) + " - " + datos.ESTADOS_TRABAJO[i])

    opcion = int(input("elegi el nuevo estado: "))
    while opcion < 1 or opcion > len(datos.ESTADOS_TRABAJO):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    nuevoEstado = datos.ESTADOS_TRABAJO[opcion - 1]
    t["estado"] = nuevoEstado
    datos.guardarTrabajos()
    print("estado actualizado a: " + nuevoEstado)

    # si paso a cobrado, registramos el pago
    if nuevoEstado == "cobrado":
        cobros.registrarPago(t)


def mostrarUnTrabajo(t):
    print("  cliente: " + t["clientePorAtender"])
    print("  direccion: " + t["direccionAVisitar"])
    print("  tarea: " + t["trabajoARealizar"])
    print("  tecnico: " + t["nombreDelTecnico"])
    print("  fecha: " + t["fecha"] + " | hora: " + t["horarioDeVisita"])
    print("  estado: " + t["estado"])
    if t["detalles"] != "":
        print("  detalles: " + t["detalles"])
    deuda = cobros.saldoDeudor(t)
    print("  precio: $" + str(t["precio"]) + " | pagado: $" + str(t["pagado"]) + " | debe: $" + str(deuda))
    for p in t["pagos"]:
        print("    pago: $" + str(p["monto"]) + " el " + p["fecha"])
    print("  ---")


def mostrarTrabajos():
    if len(datos.listaTrabajos) == 0:
        print("no hay trabajos cargados")
        return
    print("=== todos los trabajos (" + str(len(datos.listaTrabajos)) + ") ===")
    for t in datos.listaTrabajos:
        mostrarUnTrabajo(t)


def trabajosPendientes():
    encontrados = list(filter(lambda t: t["estado"] in ("pendiente", "en curso"), datos.listaTrabajos))

    if len(encontrados) == 0:
        print("no hay trabajos pendientes, estan todos al dia :)")
        return

    print("=== trabajos pendientes (" + str(len(encontrados)) + ") ===")
    for t in encontrados:
        mostrarUnTrabajo(t)


def trabajosRealizados():
    encontrados = list(filter(lambda t: t["estado"] in ("finalizado", "cobrado"), datos.listaTrabajos))

    if len(encontrados) == 0:
        print("todavia no hay trabajos realizados")
        return

    print("=== trabajos realizados (" + str(len(encontrados)) + ") ===")
    for t in encontrados:
        mostrarUnTrabajo(t)
