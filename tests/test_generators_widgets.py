from pyqt5libs.generators.fields import FieldInfo
from pyqt5libs.generators.widgets import (
    WidgetSpec,
    widget_options_for_field,
    widget_spec_from_field,
    widget_specs_as_dict,
    widget_specs_from_fields,
    widget_type_for_field,
)


def field(name="campo", kind="string", **kwargs):
    return FieldInfo(name=name, kind=kind, label=name.capitalize(), **kwargs)


def test_widget_type_for_known_field_kinds():
    assert widget_type_for_field(field(kind="string")) == "line_edit"
    assert widget_type_for_field(field(kind="text")) == "text_edit"
    assert widget_type_for_field(field(kind="integer")) == "spin_box"
    assert widget_type_for_field(field(kind="float")) == "double_spin_box"
    assert widget_type_for_field(field(kind="decimal")) == "double_spin_box"
    assert widget_type_for_field(field(kind="boolean")) == "check_box"
    assert widget_type_for_field(field(kind="date")) == "date_edit"
    assert widget_type_for_field(field(kind="datetime")) == "datetime_edit"
    assert widget_type_for_field(field(kind="time")) == "time_edit"
    assert widget_type_for_field(field(kind="foreign_key")) == "combo_box"


def test_widget_type_for_unknown_kind_falls_back_to_line_edit():
    assert widget_type_for_field(field(kind="custom")) == "line_edit"


def test_widget_options_include_metadata():
    info = field(max_length=100, default="Activo", choices=[("A", "Activo")])

    assert widget_options_for_field(info) == {
        "max_length": 100,
        "default": "Activo",
        "choices": [("A", "Activo")],
    }


def test_widget_spec_from_field():
    info = field(name="id", kind="integer", required=True, primary_key=True)

    spec = widget_spec_from_field(info)

    assert isinstance(spec, WidgetSpec)
    assert spec.field_name == "id"
    assert spec.widget_type == "spin_box"
    assert spec.required is True
    assert spec.read_only is True


def test_widget_specs_from_fields():
    specs = widget_specs_from_fields([
        field(name="nombre", kind="string"),
        field(name="activo", kind="boolean"),
    ])

    assert [spec.widget_type for spec in specs] == ["line_edit", "check_box"]


def test_widget_specs_as_dict():
    specs = widget_specs_as_dict([field(name="fecha", kind="date")])

    assert specs == [
        {
            "field_name": "fecha",
            "widget_type": "date_edit",
            "label": "Fecha",
            "required": False,
            "read_only": False,
            "options": {},
        }
    ]
