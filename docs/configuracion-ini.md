# Configuración INI

Módulo público: `pyqt5libs.core.config`

Este módulo permite leer y escribir archivos INI sin depender de rutas fijas del proyecto.

## Guardar configuración

```python
from pyqt5libs.core.config import save_ini

save_ini("config/app.ini", {
    "database": {
        "host": "localhost",
        "port": 3306,
    },
    "app": {
        "debug": "si",
    },
})
```

## Leer configuración

```python
from pyqt5libs.core.config import load_ini

config = load_ini("config/app.ini")

host = config.get("database", "host", default="localhost")
port = config.get_int("database", "port", default=3306)
debug = config.get_bool("app", "debug", default=False)
```

## API disponible

- `IniConfig(path, encoding="utf-8")`
- `load_ini(path, encoding="utf-8")`
- `save_ini(path, data, encoding="utf-8")`

## Métodos principales

- `read()`
- `save()`
- `get(section, option, default=None)`
- `get_int(section, option, default=None)`
- `get_float(section, option, default=None)`
- `get_bool(section, option, default=None)`
- `set(section, option, value)`
- `update_section(section, values)`
- `as_dict()`

## Criterio de uso

Usar este módulo para nuevas aplicaciones o para migrar gradualmente configuraciones históricas basadas en INI.
