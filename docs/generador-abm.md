# Generador automático de ABM

Issue relacionado: #43

El generador se construye por fases para no romper el ABM histórico.

## Fase 1: introspección de modelos

```python
from pyqt5libs.generators.peewee import inspect_model

fields = inspect_model(Cliente)
```

Cada campo se representa como `FieldInfo`.

## Fase 2: campo a widget

```python
from pyqt5libs.generators.widgets import widget_specs_from_fields

specs = widget_specs_from_fields(fields)
```

Cada widget se representa como `WidgetSpec`.

## Fase 3: especificación de formulario

```python
from pyqt5libs.generators.forms import build_form_spec

form = build_form_spec(specs, columns=2)
```

## Fase 4: especificación de listado

```python
from pyqt5libs.generators.lists import build_list_spec

list_spec = build_list_spec(fields, visible_primary_key=False)
```

## Fase 5: especificación ABM completa

```python
from pyqt5libs.generators.abm import create_abm_spec_from_model

spec = create_abm_spec_from_model(Cliente)
```

## Fase 6: clase ABM generada

La sexta fase crea una clase dinámica compatible con el ABM histórico.

```python
from pyqt5libs.generators.abm import create_abm_from_model

ClientesABM = create_abm_from_model(
    Cliente,
    form_columns=2,
    view_mode="split",
    visible_primary_key=False,
)

ventana = ClientesABM()
ventana.show()
```

La clase generada configura automáticamente:

- `model`
- `titulo`
- `camposAMostrar`
- `ordenBusqueda`
- `campoClave`
- `view_mode`
- `form_layout_mode`
- `form_columns`
- `ArmaCarga()`

## Próximas fases

1. Mejorar creación real de controles por tipo.
2. Cargar combos para claves foráneas.
3. Validaciones automáticas antes de guardar.
4. Ejemplo funcional con modelo Peewee real.
