# Generador automático de ABM

Issue relacionado: #43

La primera fase agrega introspección de modelos Peewee para obtener metadata neutral de campos.

## API inicial

```python
from pyqt5libs.generators.peewee import inspect_model, inspect_model_as_dict

fields = inspect_model(Cliente)
data = inspect_model_as_dict(Cliente)
```

## Resultado esperado

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

## Próximas fases

1. Campo a widget.
2. Generación automática de formulario.
3. Generación automática de listado.
4. Validaciones automáticas.
5. ABM completo desde modelo.
