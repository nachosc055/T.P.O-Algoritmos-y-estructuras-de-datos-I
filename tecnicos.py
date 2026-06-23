import datos


def cargaDatosTecnico():
    if len(datos.listaTecnicos) == 0:
        idTecnico = 0
    else:
        idTecnico = datos.listaTecnicos[-1]["idTecnico"] + 1

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

    datos.listaTecnicos.append(nuevoTecnico)
    datos.guardarTecnicos()
    print("tecnico cargado con exito :)")


def eliminarTecnico():
    if len(datos.listaTecnicos) == 0:
        print("no hay tecnicos registrados")
        return

    print("=== tecnicos registrados ===")
    for i in range(len(datos.listaTecnicos)):
        print(str(i + 1) + " - " + datos.listaTecnicos[i]["nombre"] + " | " + datos.listaTecnicos[i]["especialidad"])

    opcion = int(input("selecciona el numero del tecnico a eliminar (0 para cancelar): "))
    while opcion < 0 or opcion > len(datos.listaTecnicos):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    if opcion == 0:
        print("operacion cancelada")
        return

    tecnicoEliminado = datos.listaTecnicos.pop(opcion - 1)
    datos.guardarTecnicos()
    print("tecnico eliminado: " + tecnicoEliminado["nombre"])
