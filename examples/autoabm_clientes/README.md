# Ejemplo AutoABM Clientes

Ejemplo funcional mínimo para probar el generador automático de ABM con Peewee, SQLite y PyQt5.

## Qué demuestra

- Definición de modelo Peewee.
- Creación de base SQLite local.
- Datos iniciales de prueba.
- Generación de una clase ABM con `create_abm_from_model()`.
- Configuración de columnas, formulario responsive y modo split.
- Uso directo de métodos de producción:
  - `ValidateValues(values)`
  - `CreateRecord(values)`
  - `UpdateRecord(record, values)`
  - `RemoveRecord(record)`

## Ejecutar

Desde la raíz del proyecto:

```bash
python examples/autoabm_clientes/main.py
```

El ejemplo crea automáticamente `clientes.db` dentro de esta carpeta.

## Nota

Este ejemplo está pensado como prueba de integración manual. Los tests unitarios del generador siguen usando modelos fake para no depender de una UI real en CI.
