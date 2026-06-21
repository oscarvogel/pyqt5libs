# Generador automático de ABM

Issue relacionado: #43

El generador se construye por fases para no romper el ABM histórico.

## Fase 1: introspección de modelos

La primera fase agrega introspección de modelos Peewee para obtener metadata neutral de campos.

```python
from pyqt5libs.generators.peewee import inspect_model, inspect_model_as_dict

fields = inspect_model(Cliente)
data = inspect_model_as_dict(Cliente)
```

Cada campo se representa como `FieldInfo`:

```python
FieldInfo(
    name="nombre",
    kind="string",
    label="Nombre",
    required=True,
    primary_key=False,
    max_length=100,
)
```

## Fase 2: campo a widget

La segunda fase agrega una especificación neutral de widget.

```python
from pyqt5libs.generators.peewee import inspect_model
from pyqt5libs.generators.widgets import widget_specs_from_fields

fields = inspect_model(Cliente)
specs = widget_specs_from_fields(fields)
```

Cada widget se representa como `WidgetSpec`:

```python
WidgetSpec(
    field_name="nombre",
    widget_type="line_edit",
    label="Nombre",
    required=True,
    read_only=False,
)
```

## Tipos básicos detectados

- `integer`
- `float`
- `decimal`
- `string`
- `text`
- `boolean`
- `date`
- `datetime`
- `time`
- `foreign_key`
- `unknown`

## Mapeo inicial a widgets

- `string` -> `line_edit`
- `text` -> `text_edit`
- `integer` -> `spin_box`
- `float` -> `double_spin_box`
- `decimal` -> `double_spin_box`
- `boolean` -> `check_box`
- `date` -> `date_edit`
- `datetime` -> `datetime_edit`
- `time` -> `time_edit`
- `foreign_key` -> `combo_box`
- `unknown` -> `line_edit`

## Próximas fases

1. Instanciar widgets PyQt desde `WidgetSpec`.
2. Generación automática de formulario.
3. Generación automática de listado.
4. Validaciones automáticas.
5. ABM completo desde modelo.
