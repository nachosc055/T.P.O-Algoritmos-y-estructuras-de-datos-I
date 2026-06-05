listaClientes = [
    {
        "idCliente": 0,
        "nombre": "lucas milani",
        "direccion": "9JL 1282",
        "telefono": "+54 9 11 28323529",
    },
    {
        "idCliente": 1,
        "nombre": "rosa fernandez",
        "direccion": "Av Corrientes 1420 piso 3B",
        "telefono": "+54 9 11 45671234",
    },
    {
        "idCliente": 2,
        "nombre": "consorcio pringles",
        "direccion": "Pringles 850",
        "telefono": "+54 9 11 33445566",
    },
    {
        "idCliente": 3,
        "nombre": "fabrica aberturas lopez",
        "direccion": "Av. San Martin 2100",
        "telefono": "+54 9 11 22334455",
    },
]

listaTrabajadores=[]
listaDeTrabajosPendientes=[]
listaDeTrabajosTerminados=[]


def cargaDeDatosCliente():
    idCliente=0
    if len(listaClientes)==0:
        idCliente=0
    else:
        idMaximo = listaClientes[-1]["idCliente"]
        idCliente = idMaximo+1

    nombreCliente = input("ingrese el nombre del cliente: ")
    while nombreCliente == "":
        nombreCliente = input("el nombre no puede estar vacio: ")

    direccionCliente = input("ingrese la direccion del cliente: ")
    while direccionCliente == "":
        direccionCliente = input("la direccion no puede estar vacia: ")

    telefonoCliente = input("ingrese el numero del cliente: ")
    while telefonoCliente == "":
        telefonoCliente = input("el telefono no puede estar vacio: ")

    nuevoCliente={
        "idCliente":idCliente,
        "nombre":nombreCliente,
        "direccion":direccionCliente,
        "telefono":telefonoCliente,
    }

    listaClientes.append(nuevoCliente)
    print("cliente creado con exito :)")

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
    clientePorAtender = input("ingrese el nombre del cliente al que hay que visitar: ")
    while clientePorAtender == "" or clientePorAtender.isdigit():
        clientePorAtender = input("el nombre no puede estar vacio ni ser un numero: ")

    direccionAVisitar = input("ingrese la direccion del cliente: ")
    while direccionAVisitar == "":
        direccionAVisitar = input("la direccion no puede estar vacia: ")

    trabajoARealizar = input("ingrese el trabajo hay que realizarle al cliente: ")
    while trabajoARealizar == "":
        trabajoARealizar = input("el trabajo no puede estar vacio: ")

    nombreDelTrabajador = input("ingrese el nombre del trabajador asignado: ")
    while nombreDelTrabajador == "" or nombreDelTrabajador.isdigit():
        nombreDelTrabajador = input("el nombre no puede estar vacio ni ser un numero: ")

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

    nuevoTrabajo = {
        "clientePorAtender": clientePorAtender,
        "direccionAVisitar": direccionAVisitar,
        "trabajoARealizar": trabajoARealizar,
        "nombreDelTrabajador": nombreDelTrabajador,
        "horarioDeVisita": horarioDeVisita,
        "fecha": fecha,
        "detalles": detalles,
        "estado": "pendiente",
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

    print("=== resumen de trabajos ===")
    print("total de trabajos: " + str(total))
    print("  pendientes: " + str(pendientes))
    print("  en proceso: " + str(enProceso))
    print("  terminados: " + str(terminados))
    print("  cobrados: " + str(cobrados))


opcion = ""
while opcion != "0":
    print("\n1 - Cargar cliente")
    print("2 - Buscar cliente")
    print("3 - Asignar trabajo")
    print("4 - Cambiar estado de trabajo")
    print("5 - Trabajos del dia")
    print("6 - Mostrar todos los trabajos")
    print("7 - Trabajos pendientes")
    print("8 - Trabajos realizados")
    print("9 - Resumen de trabajos (totales)")
    print("0 - Salir")
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