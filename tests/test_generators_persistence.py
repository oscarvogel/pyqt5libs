from decimal import Decimal

from pyqt5libs.generators.abm import create_abm_spec_from_model
from pyqt5libs.generators.persistence import clean_values, convert_value, create_record, remove_record, update_record
from pyqt5libs.generators.validation import validation_rules_for_fields


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


class IntegerField:
    name = "edad"
    column_name = "edad"
    verbose_name = "Edad"
    null = True
    primary_key = False
    default = None
    max_length = None
    choices = None


class DecimalField:
    name = "saldo"
    column_name = "saldo"
    verbose_name = "Saldo"
    null = True
    primary_key = False
    default = None
    max_length = None
    choices = None


class BooleanField:
    name = "activo"
    column_name = "activo"
    verbose_name = "Activo"
    null = True
    primary_key = False
    default = True
    max_length = None
    choices = None


class FakeRecord:
    def __init__(self, **values):
        self.__dict__.update(values)
        self.saved = False
        self.removed = False

    def save(self):
        self.saved = True
        return 1

    def delete_instance(self):
        self.removed = True
        return 1


class ModelMeta:
    table_name = "clientes"
    sorted_fields = [AutoField(), CharField(), IntegerField(), DecimalField(), BooleanField()]


class Cliente:
    _meta = ModelMeta()
    created_values = None

    @classmethod
    def create(cls, **values):
        cls.created_values = values
        return FakeRecord(**values)


def spec_and_rules():
    spec = create_abm_spec_from_model(Cliente)
    return spec, validation_rules_for_fields(spec.fields)


def test_convert_value_by_field_kind():
    spec, _ = spec_and_rules()
    fields = {field.name: field for field in spec.fields}

    assert convert_value(fields["edad"], "53") == 53
    assert convert_value(fields["saldo"], "10,5") == Decimal("10.5")
    assert convert_value(fields["activo"], "si") is True
    assert convert_value(fields["nombre"], "Oscar") == "Oscar"
    assert convert_value(fields["nombre"], "") is None


def test_clean_values_skips_unknown_and_primary_key():
    spec, _ = spec_and_rules()

    cleaned = clean_values(spec, {"id": 1, "nombre": "Oscar", "edad": "53", "extra": "x"})

    assert cleaned == {"nombre": "Oscar", "edad": 53}


def test_create_record_validates_and_creates_model_record():
    spec, rules = spec_and_rules()

    result = create_record(spec, {"nombre": "Oscar", "edad": "53", "saldo": "10.5"}, rules)

    assert result.ok
    assert result.record.nombre == "Oscar"
    assert Cliente.created_values["edad"] == 53
    assert Cliente.created_values["saldo"] == Decimal("10.5")


def test_create_record_returns_validation_error():
    spec, rules = spec_and_rules()

    result = create_record(spec, {"nombre": ""}, rules)

    assert not result.ok
    assert result.validation is not None
    assert result.validation.first_error().field_name == "nombre"


def test_update_record_sets_values_and_saves():
    spec, rules = spec_and_rules()
    record = FakeRecord(nombre="Viejo", edad=10)

    result = update_record(spec, record, {"nombre": "Nuevo", "edad": "53"}, rules)

    assert result.ok
    assert record.nombre == "Nuevo"
    assert record.edad == 53
    assert record.saved is True


def test_remove_record_uses_delete_instance():
    record = FakeRecord(nombre="Oscar")

    result = remove_record(record)

    assert result.ok
    assert result.deleted_count == 1
    assert record.removed is True


def test_remove_record_handles_missing_record():
    result = remove_record(None)

    assert not result.ok
    assert result.message == "No hay registro para borrar"
