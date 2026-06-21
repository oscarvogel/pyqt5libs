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

Cada widget se representa como `WidgetSpec`.

## Fase 3: especificación de formulario

La tercera fase arma una estructura neutral de formulario desde `WidgetSpec`.

```python
from pyqt5libs.generators.forms import build_form_spec

form = build_form_spec(specs, columns=2)
```

Esto permite conocer el orden, fila, columna, tipo de widget y opciones de cada campo antes de crear widgets PyQt reales.

## Próximas fases

1. Instanciar widgets PyQt desde `FormSpec`.
2. Generación automática de listado.
3. Validaciones automáticas.
4. ABM completo desde modelo.
