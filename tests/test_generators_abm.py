from pyqt5libs.generators.abm import (
    create_abm_class_from_model,
    create_abm_class_from_spec,
    create_abm_from_model,
    create_abm_spec_as_dict,
    create_abm_spec_from_model,
    default_title_for_model,
)


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


class EmailField:
    name = "email"
    column_name = "email"
    verbose_name = "Email"
    null = True
    primary_key = False
    default = None
    max_length = 120
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
    sorted_fields = [AutoField(), CharField(), EmailField(), BooleanField()]


class Cliente:
    _meta = ModelMeta()
    created_values = None

    @classmethod
    def create(cls, **values):
        cls.created_values = values
        return FakeRecord(**values)


class FakeRecord:
    def __init__(self, **values):
        self.__dict__.update(values)
        self.saved = False

    def save(self):
        self.saved = True
        return 1


class FakeBaseABM:
    def __init__(self):
        self.entries = []

    def ArmaEntrada(self, nombre, **kwargs):
        self.entries.append((nombre, kwargs))


def test_default_title_for_model_uses_table_name():
    assert default_title_for_model(Cliente) == "Clientes"


def test_create_abm_spec_from_model_builds_complete_spec():
    spec = create_abm_spec_from_model(Cliente, form_columns=2, view_mode="split", visible_primary_key=False)

    assert spec.title == "Clientes"
    assert spec.view_mode == "split"
    assert spec.form_columns == 2
    assert [field.name for field in spec.fields] == ["id", "nombre", "email", "activo"]
    assert [widget.widget_type for widget in spec.widgets] == ["spin_box", "line_edit", "line_edit", "check_box"]
    assert spec.form.columns == 2
    assert spec.list.primary_key == "id"
    assert spec.list.searchable_fields == ["nombre", "email"]
    assert spec.list.columns[0].visible is False


def test_create_abm_spec_from_model_can_exclude_read_only_fields_from_form():
    spec = create_abm_spec_from_model(Cliente, include_read_only_fields=False)

    assert [field.name for field in spec.form.fields] == ["nombre", "email", "activo"]


def test_create_abm_spec_as_dict():
    data = create_abm_spec_as_dict(Cliente, title="Clientes activos")

    assert data["title"] == "Clientes activos"
    assert data["fields"][0]["name"] == "id"
    assert data["widgets"][1]["field_name"] == "nombre"
    assert data["form"]["fields"][1]["name"] == "nombre"
    assert data["list"]["primary_key"] == "id"


def test_create_abm_class_from_spec_configures_legacy_abm_attributes():
    spec = create_abm_spec_from_model(Cliente, form_columns=2, view_mode="split")
    cls = create_abm_class_from_spec(spec, base_class=FakeBaseABM, class_name="ClientesABM")

    assert issubclass(cls, FakeBaseABM)
    assert cls.__name__ == "ClientesABM"
    assert cls.generated_spec == spec
    assert cls.model is Cliente
    assert cls.titulo == "Clientes"
    assert cls.view_mode == "split"
    assert cls.form_layout_mode == "two_columns"
    assert cls.form_columns == 2
    assert [field.name for field in cls.camposAMostrar] == ["id", "nombre", "email", "activo"]
    assert [field.name for field in cls.ordenBusqueda] == ["nombre", "email"]
    assert cls.campoClave.name == "id"
    assert [rule.name for rule in cls.validation_rules] == ["required", "max_length", "max_length", "email"]


def test_generated_abm_validates_values():
    cls = create_abm_class_from_model(Cliente, base_class=FakeBaseABM, class_name="ClientesABM")
    instance = cls()

    invalid_result = instance.ValidateValues({"nombre": "", "email": "mal"})
    valid_result = instance.ValidateValues({"nombre": "Oscar", "email": "oscar@example.com"})

    assert not invalid_result.ok
    assert [error.field_name for error in invalid_result.errors] == ["nombre", "email"]
    assert valid_result.ok


def test_generated_abm_creates_record():
    cls = create_abm_class_from_model(Cliente, base_class=FakeBaseABM, class_name="ClientesABM")
    instance = cls()

    result = instance.CreateRecord({"nombre": "Oscar", "email": "oscar@example.com", "activo": "si"})

    assert result.ok
    assert result.record.nombre == "Oscar"
    assert Cliente.created_values["activo"] is True


def test_generated_abm_updates_record():
    cls = create_abm_class_from_model(Cliente, base_class=FakeBaseABM, class_name="ClientesABM")
    instance = cls()
    record = FakeRecord(nombre="Viejo", email="viejo@example.com")

    result = instance.UpdateRecord(record, {"nombre": "Nuevo", "email": "nuevo@example.com"})

    assert result.ok
    assert record.nombre == "Nuevo"
    assert record.email == "nuevo@example.com"
    assert record.saved is True


def test_create_abm_class_from_model_returns_generated_class():
    cls = create_abm_class_from_model(Cliente, base_class=FakeBaseABM, class_name="ClientesABM")

    assert issubclass(cls, FakeBaseABM)
    assert cls.__name__ == "ClientesABM"
    assert cls.titulo == "Clientes"


def test_create_abm_from_model_alias_returns_generated_class():
    cls = create_abm_from_model(Cliente, base_class=FakeBaseABM)

    assert issubclass(cls, FakeBaseABM)
    assert cls.model is Cliente
