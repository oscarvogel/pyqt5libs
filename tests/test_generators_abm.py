from pyqt5libs.generators.abm import create_abm_from_model, create_abm_spec_as_dict, default_title_for_model


class AutoField:
    name = "id"
    column_name = "id"
    verbose_name = None
    null = False
    primary_key = True
    default = None
    max_length = None
    choices = None


class CharField:
    name = "nombre"
    column_name = "nombre"
    verbose_name = "Nombre"
    null = False
    primary_key = False
    default = None
    max_length = 100
    choices = None


class BooleanField:
    name = "activo"
    column_name = "activo"
    verbose_name = None
    null = True
    primary_key = False
    default = True
    max_length = None
    choices = None


class ModelMeta:
    table_name = "clientes"
    sorted_fields = [AutoField(), CharField(), BooleanField()]


class Cliente:
    _meta = ModelMeta()


def test_default_title_for_model_uses_table_name():
    assert default_title_for_model(Cliente) == "Clientes"


def test_create_abm_from_model_builds_complete_spec():
    spec = create_abm_from_model(Cliente, form_columns=2, view_mode="split", visible_primary_key=False)

    assert spec.title == "Clientes"
    assert spec.view_mode == "split"
    assert spec.form_columns == 2
    assert [field.name for field in spec.fields] == ["id", "nombre", "activo"]
    assert [widget.widget_type for widget in spec.widgets] == ["spin_box", "line_edit", "check_box"]
    assert spec.form.columns == 2
    assert spec.list.primary_key == "id"
    assert spec.list.searchable_fields == ["nombre"]
    assert spec.list.columns[0].visible is False


def test_create_abm_from_model_can_exclude_read_only_fields_from_form():
    spec = create_abm_from_model(Cliente, include_read_only_fields=False)

    assert [field.name for field in spec.form.fields] == ["nombre", "activo"]


def test_create_abm_spec_as_dict():
    data = create_abm_spec_as_dict(Cliente, title="Clientes activos")

    assert data["title"] == "Clientes activos"
    assert data["fields"][0]["name"] == "id"
    assert data["widgets"][1]["field_name"] == "nombre"
    assert data["form"]["fields"][1]["name"] == "nombre"
    assert data["list"]["primary_key"] == "id"
