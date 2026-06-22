import os
import json
import re
from functools import reduce

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CLIENTES = os.path.join(RUTA_BASE, "clientes.json")
RUTA_TECNICOS = os.path.join(RUTA_BASE, "tecnicos.json")

listaClientes = []
listaTecnicos = []
listaDeTrabajosPendientes = []
listaDeTrabajosTerminados = []

TIPOS_TRABAJO = (
    "limpieza de filtros",
    "carga de gas",
    "instalacion de aire",
    "revision de perdida de agua",
    "mantenimiento de aires",
    "herreria liviana",
    "otro",
)

def cargarClientes():
    global listaClientes
    if os.path.exists(RUTA_CLIENTES):
        try:
            with open(RUTA_CLIENTES, "r", encoding="utf-8") as archivo:
                listaClientes = json.load(archivo)
        except Exception as e:
            print("ocurrio un error al cargar clientes.json:", e)
    else:
        listaClientes = [
            {"idCliente": 0, "nombre": "lucas milani", "direccion": "9JL 1282", "telefono": "+54 9 11 28323529"},
            {"idCliente": 1, "nombre": "rosa fernandez", "direccion": "Av Corrientes 1420 piso 3B", "telefono": "+54 9 11 45671234"},
            {"idCliente": 2, "nombre": "consorcio pringles", "direccion": "Pringles 850", "telefono": "+54 9 11 33445566"},
            {"idCliente": 3, "nombre": "fabrica aberturas lopez", "direccion": "Av. San Martin 2100", "telefono": "+54 9 11 22334455"},
        ]
        guardarClientes()


def guardarClientes():
    try:
        with open(RUTA_CLIENTES, "w", encoding="utf-8") as archivo:
            json.dump(listaClientes, archivo, indent=4)
    except Exception as e:
        print("ocurrio un error al guardar clientes.json:", e)


def cargarTecnicos():
    global listaTecnicos
    if os.path.exists(RUTA_TECNICOS):
        try:
            with open(RUTA_TECNICOS, "r", encoding="utf-8") as archivo:
                listaTecnicos = json.load(archivo)
        except Exception as e:
            print("ocurrio un error al cargar tecnicos.json:", e)
    else:
        listaTecnicos = [
            {"idTecnico": 0, "nombre": "Carlos", "especialidad": "herreria y equipos comerciales"},
            {"idTecnico": 1, "nombre": "Mellizo", "especialidad": "electricidad e instalacion de aires"},
            {"idTecnico": 2, "nombre": "Fede", "especialidad": "mantenimiento y limpieza"},
            {"idTecnico": 3, "nombre": "Santi", "especialidad": "logistica y traslado de materiales"},
        ]
        guardarTecnicos()


def guardarTecnicos():
    try:
        with open(RUTA_TECNICOS, "w", encoding="utf-8") as archivo:
            json.dump(listaTecnicos, archivo, indent=4)
    except Exception as e:
        print("ocurrio un error al guardar tecnicos.json:", e)


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
    while not re.match(r"^\+?[\d\s\-]{8,15}$", telefonoCliente):
        telefonoCliente = input("formato invalido, ingrese un numero valido (ej: +54 9 11 12345678): ")

    nuevoCliente = {
        "idCliente": idCliente,
        "nombre": nombreCliente,
        "direccion": direccionCliente,
        "telefono": telefonoCliente,
    }

    listaClientes.append(nuevoCliente)
    guardarClientes()
    print("cliente creado con exito :)")


def cargaDatosTecnico():
    idTecnico = 0
    if len(listaTecnicos) == 0:
        idTecnico = 0
    else:
        idMaximo = listaTecnicos[-1]["idTecnico"]
        idTecnico = idMaximo + 1

    nombreTecnico = input("ingrese el nombre del tecnico: ")
    while nombreTecnico == "" or nombreTecnico.isdigit():
        nombreTecnico = input("el nombre no puede estar vacio ni ser un numero: ")

    especialidad = input("ingrese la especialidad del tecnico (ej: electricidad, herreria): ")
    while especialidad == "":
        especialidad = input("la especialidad no puede estar vacia: ")

    nuevoTecnico = {
        "idTecnico": idTecnico,
        "nombre": nombreTecnico,
        "especialidad": especialidad,
    }

    listaTecnicos.append(nuevoTecnico)
    guardarTecnicos()
    print("tecnico cargado con exito :)")


def eliminarTecnico():
    if len(listaTecnicos) == 0:
        print("no hay tecnicos registrados")
        return

    print("=== tecnicos registrados ===")
    for i in range(len(listaTecnicos)):
        print(str(i+1) + " - " + listaTecnicos[i]["nombre"] + " | " + listaTecnicos[i]["especialidad"])

    opcion = int(input("selecciona el numero del tecnico a eliminar (0 para cancelar): "))
    while opcion < 0 or opcion > len(listaTecnicos):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    if opcion == 0:
        print("operacion cancelada")
        return

    tecnicoEliminado = listaTecnicos.pop(opcion - 1)
    guardarTecnicos()
    print("tecnico eliminado: " + tecnicoEliminado["nombre"])


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


