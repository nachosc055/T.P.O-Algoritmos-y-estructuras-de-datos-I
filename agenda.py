import datos
import trabajos


def trabajoDelDia():
    fecha = input("ingrese la fecha a consultar (DD/MM/AAAA): ")
    encontrados = list(filter(lambda t: t["fecha"] == fecha, datos.listaTrabajos))

    if len(encontrados) == 0:
        print("no hay trabajos para esa fecha")
        return

    print("=== trabajos para el " + fecha + " ===")
    for t in encontrados:
        print("  tecnico: " + t["nombreDelTecnico"])
        print("  cliente: " + t["clientePorAtender"])
        print("  tarea: " + t["trabajoARealizar"])
        print("  hora: " + str(t["horarioDeVisita"]))
        print("  ---")


def trabajosDeTecnico(nombre, indice=0):
    # Cuenta de forma recursiva cuantos trabajos tiene asignados un tecnico
    if indice >= len(datos.listaTrabajos):
        return 0
    suma = 1 if datos.listaTrabajos[indice]["nombreDelTecnico"] == nombre else 0
    return suma + trabajosDeTecnico(nombre, indice + 1)


def agendaPorTecnico():
    if len(datos.listaTecnicos) == 0:
        print("no hay tecnicos registrados")
        return

    print("=== tecnicos ===")
    for i in range(len(datos.listaTecnicos)):
        print(str(i + 1) + " - " + datos.listaTecnicos[i]["nombre"])

    opcion = int(input("selecciona el tecnico: "))
    while opcion < 1 or opcion > len(datos.listaTecnicos):
        opcion = int(input("opcion invalida, elegi de nuevo: "))

    nombre = datos.listaTecnicos[opcion - 1]["nombre"]
    asignados = list(filter(lambda t: t["nombreDelTecnico"] == nombre, datos.listaTrabajos))

    print("=== " + nombre + " tiene " + str(trabajosDeTecnico(nombre)) + " trabajo(s) ===")
    for t in asignados:
        trabajos.mostrarUnTrabajo(t)


def hojaDeRutaTecnico():
    nombre = input("ingrese el nombre del tecnico: ")
    fecha = input("ingrese la fecha (DD/MM/AAAA): ")

    ruta = list(filter(
        lambda t: t["nombreDelTecnico"] == nombre and t["fecha"] == fecha,
        datos.listaTrabajos,
    ))

    if len(ruta) == 0:
        print("no hay trabajos para " + nombre + " el " + fecha)
        return

    print("=== hoja de ruta de " + nombre + " para el " + fecha + " ===")
    for t in ruta:
        print("  " + t["horarioDeVisita"] + " - " + t["clientePorAtender"])
        print("    direccion: " + t["direccionAVisitar"])
        print("    tarea: " + t["trabajoARealizar"])
        if t["detalles"] != "":
            print("    detalles: " + t["detalles"])
        print("    estado: " + t["estado"])
        print("    ---")
