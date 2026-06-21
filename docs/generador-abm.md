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

La clase generada configura automáticamente `model`, `titulo`, `camposAMostrar`, `ordenBusqueda`, `campoClave`, `view_mode`, `form_layout_mode`, `form_columns` y `ArmaCarga()`.

## AutoABM Producción: validaciones automáticas

```python
result = ventana.ValidateValues({
    "nombre": "Oscar",
    "email": "oscar@example.com",
})

if not result.ok:
    print(result.first_error().message)
```

Reglas iniciales:

- requerido
- longitud máxima
- entero
- numérico
- email si el campo parece email/correo
- CUIT si el campo se llama cuit/cuil

## AutoABM Producción: creación y edición

La clase generada expone métodos para crear y modificar registros.

```python
result = ventana.CreateRecord({
    "nombre": "Oscar",
    "email": "oscar@example.com",
})

if result.ok:
    print(result.record)
```

```python
result = ventana.UpdateRecord(cliente, {
    "nombre": "Oscar actualizado",
})
```

Estos métodos validan antes de guardar y convierten tipos básicos como enteros, decimales, booleanos y strings vacíos.

## AutoABM Producción: borrado automático

La clase generada expone `RemoveRecord(record)` y `CanRemove(record)`.

```python
result = ventana.RemoveRecord(cliente)

if result.ok:
    print(result.deleted_count)
```

`CanRemove()` puede sobrescribirse en una clase hija para aplicar reglas de negocio.

## AutoABM UX: formulario responsive real

El formulario del panel derecho usa un contenedor con scroll, panel interno y controles expansibles.

Incluye:

- `QScrollArea` para formularios largos;
- `formPanelABM` como contenedor del detalle;
- campos con label superior en modo responsive;
- ancho mínimo configurable con `form_field_min_width`;
- botones Guardar/Cancelar con ancho expansible;
- márgenes definidos por `form_panel_margins`.

## Ejemplo funcional completo

Hay un ejemplo completo en:

```text
examples/autoabm_clientes/
```

Ejecutar desde la raíz del proyecto:

```bash
python examples/autoabm_clientes/main.py
```

El ejemplo usa Peewee, SQLite y PyQt5. Crea la base `clientes.db`, inserta datos iniciales y abre una ventana AutoABM generada desde el modelo `Cliente`.

## Próximas fases

1. Vista master/detail moderna.
2. Toolbar moderna.
3. Tabla moderna.
