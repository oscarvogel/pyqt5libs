# Combos reutilizables

Módulo público: `pyqt5libs.ui.combos`

Este módulo centraliza helpers para cargar y leer `QComboBox`.

## Cargar opciones

```python
from pyqt5libs.ui.combos import load_combo

load_combo(combo_estado, [
    ("A", "Activo"),
    ("I", "Inactivo"),
], placeholder="Seleccione estado")
```

## Cargar desde diccionarios

```python
load_combo(
    combo_cliente,
    clientes,
    text_key="razon_social",
    value_key="id",
    placeholder="Seleccione cliente",
)
```

## Leer selección

```python
from pyqt5libs.ui.combos import selected_data, selected_text

cliente_id = selected_data(combo_cliente)
cliente_nombre = selected_text(combo_cliente)
```

## Seleccionar valor

```python
from pyqt5libs.ui.combos import select_by_data

select_by_data(combo_cliente, cliente_id)
```

## Formatos soportados

- String simple: `"Activo"`
- Tupla/lista: `(valor, texto)`
- Diccionario: `{"id": 1, "nombre": "Cliente"}`
- Objeto con atributos configurables
