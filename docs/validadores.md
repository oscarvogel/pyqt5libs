# Validadores reutilizables

Módulo público: `pyqt5libs.forms.validators`

Este módulo contiene validadores simples para formularios administrativos. No dependen de widgets PyQt, por lo que pueden usarse y probarse fácilmente.

## Resultado estándar

Todas las validaciones devuelven un `ValidationResult`:

```python
ValidationResult(ok=True, message="")
ValidationResult(ok=False, message="Nombre es obligatorio")
```

## Ejemplo básico

```python
from pyqt5libs.forms.validators import required, email, first_error

result = first_error(
    required(nombre, "Nombre"),
    email(correo, "Correo"),
)

if not result.ok:
    print(result.message)
```

## Validadores disponibles

- `required(value, field_name="Campo")`
- `min_length(value, length, field_name="Campo")`
- `max_length(value, length, field_name="Campo")`
- `numeric(value, field_name="Campo")`
- `integer(value, field_name="Campo")`
- `email(value, field_name="Email")`
- `cuit(value, field_name="CUIT")`
- `in_range(value, minimum=None, maximum=None, field_name="Campo")`
- `first_error(*results)`

## Uso recomendado en ABM

En una pantalla ABM, validar antes de guardar y mostrar `result.message` al usuario si falla.
