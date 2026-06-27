import datos
import validaciones


def cargaDeDatosCliente():
    # el id nuevo es el ultimo + 1 (o 0 si la lista esta vacia)
    if len(datos.listaClientes) == 0:
        idCliente = 0
    else:
        idCliente = datos.listaClientes[-1]["idCliente"] + 1

    nombreCliente = input("ingrese el nombre del cliente: ")
    while nombreCliente == "":
        nombreCliente = input("el nombre no puede estar vacio: ")

    direccionCliente = input("ingrese la direccion del cliente: ")
    while direccionCliente == "":
        direccionCliente = input("la direccion no puede estar vacia: ")

    telefonoCliente = input("ingrese el numero del cliente: ")
    while not validaciones.telefonoValido(telefonoCliente):
        telefonoCliente = input("formato invalido, ingrese un numero valido (ej: +54 9 11 12345678): ")

    print("tipo de cliente:")
    for i in range(len(datos.TIPOS_CLIENTE)):
        print(str(i + 1) + " - " + datos.TIPOS_CLIENTE[i])
    opcionTipo = input("elegi el tipo de cliente: ")
    while not opcionTipo.isdigit() or int(opcionTipo) < 1 or int(opcionTipo) > len(datos.TIPOS_CLIENTE):
        opcionTipo = input("opcion invalida, elegi de nuevo: ")
    tipoCliente = datos.TIPOS_CLIENTE[int(opcionTipo) - 1]

    nuevoCliente = {
        "idCliente": idCliente,
        "nombre": nombreCliente,
        "direccion": direccionCliente,
        "telefono": telefonoCliente,
        "tipo": tipoCliente,
    }

    datos.listaClientes.append(nuevoCliente)
    datos.guardarClientes()
    print("cliente creado con exito :)")


def buscarCliente():
    clienteABuscar = input("ingrese el nombre del cliente a buscar: ")
    indice = None
    for i in range(len(datos.listaClientes)):
        c = datos.listaClientes[i]
        if clienteABuscar.lower() in c["nombre"].lower():
            if indice is None:
                indice = i
            print("cliente encontrado: " + c["nombre"] + " | " + c["direccion"] + " | " + c["telefono"] + " | " + c["tipo"])
    if indice is None:
        print("cliente no encontrado, volviendo al menu...")
    return indice


def cantidadClientes(indice=0):
    # Cuenta los clientes de forma recursiva
    if indice >= len(datos.listaClientes):
        return 0
    return 1 + cantidadClientes(indice + 1)
