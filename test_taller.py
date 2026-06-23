import unittest

import datos
import validaciones
import cobros
import clientes
import agenda
import dashboard


class TestValidaciones(unittest.TestCase):

    def test_telefono_valido(self):
        self.assertTrue(validaciones.telefonoValido("+54 11 4567123"))
        self.assertTrue(validaciones.telefonoValido("1145671234"))

    def test_telefono_invalido(self):
        self.assertFalse(validaciones.telefonoValido(""))
        self.assertFalse(validaciones.telefonoValido("abc"))
        self.assertFalse(validaciones.telefonoValido("12"))  # muy corto

    def test_fecha_valida(self):
        self.assertTrue(validaciones.fechaValida("22/06/2026"))
        self.assertFalse(validaciones.fechaValida("2026-06-22"))
        self.assertFalse(validaciones.fechaValida("22/6/26"))

    def test_hora_valida(self):
        self.assertTrue(validaciones.horaValida("09:30"))
        self.assertTrue(validaciones.horaValida("23:59"))
        self.assertFalse(validaciones.horaValida("24:00"))
        self.assertFalse(validaciones.horaValida("9.30"))


class TestCobros(unittest.TestCase):

    def test_saldo_deudor(self):
        trabajo = {"precio": 10000, "pagado": 4000}
        self.assertEqual(cobros.saldoDeudor(trabajo), 6000)

    def test_saldo_nunca_negativo(self):
        trabajo = {"precio": 10000, "pagado": 12000}
        self.assertEqual(cobros.saldoDeudor(trabajo), 0)

    def test_estado_de_pago(self):
        self.assertEqual(cobros.estadoDePago({"precio": 100, "pagado": 0}), "pendiente")
        self.assertEqual(cobros.estadoDePago({"precio": 100, "pagado": 50}), "pago parcial")
        self.assertEqual(cobros.estadoDePago({"precio": 100, "pagado": 100}), "pagado")

    def test_deuda_por_cliente(self):
        datos.listaTrabajos = [
            {"clientePorAtender": "rosa", "precio": 5000, "pagado": 1000, "nombreDelTecnico": "Carlos", "estado": "terminado"},
            {"clientePorAtender": "rosa", "precio": 2000, "pagado": 0, "nombreDelTecnico": "Fede", "estado": "pendiente"},
            {"clientePorAtender": "lucas", "precio": 3000, "pagado": 3000, "nombreDelTecnico": "Mellizo", "estado": "cobrado"},
        ]
        deudas = cobros.deudaPorCliente()
        self.assertEqual(deudas["rosa"], 6000)   # 4000 + 2000
        self.assertNotIn("lucas", deudas)        # ya pago todo


class TestRecursividad(unittest.TestCase):

    def test_cantidad_clientes(self):
        datos.listaClientes = [{"nombre": "a"}, {"nombre": "b"}, {"nombre": "c"}]
        self.assertEqual(clientes.cantidadClientes(), 3)

    def test_cantidad_clientes_vacia(self):
        datos.listaClientes = []
        self.assertEqual(clientes.cantidadClientes(), 0)

    def test_trabajos_de_tecnico(self):
        datos.listaTrabajos = [
            {"nombreDelTecnico": "Carlos"},
            {"nombreDelTecnico": "Fede"},
            {"nombreDelTecnico": "Carlos"},
        ]
        self.assertEqual(agenda.trabajosDeTecnico("Carlos"), 2)
        self.assertEqual(agenda.trabajosDeTecnico("Fede"), 1)
        self.assertEqual(agenda.trabajosDeTecnico("Santi"), 0)


class TestMatriz(unittest.TestCase):

    def test_matriz_tecnico_estado(self):
        datos.listaTecnicos = [{"nombre": "Carlos"}, {"nombre": "Fede"}]
        datos.listaTrabajos = [
            {"nombreDelTecnico": "Carlos", "estado": "pendiente"},
            {"nombreDelTecnico": "Carlos", "estado": "cobrado"},
            {"nombreDelTecnico": "Fede", "estado": "pendiente"},
        ]
        nombres, estados, matriz = dashboard.matrizTrabajosPorTecnicoEstado()

        # la matriz tiene una fila por tecnico y una columna por estado
        self.assertEqual(len(matriz), 2)
        self.assertEqual(len(matriz[0]), len(estados))

        filaCarlos = nombres.index("Carlos")
        colPendiente = estados.index("pendiente")
        colCobrado = estados.index("cobrado")
        self.assertEqual(matriz[filaCarlos][colPendiente], 1)
        self.assertEqual(matriz[filaCarlos][colCobrado], 1)

        filaFede = nombres.index("Fede")
        self.assertEqual(matriz[filaFede][colPendiente], 1)


if __name__ == "__main__":
    unittest.main()
