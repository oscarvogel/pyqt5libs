from pyqt5libs.generators.fields import FieldInfo, normalize_label


def test_normalize_label():
    assert normalize_label("razon_social") == "Razon social"
    assert normalize_label(" nombre ") == "Nombre"


def test_field_info_as_dict_excludes_raw_field():
    field = FieldInfo(
        name="nombre",
        kind="string",
        label="Nombre",
        required=True,
        max_length=100,
        raw_field=object(),
    )

    data = field.as_dict()

    assert data["name"] == "nombre"
    assert data["kind"] == "string"
    assert data["label"] == "Nombre"
    assert data["required"] is True
    assert data["max_length"] == 100
    assert "raw_field" not in data
