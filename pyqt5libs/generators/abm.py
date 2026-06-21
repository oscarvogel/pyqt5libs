"""Ensamblador neutral para generar especificaciones ABM.

Esta fase une introspección de campos, widgets, formulario y listado en un
contrato único. Aún no instancia la pantalla PyQt real.
"""

from dataclasses import dataclass
from typing import Any, Optional

from pyqt5libs.generators.forms import FormSpec, build_form_spec
from pyqt5libs.generators.lists import ListSpec, build_list_spec
from pyqt5libs.generators.peewee import inspect_model
from pyqt5libs.generators.widgets import WidgetSpec, widget_specs_from_fields


@dataclass(frozen=True)
class ABMSpec:
    """Especificación completa de un ABM automático."""

    model: Any
    title: str
    fields: list
    widgets: list
    form: FormSpec
    list: ListSpec
    view_mode: str = "tabs"
    form_columns: int = 1

    def as_dict(self):
        return {
            "title": self.title,
            "view_mode": self.view_mode,
            "form_columns": self.form_columns,
            "fields": [field.as_dict() for field in self.fields],
            "widgets": [widget.as_dict() for widget in self.widgets],
            "form": self.form.as_dict(),
            "list": self.list.as_dict(),
        }


def default_title_for_model(model) -> str:
    """Obtiene un título legible para el ABM desde el modelo."""
    meta = getattr(model, "_meta", None)
    table_name = getattr(meta, "table_name", None)
    if table_name:
        return str(table_name).replace("_", " ").title()
    return getattr(model, "__name__", "Registros")


def create_abm_spec_from_model(
    model,
    *,
    title: Optional[str] = None,
    form_columns: int = 1,
    view_mode: str = "tabs",
    include_read_only_fields: bool = True,
    visible_primary_key: bool = True,
) -> ABMSpec:
    """Crea una especificación ABM completa desde un modelo Peewee."""
    fields = inspect_model(model)
    widgets = widget_specs_from_fields(fields)
    form = build_form_spec(widgets, columns=form_columns, include_read_only=include_read_only_fields)
    list_spec = build_list_spec(fields, visible_primary_key=visible_primary_key)

    return ABMSpec(
        model=model,
        title=title or default_title_for_model(model),
        fields=fields,
        widgets=widgets,
        form=form,
        list=list_spec,
        view_mode=view_mode,
        form_columns=max(1, int(form_columns or 1)),
    )


def create_abm_spec_as_dict(model, **kwargs):
    """Devuelve una especificación ABM serializable."""
    return create_abm_spec_from_model(model, **kwargs).as_dict()


# Alias corto para la API pública futura.
def create_abm_from_model(model, **kwargs) -> ABMSpec:
    """Alias inicial: por ahora devuelve `ABMSpec`, no una pantalla PyQt."""
    return create_abm_spec_from_model(model, **kwargs)


__all__ = [
    "ABMSpec",
    "default_title_for_model",
    "create_abm_spec_from_model",
    "create_abm_spec_as_dict",
    "create_abm_from_model",
]
