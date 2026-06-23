import re

def telefonoValido(telefono):
    # Acepta numeros con +, digitos, espacios y guiones (entre 8 y 15) 
    return re.match(r"^\+?[\d\s\-]{8,15}$", telefono) is not None


def fechaValida(fecha):
    # Valida el formato DD/MM/AAAA
    return re.match(r"^\d{2}/\d{2}/\d{4}$", fecha) is not None


def horaValida(hora):
    # Valida el formato HH:MM con horas 0-23 y minutos 0-59
    partes = hora.split(":")
    if len(partes) != 2 or not partes[0].isdigit() or not partes[1].isdigit():
        return False
    return int(partes[0]) <= 23 and int(partes[1]) <= 59
