# Sistema de Gestión — Taller de Climatización y Herrería (Oli)

Sistema interno para que Oli y la asistente administrativa gestionen el taller:
clientes, trabajos, agenda de técnicos, cobros y un resumen del estado del
negocio. Reemplaza el cuaderno físico y el Excel desactualizado que usaban antes.

Es una aplicación de consola escrita en **Python** (sin librerías externas).

---

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
python main.py
```

Arranca el menú principal. Se navega escribiendo el número de la opción y
Enter. La opción `0` cierra el programa.

### Correr los tests

```bash
python -m unittest test_taller
```

(o también `python test_taller.py`). Son 12 tests que validan la lógica del
sistema; si todo está bien termina con `OK`.

---

## Estructura del proyecto

El sistema estaba originalmente en un solo archivo y se dividió en módulos para
que cada parte tenga una responsabilidad clara y se pueda entender y testear por
separado.

```
main.py            -> menú principal, une todo
datos.py           -> datos compartidos + lectura/escritura de los .txt
validaciones.py    -> validaciones de formato (teléfono, fecha, hora)
clientes.py        -> alta, búsqueda y conteo de clientes
tecnicos.py        -> alta y baja de técnicos
trabajos.py        -> alta de trabajos, cambio de estado y listados
agenda.py          -> trabajos por fecha, por técnico y hoja de ruta
cobros.py          -> precios, pagos y saldos deudores
dashboard.py       -> resumen del negocio + matriz técnico/estado
test_taller.py     -> tests unitarios

clientes.txt       -> se generan solos al ejecutar (datos persistidos)
tecnicos.txt
trabajos.txt
```

### Cómo se comparte la información entre módulos

Todo el estado del sistema (las listas de clientes, técnicos y trabajos) vive en
**`datos.py`**. Los demás módulos hacen `import datos` y acceden siempre como
`datos.listaClientes`, `datos.listaTrabajos`, etc.

Esto es importante en Python: si cada módulo hiciera `from datos import listaClientes`
se quedaría con una copia "vieja" de la referencia y no vería los cambios. Al
acceder como `datos.listaClientes` siempre se lee el valor actualizado.

Los datos se guardan automáticamente en archivos de texto (`.txt`) cada vez que
se crea o modifica algo, así no se pierden al cerrar el programa. Cada registro
es una línea con los campos separados por `;` (se escribe con `open` en modo
`"w"` y se lee con `open` en modo `"r"` y `.split(";")`, todo dentro de
`try`/`except`). Si los archivos no existen, la primera ejecución los crea con
datos de ejemplo (clientes y técnicos).

---

## Módulos del sistema (relación con el análisis)

Cada archivo cubre uno o más de los seis módulos funcionales que se identificaron
en la etapa de análisis:

| Módulo del análisis | Archivo(s) | Qué resuelve |
|---|---|---|
| 1. Registro de Clientes | `clientes.py` | Pérdida de datos y direcciones de clientes |
| 2. Registro de Trabajos | `trabajos.py` | Falta de historial y de estado de los trabajos |
| 3. Agenda y Asignación | `agenda.py`, `tecnicos.py` | Coordinación de técnicos y carga por técnico |
| 4. Vista del Técnico | `agenda.py` (hoja de ruta) | Audios repetitivos; el técnico ve qué hacer |
| 5. Gestión de Cobros | `cobros.py` | Excel desactualizado y cobros mal registrados |
| 6. Resumen General | `dashboard.py` | Sin visión global del estado del negocio |

---

## Opciones del menú

```
-- Clientes --
1  - Cargar cliente            (alta de un cliente nuevo, con validación de teléfono)
2  - Buscar cliente            (busca por nombre y muestra la dirección)

-- Técnicos --
3  - Cargar técnico
4  - Eliminar técnico

-- Trabajos --
5  - Asignar trabajo           (elige cliente, tipo, técnico, fecha, hora y precio)
6  - Cambiar estado de trabajo (pendiente / en proceso / terminado / cobrado)
7  - Mostrar todos los trabajos
8  - Trabajos pendientes
9  - Trabajos realizados

-- Agenda --
10 - Trabajos del día          (todos los trabajos de una fecha)
11 - Agenda por técnico        ("¿qué tiene Carlos hoy?")
12 - Hoja de ruta del técnico  (vista limpia para un técnico en una fecha)

-- Cobros --
13 - Registrar cobro           (admite pagos parciales; calcula el saldo)

-- Resumen --
14 - Resumen general           (activos, terminados sin cobrar, clientes con deuda)
15 - Resumen de trabajos       (cantidades y totales de plata)
16 - Matriz trabajos por técnico/estado
17 - Técnicos ocupados

0  - Salir
```

El estado de un trabajo sigue el ciclo:
`pendiente → en proceso → terminado → cobrado`. Cuando se marca como **cobrado**
el sistema pide el monto y calcula automáticamente cuánto resta cobrar.

---

## Temas de la materia aplicados

Dónde se ve cada tema dentro del código:

| Tema | Dónde |
|---|---|
| Listas | listas de clientes/técnicos/trabajos en `datos.py` |
| Diccionarios | cada cliente/técnico/trabajo es un diccionario; deuda por cliente en `cobros.py` |
| Tuplas | `TIPOS_TRABAJO` y `ESTADOS_TRABAJO` en `datos.py` (valores fijos) |
| Conjuntos | `tecnicosOcupados()` en `dashboard.py` (evita técnicos repetidos) |
| Funciones | todo el sistema está organizado en funciones |
| Cadena de caracteres | armado de mensajes, `.lower()`, `.split()`, `.isdigit()`, `.ljust()` |
| Expresiones regulares | `validaciones.py` (teléfono, fecha, hora) |
| `map` / `filter` / `lambda` | filtrado de trabajos por estado y totales en `dashboard.py` y `trabajos.py` |
| `reduce` | total adeudado en `dashboard.py` (`trabajosTotales`) |
| Recursividad | `cantidadClientes()` en `clientes.py` y `trabajosDeTecnico()` en `agenda.py` |
| Excepciones | lectura/escritura de archivos en `datos.py` y `try/except` del menú en `main.py` |
| Archivos | persistencia en `.txt` con `open` (modos `"r"`/`"w"`) y `.split(";")` en `datos.py` |
| Matrices | `matrizTrabajosPorTecnicoEstado()` en `dashboard.py` (lista de listas técnico × estado) |
| Test unitarios | `test_taller.py` (módulo `unittest`) |

---

## Supuestos

- El sistema es de uso interno (Oli y la oficina): no hay login por cliente ni
  por técnico.
- No se valida automáticamente la disponibilidad de los técnicos; el sistema
  muestra la carga de cada uno para que la persona decida.
- El precio lo carga Oli a mano; el sistema no lo calcula solo.
- Se admiten pagos parciales en varias tandas; no se distingue el medio de pago.
- No se guarda DNI ni CUIT de los clientes.
- Como los archivos usan `;` para separar los campos, los textos libres (nombre,
  dirección, detalles) no deberían contener ese carácter.
