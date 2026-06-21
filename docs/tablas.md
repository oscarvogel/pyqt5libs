# Tablas reutilizables

Módulo público: `pyqt5libs.ui.tables`

Este módulo centraliza helpers para tablas Qt, especialmente `QTableWidget`.

## Configurar cabeceras

```python
from pyqt5libs.ui.tables import setup_headers

setup_headers(tabla, ["ID", "Nombre", "Estado"])
```

## Cargar filas

```python
from pyqt5libs.ui.tables import load_table

rows = [
    {"id": 1, "nombre": "Cliente A", "estado": "Activo"},
    {"id": 2, "nombre": "Cliente B", "estado": "Inactivo"},
]

load_table(
    tabla,
    rows,
    headers=["ID", "Nombre", "Estado"],
    columns=["id", "nombre", "estado"],
)
```

## Leer selección

```python
from pyqt5libs.ui.tables import current_row_values, current_cell_text

fila = current_row_values(tabla)
id_actual = current_cell_text(tabla, 0)
```

## Funciones disponibles

- `normalize_table_row(row, columns=())`
- `clear_table(table)`
- `setup_headers(table, headers)`
- `append_row(table, row)`
- `load_table(table, rows, headers=(), columns=(), clear=True)`
- `current_row_index(table)`
- `current_row_values(table)`
- `current_cell_text(table, column, default="")`

## Criterio de uso

Usar estos helpers para pantallas simples o nuevas vistas. La grilla histórica del proyecto se mantiene por compatibilidad y puede migrarse gradualmente.
