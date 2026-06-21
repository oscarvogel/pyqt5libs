from pyqt5libs.forms import validators


def test_required_validator():
    assert validators.required("Oscar", "Nombre").ok
    result = validators.required("", "Nombre")
    assert not result.ok
    assert result.message == "Nombre es obligatorio"


def test_length_validators_ignore_empty_values():
    assert validators.min_length("", 3).ok
    assert validators.max_length(None, 3).ok


def test_min_and_max_length_validators():
    assert validators.min_length("abcd", 3).ok
    assert not validators.min_length("ab", 3, "Código").ok
    assert validators.max_length("ab", 3).ok
    assert not validators.max_length("abcd", 3, "Código").ok


def test_numeric_and_integer_validators():
    assert validators.numeric("10,5").ok
    assert validators.numeric("10.5").ok
    assert not validators.numeric("abc", "Importe").ok
    assert validators.integer("10").ok
    assert not validators.integer("10.5", "Cantidad").ok


def test_email_validator():
    assert validators.email("oscar@example.com").ok
    assert not validators.email("oscar.example.com").ok


def test_cuit_validator_accepts_valid_cuit_and_rejects_invalid():
    assert validators.cuit("20-12345678-6").ok
    assert not validators.cuit("20-12345678-0").ok
    assert not validators.cuit("123").ok


def test_in_range_validator():
    assert validators.in_range("10", minimum=1, maximum=20).ok
    assert not validators.in_range("0", minimum=1, field_name="Edad").ok
    assert not validators.in_range("21", maximum=20, field_name="Edad").ok
    assert not validators.in_range("abc", field_name="Edad").ok


def test_first_error_returns_first_invalid_result():
    result = validators.first_error(
        validators.required("ok"),
        validators.required("", "Nombre"),
        validators.required("", "Apellido"),
    )
    assert not result.ok
    assert result.message == "Nombre es obligatorio"


def test_all_exports_are_defined():
    assert "ValidationResult" in validators.__all__
    assert "required" in validators.__all__
    assert "email" in validators.__all__
    assert "cuit" in validators.__all__
