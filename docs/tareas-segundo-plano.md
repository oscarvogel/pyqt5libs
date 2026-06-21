# Tareas en segundo plano

Módulo público: `pyqt5libs.core.tasks`

Permite ejecutar funciones largas en un hilo secundario usando una API simple basada en `threading`.

## Uso básico

```python
from pyqt5libs.core.tasks import run_in_background


def proceso_largo():
    return "finalizado"


task = run_in_background(proceso_largo)
result = task.join()

if result.ok:
    print(result.value)
```

## Callbacks

```python
from pyqt5libs.core.tasks import BackgroundTask


def on_success(value):
    print("OK", value)


def on_error(error):
    print("ERROR", error)


def on_done(result):
    print("Terminó", result.ok)


BackgroundTask(
    proceso_largo,
    on_success=on_success,
    on_error=on_error,
    on_done=on_done,
).start()
```

## API disponible

- `TaskResult`
- `BackgroundTask`
- `run_in_background(target, *args, **kwargs)`

## Criterio de uso

Usar para procesos que no deben bloquear la interfaz: importaciones, exportaciones, reportes, consultas pesadas o sincronizaciones.
