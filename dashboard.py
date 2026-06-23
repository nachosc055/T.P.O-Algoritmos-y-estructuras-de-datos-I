from functools import reduce

import datos
import cobros


def trabajosTotales():
    total = len(datos.listaTrabajos)
    if total == 0:
        print("no hay trabajos cargados")
        return

    pendientes = len(list(filter(lambda x: x["estado"] == "pendiente", datos.listaTrabajos)))
    enProceso = len(list(filter(lambda x: x["estado"] == "en proceso", datos.listaTrabajos)))
    terminados = len(list(filter(lambda x: x["estado"] == "terminado", datos.listaTrabajos)))
    cobrados = len(list(filter(lambda x: x["estado"] == "cobrado", datos.listaTrabajos)))

    totalFacturado = sum(map(lambda x: x["precio"], datos.listaTrabajos))
    totalCobrado = sum(map(lambda x: x["pagado"], datos.listaTrabajos))
    totalDeuda = reduce(lambda acum, t: acum + cobros.saldoDeudor(t), datos.listaTrabajos, 0)

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
    for t in datos.listaTrabajos:
        if t["estado"] in ("pendiente", "en proceso"):
            ocupados.add(t["nombreDelTecnico"])

    if len(ocupados) == 0:
        print("no hay tecnicos con trabajos asignados")
        return

    print("=== tecnicos con trabajos activos ===")
    for nombre in ocupados:
        print("  - " + nombre)


def matrizTrabajosPorTecnicoEstado():
    nombresTecnicos = list(map(lambda tec: tec["nombre"], datos.listaTecnicos))
    estados = list(datos.ESTADOS_TRABAJO)

    matriz = [[0 for _ in estados] for _ in nombresTecnicos]

    for trabajo in datos.listaTrabajos:
        tecnico = trabajo["nombreDelTecnico"]
        estado = trabajo["estado"]
        if tecnico in nombresTecnicos and estado in estados:
            fila = nombresTecnicos.index(tecnico)
            columna = estados.index(estado)
            matriz[fila][columna] += 1

    return nombresTecnicos, estados, matriz


def mostrarMatriz():
    nombresTecnicos, estados, matriz = matrizTrabajosPorTecnicoEstado()

    if len(nombresTecnicos) == 0:
        print("no hay tecnicos registrados")
        return

    print("=== matriz de trabajos (tecnico x estado) ===")
    encabezado = "tecnico".ljust(12)
    for estado in estados:
        encabezado += estado.ljust(13)
    print(encabezado)

    for i in range(len(nombresTecnicos)):
        fila = nombresTecnicos[i].ljust(12)
        for j in range(len(estados)):
            fila += str(matriz[i][j]).ljust(13)
        print(fila)


def resumenGeneral():
    print("=========== RESUMEN GENERAL ===========")

    activos = list(filter(lambda t: t["estado"] in ("pendiente", "en proceso"), datos.listaTrabajos))
    print("\n-- trabajos activos (pendientes / en proceso): " + str(len(activos)))
    for t in activos:
        print("  - " + t["clientePorAtender"] + " | " + t["trabajoARealizar"] + " | " + t["estado"])

    sinCobrar = list(filter(lambda t: t["estado"] == "terminado", datos.listaTrabajos))
    print("\n-- trabajos terminados sin cobrar: " + str(len(sinCobrar)))
    for t in sinCobrar:
        print("  - " + t["clientePorAtender"] + " | debe: $" + str(cobros.saldoDeudor(t)))

    deudas = cobros.deudaPorCliente()
    print("\n-- clientes con deuda: " + str(len(deudas)))
    for cliente in deudas:
        print("  - " + cliente + ": $" + str(deudas[cliente]))

    print("\n=======================================")
