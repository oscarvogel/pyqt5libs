# Logging

Módulo público: `pyqt5libs.core.logging`

Permite configurar logs para aplicaciones PyQt y registrar excepciones de forma consistente.

## Configuración básica

```python
from pyqt5libs.core.logging import configure_logging

logger = configure_logging(
    name="mi_app",
    log_file="logs/app.log",
    console=True,
)

logger.info("Aplicación iniciada")
```

## Captura de excepciones

```python
from pyqt5libs.core.logging import capture_exceptions, get_logger

logger = get_logger("mi_app")

@capture_exceptions(logger, message="Error al guardar")
def guardar():
    pass
```

## API disponible

- `configure_logging(...)`
- `get_logger(name=None)`
- `log_exception(logger, message, exc)`
- `capture_exceptions(logger=None, message="Error no controlado", reraise=True)`
