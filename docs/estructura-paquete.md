# Estructura del paquete

Este documento define la dirección de organización interna de `pyqt5libs`.

## Objetivo

Ordenar progresivamente la librería para que tenga una API pública clara, sin romper compatibilidad con el código histórico existente.

## Estado actual

El repositorio contiene código histórico en carpetas como `libs/` y un paquete principal `pyqt5libs/`.

Por compatibilidad, no se deben mover módulos existentes de forma masiva hasta tener tests y una estrategia de migración.

## Estructura objetivo sugerida

```text
pyqt5libs/
  __init__.py
  ui/
    dialogs.py
    tables.py
    combos.py
    styles.py
    windows.py
  forms/
    validators.py
  db/
    mysql.py
  core/
    config.py
    errors.py
    workers.py
  exporters/
    spreadsheets.py
```

## Reglas de evolución

1. Mantener compatibilidad con imports existentes mientras sea posible.
2. Crear módulos públicos nuevos dentro de `pyqt5libs/`.
3. Evitar imports ficticios o ejemplos que apunten a módulos inexistentes.
4. Documentar cada módulo público nuevo.
5. Agregar tests antes de mover lógica histórica.

## API pública inicial

Por ahora, el paquete expone:

```python
import pyqt5libs
pyqt5libs.__version__
```

Los próximos issues deberán agregar módulos públicos de forma incremental.
