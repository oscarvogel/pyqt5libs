from pyqt5libs.generators.fields import FieldInfo
from pyqt5libs.generators.lists import build_list_spec, build_list_spec_as_dict, column_from_field


def field(name, kind="string", label=None, primary_key=False):
    return FieldInfo(
        name=name,
        kind=kind,
        label=label or name.capitalize(),
        primary_key=primary_key,
    )


def test_column_from_field_marks_searchable_text_fields():
    column = column_from_field(field("nombre", "string"))

    assert column.name == "nombre"
    assert column.label == "Nombre"
    assert column.visible is True
    assert column.searchable is True
    assert column.primary_key is False


def test_column_from_field_can_hide_primary_key():
    column = column_from_field(field("id", "integer", primary_key=True), visible_primary_key=False)

    assert column.primary_key is True
    assert column.visible is False


def test_build_list_spec_detects_primary_key_and_searchable_fields():
    spec = build_list_spec([
        field("id", "integer", primary_key=True),
        field("nombre", "string"),
        field("activo", "boolean"),
    ])

    assert spec.primary_key == "id"
    assert spec.searchable_fields == ["nombre"]
    assert spec.headers() == ["Id", "Nombre", "Activo"]
    assert spec.field_names() == ["id", "nombre", "activo"]


def test_build_list_spec_hides_unknown_kind():
    spec = build_list_spec([field("custom", "unknown")])

    assert spec.visible_columns() == []
    assert spec.headers() == []
    assert spec.field_names() == []


def test_build_list_spec_as_dict():
    data = build_list_spec_as_dict([
        field("id", "integer", primary_key=True),
        field("nombre", "string"),
    ], visible_primary_key=False)

    assert data["primary_key"] == "id"
    assert data["searchable_fields"] == ["nombre"]
    assert data["columns"][0]["name"] == "id"
    assert data["columns"][0]["visible"] is False
    assert data["columns"][1]["searchable"] is True
