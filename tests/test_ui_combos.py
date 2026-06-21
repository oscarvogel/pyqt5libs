from dataclasses import dataclass

from pyqt5libs.ui import combos


@dataclass
class ComboOption:
    value: int
    text: str


def test_normalize_combo_item_from_string():
    assert combos.normalize_combo_item("Activo") == ("Activo", "Activo")


def test_normalize_combo_item_from_tuple():
    assert combos.normalize_combo_item((1, "Activo")) == ("Activo", 1)


def test_normalize_combo_item_from_single_value_tuple():
    assert combos.normalize_combo_item((1,)) == ("1", 1)


def test_normalize_combo_item_from_dict():
    item = {"id": 10, "name": "Cliente"}
    assert combos.normalize_combo_item(item, text_key="name", value_key="id") == ("Cliente", 10)


def test_normalize_combo_item_from_object():
    item = ComboOption(value=20, text="Proveedor")
    assert combos.normalize_combo_item(item) == ("Proveedor", 20)


def test_normalize_combo_item_falls_back_between_text_and_value():
    assert combos.normalize_combo_item({"value": 5}) == ("5", 5)
    assert combos.normalize_combo_item({"text": "Sin valor"}) == ("Sin valor", "Sin valor")


def test_combo_module_all_is_defined():
    assert "normalize_combo_item" in combos.__all__
    assert "load_combo" in combos.__all__
    assert "selected_data" in combos.__all__
    assert "select_by_data" in combos.__all__
