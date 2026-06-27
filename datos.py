import os

RUTA_BASE = os.path.dirname(os.path.abspath(__file__))
RUTA_CLIENTES = os.path.join(RUTA_BASE, "clientes.txt")
RUTA_TECNICOS = os.path.join(RUTA_BASE, "tecnicos.txt")
RUTA_TRABAJOS = os.path.join(RUTA_BASE, "trabajos.txt")

listaClientes = []
listaTecnicos = []
listaTrabajos = []

TIPOS_CLIENTE = ("particular", "empresa")

ESTADOS_TRABAJO = ("pendiente", "en curso", "finalizado", "cobrado")


# ----- Clientes -----

def cargarClientes():
    global listaClientes
    if os.path.exists(RUTA_CLIENTES):
        try:
            listaClientes = []
            with open(RUTA_CLIENTES, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea == "":
                        continue
                    campos = linea.split(";")
                    cliente = {
                        "idCliente": int(campos[0]),
                        "nombre": campos[1],
                        "direccion": campos[2],
                        "telefono": campos[3],
                        "tipo": campos[4]
                    }
                    listaClientes.append(cliente)
        except Exception as e:
            print("ocurrio un error al cargar clientes.txt:", e)
    else:
        listaClientes = [
            {"idCliente": 0, "nombre": "lucas milani", "direccion": "9JL 1282", "telefono": "+54 9 11 28323529", "tipo": "particular"},
            {"idCliente": 1, "nombre": "rosa fernandez", "direccion": "Av Corrientes 1420 piso 3B", "telefono": "+54 9 11 45671234", "tipo": "particular"},
            {"idCliente": 2, "nombre": "consorcio pringles", "direccion": "Pringles 850", "telefono": "+54 9 11 33445566", "tipo": "empresa"},
            {"idCliente": 3, "nombre": "fabrica aberturas lopez", "direccion": "Av. San Martin 2100", "telefono": "+54 9 11 22334455", "tipo": "empresa"},
        ]
        guardarClientes()


def guardarClientes():
    try:
        with open(RUTA_CLIENTES, "w", encoding="utf-8") as archivo:
            for c in listaClientes:
                campos = [str(c["idCliente"]), c["nombre"], c["direccion"], c["telefono"], c["tipo"]]
                archivo.write(";".join(campos) + "\n")
    except Exception as e:
        print("ocurrio un error al guardar clientes.txt:", e)


# ----- Tecnicos -----

def cargarTecnicos():
    global listaTecnicos
    if os.path.exists(RUTA_TECNICOS):
        try:
            listaTecnicos = []
            with open(RUTA_TECNICOS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea == "":
                        continue
                    campos = linea.split(";")
                    tecnico = {
                        "idTecnico": int(campos[0]),
                        "nombre": campos[1],
                        "especialidad": campos[2],
                    }
                    listaTecnicos.append(tecnico)
        except Exception as e:
            print("ocurrio un error al cargar tecnicos.txt:", e)
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
            for t in listaTecnicos:
                campos = [str(t["idTecnico"]), t["nombre"], t["especialidad"]]
                archivo.write(";".join(campos) + "\n")
    except Exception as e:
        print("ocurrio un error al guardar tecnicos.txt:", e)


# ----- Trabajos -----

def formatearPagos(pagos):
    # cada pago queda como "monto,fecha" y se separan entre si con "|"
    # (ej: "2000,29/06/2026|3000,01/07/2026")
    partes = []
    for p in pagos:
        partes.append(str(p["monto"]) + "," + p["fecha"])
    return "|".join(partes)


def desformatearPagos(texto):
    pagos = []
    if texto == "":
        return pagos
    for item in texto.split("|"):
        monto, fecha = item.split(",")
        pagos.append({"monto": int(monto), "fecha": fecha})
    return pagos


def cargarTrabajos():
    global listaTrabajos
    if os.path.exists(RUTA_TRABAJOS):
        try:
            listaTrabajos = []
            with open(RUTA_TRABAJOS, "r", encoding="utf-8") as archivo:
                for linea in archivo:
                    linea = linea.strip()
                    if linea == "":
                        continue
                    campos = linea.split(";")
                    trabajo = {
                        "clientePorAtender": campos[0],
                        "direccionAVisitar": campos[1],
                        "trabajoARealizar": campos[2],
                        "nombreDelTecnico": campos[3],
                        "horarioDeVisita": campos[4],
                        "fecha": campos[5],
                        "detalles": campos[6],
                        "estado": campos[7],
                        "precio": int(campos[8]),
                        "pagado": int(campos[9]),
                        "pagos": desformatearPagos(campos[10]),
                    }
                    listaTrabajos.append(trabajo)
        except Exception as e:
            print("ocurrio un error al cargar trabajos.txt:", e)
    else:
        listaTrabajos = [
            {
                "clientePorAtender": "rosa fernandez",
                "direccionAVisitar": "Av Corrientes 1420 piso 3B",
                "trabajoARealizar": "perdida de agua en el equipo del living",
                "nombreDelTecnico": "Mellizo",
                "horarioDeVisita": "14:30",
                "fecha": "29/06/2026",
                "detalles": "revisar el drenaje",
                "estado": "en curso",
                "precio": 35000,
                "pagado": 0,
                "pagos": [],
            },
            {
                "clientePorAtender": "consorcio pringles",
                "direccionAVisitar": "Pringles 850",
                "trabajoARealizar": "mantenimiento de la bomba de agua",
                "nombreDelTecnico": "Carlos",
                "horarioDeVisita": "09:00",
                "fecha": "30/06/2026",
                "detalles": "preguntar por el encargado",
                "estado": "finalizado",
                "precio": 80000,
                "pagado": 40000,
                "pagos": [{"monto": 40000, "fecha": "28/06/2026"}],
            },
        ]
        guardarTrabajos()


def guardarTrabajos():
    try:
        with open(RUTA_TRABAJOS, "w", encoding="utf-8") as archivo:
            for t in listaTrabajos:
                campos = [
                    t["clientePorAtender"],
                    t["direccionAVisitar"],
                    t["trabajoARealizar"],
                    t["nombreDelTecnico"],
                    t["horarioDeVisita"],
                    t["fecha"],
                    t["detalles"],
                    t["estado"],
                    str(t["precio"]),
                    str(t["pagado"]),
                    formatearPagos(t["pagos"]),
                ]
                archivo.write(";".join(campos) + "\n")
    except Exception as e:
        print("ocurrio un error al guardar trabajos.txt:", e)


def cargarTodo():
    cargarClientes()
    cargarTecnicos()
    cargarTrabajos()
