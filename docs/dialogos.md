# Diálogos reutilizables

Módulo público: `pyqt5libs.ui.dialogs`

Este módulo centraliza diálogos comunes de PyQt5 para evitar repetir llamadas directas a `QMessageBox` en cada pantalla.

## Funciones disponibles

- `show_info(message, title="Sistema", parent=None)`
- `show_warning(message, title="Sistema", parent=None)`
- `show_error(message, title="Sistema", parent=None)`
- `ask_yes_no(message, title="Sistema", parent=None)`
- `confirm(message, title="Sistema", parent=None)`

## Ejemplo

```python
from pyqt5libs.ui.dialogs import show_info, show_error, confirm

show_info("Datos guardados correctamente")

if confirm("¿Desea borrar el registro seleccionado?"):
    borrar_registro()

show_error("No se pudo guardar el registro")
```

## Criterio de uso

Usar estos helpers para mensajes simples y confirmaciones generales. Para diálogos complejos con formularios propios, crear widgets o clases específicas.
