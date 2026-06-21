from pyqt5libs.generators.peewee import inspect_field, inspect_model, inspect_model_as_dict, map_peewee_field_kind


class CharField:
    def __init__(self):
        self.name = "nombre"
        self.column_name = "nombre"
        self.verbose_name = "Nombre"
        self.null = False
        self.primary_key = False
        self.default = None
        self.max_length = 100
        self.choices = None


class AutoField:
    def __init__(self):
        self.name = "id"
        self.column_name = "id"
        self.verbose_name = None
        self.null = False
        self.primary_key = True
        self.default = None
        self.max_length = None
        self.choices = None


class BooleanField:
    def __init__(self):
        self.name = "activo"
        self.column_name = "activo"
        self.verbose_name = None
        self.null = True
        self.primary_key = False
        self.default = True
        self.max_length = None
        self.choices = None


class UnknownField:
    name = "custom"
    column_name = "custom"
    verbose_name = None
    null = True
    primary_key = False
    default = None
    max_length = None
    choices = None


class ModelMeta:
    sorted_fields = [AutoField(), CharField(), BooleanField()]


class FakeModel:
    _meta = ModelMeta()


def test_map_peewee_field_kind():
    assert map_peewee_field_kind(CharField()) == "string"
    assert map_peewee_field_kind(AutoField()) == "integer"
    assert map_peewee_field_kind(BooleanField()) == "boolean"
    assert map_peewee_field_kind(UnknownField()) == "unknown"


def test_inspect_field():
    field = inspect_field(CharField())

    assert field.name == "nombre"
    assert field.kind == "string"
    assert field.label == "Nombre"
    assert field.required is True
    assert field.primary_key is False
    assert field.max_length == 100


def test_inspect_model_uses_sorted_fields():
    fields = inspect_model(FakeModel)

    assert [field.name for field in fields] == ["id", "nombre", "activo"]
    assert [field.kind for field in fields] == ["integer", "string", "boolean"]
    assert fields[0].primary_key is True
    assert fields[2].required is False


def test_inspect_model_as_dict():
    fields = inspect_model_as_dict(FakeModel)

    assert fields[0]["name"] == "id"
    assert fields[1]["max_length"] == 100
    assert fields[2]["default"] is True
