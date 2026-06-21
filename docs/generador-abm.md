# Generador automático de ABM

Issue relacionado: #43

El generador se construye por fases para no romper el ABM histórico.

## Fase 1: introspección de modelos

La primera fase agrega introspección de modelos Peewee para obtener metadata neutral de campos.

```python
from pyqt5libs.generators.peewee import inspect_model

fields = inspect_model(Cliente)
```

Cada campo se representa como `FieldInfo`.

## Fase 2: campo a widget

La segunda fase agrega una especificación neutral de widget.

```python
from pyqt5libs.generators.widgets import widget_specs_from_fields

specs = widget_specs_from_fields(fields)
```

Cada widget se representa como `WidgetSpec`.

## Fase 3: especificación de formulario

La tercera fase arma una estructura neutral de formulario desde `WidgetSpec`.

```python
from pyqt5libs.generators.forms import build_form_spec

form = build_form_spec(specs, columns=2)
```

## Fase 4: especificación de listado

La cuarta fase arma una estructura neutral de listado desde `FieldInfo`.

```python
from pyqt5libs.generators.lists import build_list_spec

list_spec = build_list_spec(fields, visible_primary_key=False)
```

## Fase 5: especificación ABM completa

La quinta fase une todo en `ABMSpec`.

```python
from pyqt5libs.generators.abm import create_abm_from_model

spec = create_abm_from_model(
    Cliente,
    form_columns=2,
    view_mode="split",
    visible_primary_key=False,
)
```

Por ahora `create_abm_from_model()` devuelve una especificación neutral. En la próxima fase se podrá convertir esa especificación en una pantalla PyQt real.

## Próximas fases

1. Instanciar widgets PyQt desde `FormSpec`.
2. Instanciar grilla/listado desde `ListSpec`.
3. Conectar `ABMSpec` con `libs/vistas/ABM.py`.
4. Validaciones automáticas.
