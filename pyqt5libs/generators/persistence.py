"""Persistencia automática para AutoABM.

Funciones pequeñas y testeables para crear y actualizar registros usando la
metadata generada por `ABMSpec`.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Any, Dict, Optional

from pyqt5libs.generators.validation import FormValidationResult, validate_values


@dataclass(frozen=True)
class SaveResult:
    """Resultado de crear o actualizar un registro."""

    ok: bool
    record: Any = None
    validation: Optional[FormValidationResult] = None
    error: Optional[BaseException] = None


def _field_map(spec):
    return {field.name: field for field in spec.fields}


def convert_value(field_info, value):
    """Convierte un valor de formulario según el tipo neutral del campo."""
    if value == "":
        return None
    if value is None:
        return None

    kind = field_info.kind
    if kind == "integer":
        return int(value)
    if kind in {"float"}:
        return float(str(value).replace(",", "."))
    if kind == "decimal":
        return Decimal(str(value).replace(",", "."))
    if kind == "boolean":
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in {"1", "true", "yes", "si", "sí", "on"}
    return value


def clean_values(spec, values: Dict[str, Any]) -> Dict[str, Any]:
    """Filtra y convierte valores usando los campos de la especificación."""
    fields = _field_map(spec)
    cleaned = {}
    for name, value in values.items():
        field_info = fields.get(name)
        if field_info is None:
            continue
        if field_info.primary_key:
            continue
        cleaned[name] = convert_value(field_info, value)
    return cleaned


def create_record(spec, values: Dict[str, Any], validation_rules=None) -> SaveResult:
    """Crea un registro del modelo asociado al `ABMSpec`."""
    validation = validate_values(values, validation_rules or [])
    if not validation.ok:
        return SaveResult(ok=False, validation=validation)

    try:
        cleaned = clean_values(spec, values)
        record = spec.model.create(**cleaned)
        return SaveResult(ok=True, record=record, validation=validation)
    except Exception as exc:
        return SaveResult(ok=False, validation=validation, error=exc)


def update_record(spec, record, values: Dict[str, Any], validation_rules=None) -> SaveResult:
    """Actualiza un registro existente del modelo asociado al `ABMSpec`."""
    validation = validate_values(values, validation_rules or [])
    if not validation.ok:
        return SaveResult(ok=False, record=record, validation=validation)

    try:
        cleaned = clean_values(spec, values)
        for name, value in cleaned.items():
            setattr(record, name, value)
        record.save()
        return SaveResult(ok=True, record=record, validation=validation)
    except Exception as exc:
        return SaveResult(ok=False, record=record, validation=validation, error=exc)


__all__ = [
    "SaveResult",
    "convert_value",
    "clean_values",
    "create_record",
    "update_record",
]
