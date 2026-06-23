import datos
import clientes
import tecnicos
import trabajos
import agenda
import cobros
import dashboard


def mostrarMenu():
    print("\n========== TALLER DE OLI ==========")
    print("-- Clientes --")
    print("1  - Cargar cliente")
    print("2  - Buscar cliente")
    print("-- Tecnicos --")
    print("3  - Cargar tecnico")
    print("4  - Eliminar tecnico")
    print("-- Trabajos --")
    print("5  - Asignar trabajo")
    print("6  - Cambiar estado de trabajo")
    print("7  - Mostrar todos los trabajos")
    print("8  - Trabajos pendientes")
    print("9  - Trabajos realizados")
    print("-- Agenda --")
    print("10 - Trabajos del dia")
    print("11 - Agenda por tecnico")
    print("12 - Hoja de ruta del tecnico")
    print("-- Cobros --")
    print("13 - Registrar cobro")
    print("-- Resumen --")
    print("14 - Resumen general")
    print("15 - Resumen de trabajos (totales)")
    print("16 - Matriz trabajos por tecnico/estado")
    print("17 - Tecnicos ocupados")
    print("0  - Salir")


# las opciones del menu apuntan a la funcion de cada modulo
acciones = {
    "1": clientes.cargaDeDatosCliente,
    "2": clientes.buscarCliente,
    "3": tecnicos.cargaDatosTecnico,
    "4": tecnicos.eliminarTecnico,
    "5": trabajos.asignarTrabajo,
    "6": trabajos.cambioEstadoTrabajo,
    "7": trabajos.mostrarTrabajos,
    "8": trabajos.trabajosPendientes,
    "9": trabajos.trabajosRealizados,
    "10": agenda.trabajoDelDia,
    "11": agenda.agendaPorTecnico,
    "12": agenda.hojaDeRutaTecnico,
    "13": cobros.registrarCobro,
    "14": dashboard.resumenGeneral,
    "15": dashboard.trabajosTotales,
    "16": dashboard.mostrarMatriz,
    "17": dashboard.tecnicosOcupados,
}


def main():
    datos.cargarTodo()

    opcion = ""
    while opcion != "0":
        mostrarMenu()
        opcion = input("elegi una opcion: ")

        if opcion == "0":
            print("hasta luego!")
        elif opcion in acciones:
            try:
                acciones[opcion]()
            except ValueError:
                print("entrada invalida, tenias que ingresar un numero. volviendo al menu...")
        else:
            print("opcion invalida, elegi una del menu")


if __name__ == "__main__":
    main()
