import datos
import validaciones
import cobros
import clientes
import agenda
import dashboard


# ----- Validaciones -----

def test_telefono_valido():
    assert validaciones.telefonoValido("+54 11 4567123")
    assert validaciones.telefonoValido("1145671234")


def test_telefono_invalido():
    assert not validaciones.telefonoValido("")
    assert not validaciones.telefonoValido("abc")
    assert not validaciones.telefonoValido("12")   # muy corto


def test_fecha_valida():
    assert validaciones.fechaValida("22/06/2026")
    assert not validaciones.fechaValida("2026-06-22")
    assert not validaciones.fechaValida("22/6/26")


def test_hora_valida():
    assert validaciones.horaValida("09:30")
    assert validaciones.horaValida("23:59")
    assert not validaciones.horaValida("24:00")
    assert not validaciones.horaValida("9.30")


# ----- Cobros -----

def test_saldo_deudor():
    trabajo = {"precio": 10000, "pagado": 4000}
    assert cobros.saldoDeudor(trabajo) == 6000


def test_saldo_nunca_negativo():
    trabajo = {"precio": 10000, "pagado": 12000}
    assert cobros.saldoDeudor(trabajo) == 0


def test_estado_de_pago():
    assert cobros.estadoDePago({"precio": 100, "pagado": 0}) == "pendiente"
    assert cobros.estadoDePago({"precio": 100, "pagado": 50}) == "pago parcial"
    assert cobros.estadoDePago({"precio": 100, "pagado": 100}) == "pagado"


def test_deuda_por_cliente():
    datos.listaTrabajos = [
        {"clientePorAtender": "rosa", "precio": 5000, "pagado": 1000, "nombreDelTecnico": "Carlos", "estado": "finalizado"},
        {"clientePorAtender": "rosa", "precio": 2000, "pagado": 0, "nombreDelTecnico": "Fede", "estado": "pendiente"},
        {"clientePorAtender": "lucas", "precio": 3000, "pagado": 3000, "nombreDelTecnico": "Mellizo", "estado": "cobrado"},
    ]
    deudas = cobros.deudaPorCliente()
    assert deudas["rosa"] == 6000     # 4000 + 2000
    assert "lucas" not in deudas      # ya pago todo


# ----- Recursividad -----

def test_cantidad_clientes():
    datos.listaClientes = [{"nombre": "a"}, {"nombre": "b"}, {"nombre": "c"}]
    assert clientes.cantidadClientes() == 3


def test_cantidad_clientes_vacia():
    datos.listaClientes = []
    assert clientes.cantidadClientes() == 0


def test_trabajos_de_tecnico():
    datos.listaTrabajos = [
        {"nombreDelTecnico": "Carlos"},
        {"nombreDelTecnico": "Fede"},
        {"nombreDelTecnico": "Carlos"},
    ]
    assert agenda.trabajosDeTecnico("Carlos") == 2
    assert agenda.trabajosDeTecnico("Fede") == 1
    assert agenda.trabajosDeTecnico("Santi") == 0


# ----- Matriz -----

def test_matriz_tecnico_estado():
    datos.listaTecnicos = [{"nombre": "Carlos"}, {"nombre": "Fede"}]
    datos.listaTrabajos = [
        {"nombreDelTecnico": "Carlos", "estado": "pendiente"},
        {"nombreDelTecnico": "Carlos", "estado": "cobrado"},
        {"nombreDelTecnico": "Fede", "estado": "pendiente"},
    ]
    nombres, estados, matriz = dashboard.matrizTrabajosPorTecnicoEstado()

    # la matriz tiene una fila por tecnico y una columna por estado
    assert len(matriz) == 2
    assert len(matriz[0]) == len(estados)

    filaCarlos = nombres.index("Carlos")
    colPendiente = estados.index("pendiente")
    colCobrado = estados.index("cobrado")
    assert matriz[filaCarlos][colPendiente] == 1
    assert matriz[filaCarlos][colCobrado] == 1

    filaFede = nombres.index("Fede")
    assert matriz[filaFede][colPendiente] == 1
