from pyqt5libs.generators.fields import FieldInfo
from pyqt5libs.generators.validation import (
    is_cuit_field,
    is_email_field,
    validate_values,
    validation_rules_for_field,
    validation_rules_for_fields,
)


def field(name, kind="string", label=None, required=False, primary_key=False, max_length=None):
    return FieldInfo(
        name=name,
        kind=kind,
        label=label or name.capitalize(),
        required=required,
        primary_key=primary_key,
        max_length=max_length,
    )


def rule_names(rules):
    return [rule.name for rule in rules]


def test_email_and_cuit_detection():
    assert is_email_field(field("email"))
    assert is_email_field(field("correo"))
    assert is_cuit_field(field("cuit"))
    assert is_cuit_field(field("cuil"))


def test_validation_rules_for_required_and_max_length():
    rules = validation_rules_for_field(field("nombre", required=True, max_length=5))

    assert rule_names(rules) == ["required", "max_length"]


def test_validation_rules_for_numeric_types():
    assert rule_names(validation_rules_for_field(field("edad", kind="integer"))) == ["integer"]
    assert rule_names(validation_rules_for_field(field("importe", kind="decimal"))) == ["numeric"]


def test_validation_rules_for_email_and_cuit():
    assert "email" in rule_names(validation_rules_for_field(field("email")))
    assert "cuit" in rule_names(validation_rules_for_field(field("cuit")))


def test_primary_key_is_not_required_or_integer_validated():
    rules = validation_rules_for_field(field("id", kind="integer", required=True, primary_key=True))

    assert rule_names(rules) == []


def test_validate_values_returns_errors():
    rules = validation_rules_for_fields([
        field("nombre", required=True),
        field("email"),
        field("edad", kind="integer"),
    ])

    result = validate_values({"nombre": "", "email": "mal", "edad": "10.5"}, rules)

    assert not result.ok
    assert [error.field_name for error in result.errors] == ["nombre", "email", "edad"]
    assert result.first_error().field_name == "nombre"


def test_validate_values_accepts_valid_data():
    rules = validation_rules_for_fields([
        field("nombre", required=True, max_length=20),
        field("email"),
        field("edad", kind="integer"),
    ])

    result = validate_values({"nombre": "Oscar", "email": "oscar@example.com", "edad": "53"}, rules)

    assert result.ok
    assert result.errors == []
