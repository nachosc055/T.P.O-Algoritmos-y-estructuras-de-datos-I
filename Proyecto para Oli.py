import os
import json

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CLIENTES = os.path.join(RUTA_BASE, "clientes.json")
RUTA_TRABAJADORES = os.path.join(RUTA_BASE, "trabajadores.json")

listaClientes = []

listaTrabajadores = []

listaDeTrabajosPendientes = []
listaDeTrabajosTerminados = []

def cargarClientes():
    global listaClientes
    if os.path.exists(RUTA_CLIENTES):
        try:
            with open(RUTA_CLIENTES, "r", encoding="utf-8") as archivo:
                listaClientes = json.load(archivo)
        except Exception as e:
            print("ocurrio un error al cargar clientes.json, se usaran los datos por defecto:", e)
    else:
        # primera vez que se corre el programa: crea el archivo con los clientes de ejemplo
        guardarClientes()


def guardarClientes():
    try:
        with open(RUTA_CLIENTES, "w", encoding="utf-8") as archivo:
            json.dump(listaClientes, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print("ocurrio un error al guardar clientes.json:", e)


def cargarTrabajadores():
    global listaTrabajadores
    if os.path.exists(RUTA_TRABAJADORES):
        try:
            with open(RUTA_TRABAJADORES, "r", encoding="utf-8") as archivo:
                listaTrabajadores = json.load(archivo)
        except Exception as e:
            print("ocurrio un error al cargar trabajadores.json, se usaran los datos por defecto:", e)
    else:
        # primera vez que se corre el programa: crea el archivo con los trabajadores de ejemplo
        guardarTrabajadores()


def guardarTrabajadores():
    try:
        with open(RUTA_TRABAJADORES, "w", encoding="utf-8") as archivo:
            json.dump(listaTrabajadores, archivo, indent=4, ensure_ascii=False)
    except Exception as e:
        print("ocurrio un error al guardar trabajadores.json:", e)

def cargaDeDatosCliente():
    idCliente = 0
    if len(listaClientes) == 0:
        idCliente = 0
    else:
        idMaximo = listaClientes[-1]["idCliente"]
        idCliente = idMaximo + 1

    nombreCliente = input("ingrese el nombre del cliente: ")
    while nombreCliente == "":
        nombreCliente = input("el nombre no puede estar vacio: ")

    direccionCliente = input("ingrese la direccion del cliente: ")
    while direccionCliente == "":
        direccionCliente = input("la direccion no puede estar vacia: ")

    telefonoCliente = input("ingrese el numero del cliente: ")
    while telefonoCliente == "":
        telefonoCliente = input("el telefono no puede estar vacio: ")

    nuevoCliente = {
        "idCliente": idCliente,
        "nombre": nombreCliente,
        "direccion": direccionCliente,
        "telefono": telefonoCliente,
    }

    listaClientes.append(nuevoCliente)
    guardarClientes()
    print("cliente creado con exito :)")


def cargaDatosTrabajador():
    idTrabajador = 0
    if len(listaTrabajadores) == 0:
        idTrabajador = 0
    else:
        idMaximo = listaTrabajadores[-1]["idTrabajador"]
        idTrabajador = idMaximo + 1

    nombreTrabajador = input("ingrese el nombre del trabajador: ")
    while nombreTrabajador == "" or nombreTrabajador.isdigit():
        nombreTrabajador = input("el nombre no puede estar vacio ni ser un numero: ")

    especialidad = input("ingrese la especialidad del trabajador (ej: electricidad, herreria): ")
    while especialidad == "":
        especialidad = input("la especialidad no puede estar vacia: ")

    nuevoTrabajador = {
        "idTrabajador": idTrabajador,
        "nombre": nombreTrabajador,
        "especialidad": especialidad,
    }

    listaTrabajadores.append(nuevoTrabajador)
    guardarTrabajadores()
    print("trabajador cargado con exito :)")


def eliminarTrabajador():
    if len(listaTrabajadores) == 0:
        print("no hay trabajadores registrados")
        return

    print("=== trabajadores registrados ===")
    for i in range(len(listaTrabajadores)):
        print(str(i+1) + " - " + listaTrabajadores[i]["nombre"] + " | " + listaTrabajadores[i]["especialidad"])

    opcion = int(input("selecciona el numero del trabajador a eliminar (0 para cancelar): "))
    while opcion < 0 or opcion > len(listaTrabajadores):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    if opcion == 0:
        print("operacion cancelada")
        return

    trabajadorEliminado = listaTrabajadores.pop(opcion - 1)
    guardarTrabajadores()
    print("trabajador eliminado: " + trabajadorEliminado["nombre"])


def buscarCliente():
    clienteABuscar = input("ingrese el nombre del cliente a buscar: ")
    coincidencia = False
    indice = None
    for i in range(len(listaClientes)):
        if clienteABuscar == listaClientes[i]["nombre"]:
            coincidencia = True
            indice = i
            print("cliente encontrado: " + listaClientes[i]["nombre"] + " | " + listaClientes[i]["direccion"])
    if not coincidencia:
        print("cliente no encontrado, volviendo al menu...")
    return indice


def asignarTrabajo():
    if len(listaClientes) == 0:
        print("no hay clientes registrados, cargue uno primero")
        return

    print("=== clientes registrados ===")
    for i in range(len(listaClientes)):
        print(str(i+1) + " - " + listaClientes[i]["nombre"] + " | " + listaClientes[i]["direccion"])

    opcionCliente = int(input("selecciona el numero del cliente: "))
    while opcionCliente < 1 or opcionCliente > len(listaClientes):
        opcionCliente = int(input("opcion invalida, elegi de nuevo: "))

    clienteSeleccionado = listaClientes[opcionCliente - 1]
    clientePorAtender = clienteSeleccionado["nombre"]
    direccionAVisitar = clienteSeleccionado["direccion"]
    print("cliente seleccionado: " + clientePorAtender + " | " + direccionAVisitar)

    trabajoARealizar = input("ingrese el trabajo hay que realizarle al cliente: ")
    while trabajoARealizar == "":
        trabajoARealizar = input("el trabajo no puede estar vacio: ")

    if len(listaTrabajadores) == 0:
        print("no hay trabajadores registrados, cargue uno primero")
        return

    print("=== trabajadores disponibles ===")
    for i in range(len(listaTrabajadores)):
        print(str(i+1) + " - " + listaTrabajadores[i]["nombre"] + " | " + listaTrabajadores[i]["especialidad"])

    opcionTrabajador = int(input("selecciona el numero del trabajador: "))
    while opcionTrabajador < 1 or opcionTrabajador > len(listaTrabajadores):
        opcionTrabajador = int(input("opcion invalida, elegi de nuevo: "))

    nombreDelTrabajador = listaTrabajadores[opcionTrabajador - 1]["nombre"]
    print("trabajador seleccionado: " + nombreDelTrabajador)

    horarioDeVisita = input("ingrese el horario de la visita (HH:MM): ")
    while True:
        try:
            partes = horarioDeVisita.split(":")
            if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
                raise ValueError
            if int(partes[0]) > 23 or int(partes[1]) > 59:
                raise ValueError
            break
        except ValueError:
            horarioDeVisita = input("formato invalido, ingrese la hora asi (HH:MM): ")

    fecha = input("ingrese la fecha del trabajo (DD/MM/AAAA): ")
    while "/" not in fecha or len(fecha) != 10:
        fecha = input("formato invalido, ingrese la fecha asi (DD/MM/AAAA): ")

    detalles = input("ingrese algun detalle o descripcion en caso de desearlo: ")

    precio = input("ingrese el precio del trabajo (o Enter si todavia no sabe): ")
    precio = int(precio) if precio.isdigit() else 0

    nuevoTrabajo = {
        "clientePorAtender": clientePorAtender,
        "direccionAVisitar": direccionAVisitar,
        "trabajoARealizar": trabajoARealizar,
        "nombreDelTrabajador": nombreDelTrabajador,
        "horarioDeVisita": horarioDeVisita,
        "fecha": fecha,
        "detalles": detalles,
        "estado": "pendiente",
        "precio": precio,
        "pagado": 0,
    }

    listaDeTrabajosPendientes.append(nuevoTrabajo)
    print("trabajo asignado con exito!")


def cambioEstadoTrabajo():
    nombreBuscado = input("ingrese el nombre del cliente: ")
    indice = None

    for i in range(len(listaDeTrabajosPendientes)):
        if listaDeTrabajosPendientes[i]["clientePorAtender"].lower() == nombreBuscado.lower():
            indice = i
            break

    if indice == None:
        print("no se encontro ningun trabajo para ese cliente")
        return

    t = listaDeTrabajosPendientes[indice]
    print("trabajo encontrado: " + t["trabajoARealizar"] + " | estado actual: " + t["estado"])

    estadosTrabajo = ["pendiente", "en proceso", "terminado", "cobrado"]
    print("estados disponibles:")
    for i in range(len(estadosTrabajo)):
        print(str(i+1) + " - " + estadosTrabajo[i])

    opcion = int(input("elegi el nuevo estado: "))
    while opcion < 1 or opcion > len(estadosTrabajo):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    listaDeTrabajosPendientes[indice]["estado"] = estadosTrabajo[opcion - 1]
    print("estado actualizado a: " + estadosTrabajo[opcion - 1])

    if estadosTrabajo[opcion - 1] == "cobrado":
        montoPago = input("cuanto pago el cliente? (precio total: $" + str(listaDeTrabajosPendientes[indice]["precio"]) + "): ")
        while not montoPago.isdigit():
            montoPago = input("ingresa un numero valido: ")
        listaDeTrabajosPendientes[indice]["pagado"] += int(montoPago)
        deuda = listaDeTrabajosPendientes[indice]["precio"] - listaDeTrabajosPendientes[indice]["pagado"]
        if deuda > 0:
            print("pago parcial registrado. todavia debe: $" + str(deuda))
        else:
            print("pago completo! no debe nada :)")


def trabajoDelDia():
    fecha = input("ingrese la fecha a consultar (DD/MM/AAAA): ")
    encontrados = []

    for trabajo in listaDeTrabajosPendientes:
        if trabajo["fecha"] == fecha:
            encontrados.append(trabajo)

    if len(encontrados) == 0:
        print("no hay trabajos para esa fecha")
        return

    print("=== trabajos para el " + fecha + ":")
    for t in encontrados:
        print("  tecnico: " + t["nombreDelTrabajador"])
        print("  cliente: " + t["clientePorAtender"])
        print("  tarea: " + t["trabajoARealizar"])
        print("  hora: " + str(t["horarioDeVisita"]))
        print("  ---")


def mostrarUnTrabajo(t):
    print("  cliente: " + t["clientePorAtender"])
    print("  direccion: " + t["direccionAVisitar"])
    print("  tarea: " + t["trabajoARealizar"])
    print("  tecnico: " + t["nombreDelTrabajador"])
    print("  fecha: " + t["fecha"] + " | hora: " + t["horarioDeVisita"])
    print("  estado: " + t["estado"])
    if t["detalles"] != "":
        print("  detalles: " + t["detalles"])
    deuda = t["precio"] - t["pagado"]
    print("  precio: $" + str(t["precio"]) + " | pagado: $" + str(t["pagado"]) + " | debe: $" + str(deuda))
    print("  ---")


def mostrarTrabajos():
    if len(listaDeTrabajosPendientes) == 0:
        print("no hay trabajos cargados")
        return
    print("=== todos los trabajos (" + str(len(listaDeTrabajosPendientes)) + ") ===")
    for t in listaDeTrabajosPendientes:
        mostrarUnTrabajo(t)


def trabajosPendientes():
    encontrados = []
    for t in listaDeTrabajosPendientes:
        if t["estado"] == "pendiente" or t["estado"] == "en proceso":
            encontrados.append(t)

    if len(encontrados) == 0:
        print("no hay trabajos pendientes, estan todos al dia :)")
        return

    print("=== trabajos pendientes (" + str(len(encontrados)) + ") ===")
    for t in encontrados:
        mostrarUnTrabajo(t)


def trabajosRealizados():
    encontrados = []
    for t in listaDeTrabajosPendientes:
        if t["estado"] == "terminado" or t["estado"] == "cobrado":
            encontrados.append(t)

    if len(encontrados) == 0:
        print("todavia no hay trabajos realizados")
        return

    print("=== trabajos realizados (" + str(len(encontrados)) + ") ===")
    for t in encontrados:
        mostrarUnTrabajo(t)


def trabajosTotales():
    total = len(listaDeTrabajosPendientes)
    if total == 0:
        print("no hay trabajos cargados")
        return

    pendientes = 0
    enProceso = 0
    terminados = 0
    cobrados = 0
    for t in listaDeTrabajosPendientes:
        if t["estado"] == "pendiente":
            pendientes += 1
        elif t["estado"] == "en proceso":
            enProceso += 1
        elif t["estado"] == "terminado":
            terminados += 1
        elif t["estado"] == "cobrado":
            cobrados += 1

    totalFacturado = sum(t["precio"] for t in listaDeTrabajosPendientes)
    totalCobrado = sum(t["pagado"] for t in listaDeTrabajosPendientes)
    totalDeuda = totalFacturado - totalCobrado

    print("=== resumen de trabajos ===")
    print("total de trabajos: " + str(total))
    print("  pendientes: " + str(pendientes))
    print("  en proceso: " + str(enProceso))
    print("  terminados: " + str(terminados))
    print("  cobrados: " + str(cobrados))
    print("  -------------------------")
    print("  total facturado: $" + str(totalFacturado))
    print("  total cobrado: $" + str(totalCobrado))
    print("  total que te deben: $" + str(totalDeuda))


cargarClientes()
cargarTrabajadores()

opcion = ""
while opcion != "0":
    print("\n1  - Cargar cliente")
    print("2  - Buscar cliente")
    print("3  - Asignar trabajo")
    print("4  - Cambiar estado de trabajo")
    print("5  - Trabajos del dia")
    print("6  - Mostrar todos los trabajos")
    print("7  - Trabajos pendientes")
    print("8  - Trabajos realizados")
    print("9  - Resumen de trabajos (totales)")
    print("10 - Cargar trabajador")
    print("11 - Eliminar trabajador")
    print("0  - Salir")
    opcion = input("elegí una opción: ")

    if opcion == "1":
        cargaDeDatosCliente()
    elif opcion == "2":
        buscarCliente()
    elif opcion == "3":
        asignarTrabajo()
    elif opcion == "4":
        cambioEstadoTrabajo()
    elif opcion == "5":
        trabajoDelDia()
    elif opcion == "6":
        mostrarTrabajos()
    elif opcion == "7":
        trabajosPendientes()
    elif opcion == "8":
        trabajosRealizados()
    elif opcion == "9":
        trabajosTotales()
    elif opcion == "10":
        cargaDatosTrabajador()
    elif opcion == "11":
        eliminarTrabajador()