def cantidadClientes(Index=0):
    if Index >= len(listaClientes):
        return 0
    return 1 + cantidadClientes(Index + 1)


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

    print("=== tipo de trabajo ===")
    for i in range(len(TIPOS_TRABAJO)):
        print(str(i+1) + " - " + TIPOS_TRABAJO[i])

    opcionTrabajo = int(input("selecciona el tipo de trabajo: "))
    while opcionTrabajo < 1 or opcionTrabajo > len(TIPOS_TRABAJO):
        opcionTrabajo = int(input("opcion invalida, elegi de nuevo: "))

    trabajoARealizar = TIPOS_TRABAJO[opcionTrabajo - 1]
    if trabajoARealizar == "otro":
        trabajoARealizar = input("describí el trabajo a realizar: ")
        while trabajoARealizar == "":
            trabajoARealizar = input("el trabajo no puede estar vacio: ")

    if len(listaTecnicos) == 0:
        print("no hay tecnicos registrados, cargue uno primero")
        return

    print("=== tecnicos disponibles ===")
    for i in range(len(listaTecnicos)):
        print(str(i+1) + " - " + listaTecnicos[i]["nombre"] + " | " + listaTecnicos[i]["especialidad"])

    opcionTecnico = int(input("selecciona el numero del tecnico: "))
    while opcionTecnico < 1 or opcionTecnico > len(listaTecnicos):
        opcionTecnico = int(input("opcion invalida, elegi de nuevo: "))

    nombreDelTecnico = listaTecnicos[opcionTecnico - 1]["nombre"]
    print("tecnico seleccionado: " + nombreDelTecnico)

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
    while not re.match(r"^\d{2}/\d{2}/\d{4}$", fecha):
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
    }

    listaDeTrabajosPendientes.append(nuevoTrabajo)
    print("trabajo asignado con exito!")


def trabajosDeTecnico(nombre, Index2=0):
    if Index2 >= len(listaDeTrabajosPendientes):
        return 0
    suma = 0
    if listaDeTrabajosPendientes[Index2]["nombreDelTecnico"] == nombre:
        suma = 1
    return suma + trabajosDeTecnico(nombre, Index2 + 1)


def cambioEstadoTrabajo():
    direccionBuscada = input("ingrese la direccion del cliente: ")
    indice = None

    for i in range(len(listaDeTrabajosPendientes)):
        if listaDeTrabajosPendientes[i]["direccionAVisitar"].lower() == direccionBuscada.lower():
            indice = i
            break

    if indice == None:
        print("no se encontro ningun trabajo para esa direccion")
        return

    t = listaDeTrabajosPendientes[indice]
    print("trabajo encontrado: " + t["trabajoARealizar"] + " | cliente: " + t["clientePorAtender"] + " | estado actual: " + t["estado"])

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
        print("  tecnico: " + t["nombreDelTecnico"])
        print("  cliente: " + t["clientePorAtender"])
        print("  tarea: " + t["trabajoARealizar"])
        print("  hora: " + str(t["horarioDeVisita"]))
        print("  ---")


def mostrarUnTrabajo(t):
    print("  cliente: " + t["clientePorAtender"])
    print("  direccion: " + t["direccionAVisitar"])
    print("  tarea: " + t["trabajoARealizar"])
    print("  tecnico: " + t["nombreDelTecnico"])
    print("  fecha: " + t["fecha"] + " | hora: " + t["horarioDeVisita"])
    print("  estado: " + t["estado"])
    if t["detalles"] != "":
        print("  detalles: " + t["detalles"])
    deuda = t["precio"] - t["pagado"]
    if deuda < 0:
        deuda = 0
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

    pendientes = len(list(filter(lambda x: x["estado"] == "pendiente", listaDeTrabajosPendientes)))
    enProceso = len(list(filter(lambda x: x["estado"] == "en proceso", listaDeTrabajosPendientes)))
    terminados = len(list(filter(lambda x: x["estado"] == "terminado", listaDeTrabajosPendientes)))
    cobrados = len(list(filter(lambda x: x["estado"] == "cobrado", listaDeTrabajosPendientes)))

    totalFacturado = sum(map(lambda x: x["precio"], listaDeTrabajosPendientes))
    totalCobrado = sum(map(lambda x: x["pagado"], listaDeTrabajosPendientes))
    totalDeuda = reduce(lambda acum, t: acum + (t["precio"] - t["pagado"]), listaDeTrabajosPendientes, 0)

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


def tecnicosOcupados():
    ocupados = set()
    for t in listaDeTrabajosPendientes:
        if t["estado"] == "pendiente" or t["estado"] == "en proceso":
            ocupados.add(t["nombreDelTecnico"])

    if len(ocupados) == 0:
        print("no hay tecnicos con trabajos asignados")
        return

    print("=== tecnicos con trabajos activos ===")
    for nombre in ocupados:
        print("  - " + nombre)


cargarClientes()
cargarTecnicos()

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
    print("10 - Cargar tecnico")
    print("11 - Eliminar tecnico")
    print("12 - Tecnicos ocupados")
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
        cargaDatosTecnico()
    elif opcion == "11":
        eliminarTecnico()
    elif opcion == "12":
        tecnicosOcupados()
