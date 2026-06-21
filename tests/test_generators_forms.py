from pyqt5libs.generators.forms import build_form_spec, build_form_spec_as_dict, form_field_from_widget_spec
from pyqt5libs.generators.widgets import WidgetSpec


def make_widget(name, widget_type="line_edit", required=False, read_only=False, options=None):
    return WidgetSpec(
        field_name=name,
        widget_type=widget_type,
        label=name.capitalize(),
        required=required,
        read_only=read_only,
        options=options or {},
    )


def test_form_field_from_widget_spec():
    spec = make_widget("nombre", required=True, options={"max_length": 100})
    field = form_field_from_widget_spec(spec, row=1, column=2)

    assert field.name == "nombre"
    assert field.label == "Nombre"
    assert field.widget_type == "line_edit"
    assert field.required is True
    assert field.row == 1
    assert field.column == 2
    assert field.options == {"max_length": 100}


def test_build_form_spec_single_column():
    form = build_form_spec([
        make_widget("id", "spin_box", read_only=True),
        make_widget("nombre"),
        make_widget("activo", "check_box"),
    ])

    assert form.columns == 1
    assert [(field.name, field.row, field.column) for field in form.fields] == [
        ("id", 0, 0),
        ("nombre", 1, 0),
        ("activo", 2, 0),
    ]


def test_build_form_spec_two_columns():
    form = build_form_spec([
        make_widget("nombre"),
        make_widget("cuit"),
        make_widget("activo", "check_box"),
    ], columns=2)

    assert [(field.name, field.row, field.column) for field in form.fields] == [
        ("nombre", 0, 0),
        ("cuit", 0, 1),
        ("activo", 1, 0),
    ]


def test_build_form_spec_can_exclude_read_only_fields():
    form = build_form_spec([
        make_widget("id", "spin_box", read_only=True),
        make_widget("nombre"),
    ], include_read_only=False)

    assert [field.name for field in form.fields] == ["nombre"]


def test_form_spec_field_map():
    form = build_form_spec([make_widget("nombre"), make_widget("activo", "check_box")])

    assert set(form.field_map()) == {"nombre", "activo"}
    assert form.field_map()["activo"].widget_type == "check_box"


def test_build_form_spec_as_dict():
    data = build_form_spec_as_dict([make_widget("fecha", "date_edit")], columns=2)

    assert data["columns"] == 2
    assert data["fields"][0]["name"] == "fecha"
    assert data["fields"][0]["widget_type"] == "date_edit"
