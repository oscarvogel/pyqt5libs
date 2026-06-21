from dataclasses import dataclass

from pyqt5libs.ui import tables


@dataclass
class Person:
    id: int
    name: str


def test_normalize_table_row_from_dict_with_columns():
    row = {"id": 1, "name": "Oscar", "ignored": "x"}
    assert tables.normalize_table_row(row, columns=["id", "name"]) == [1, "Oscar"]


def test_normalize_table_row_from_dict_without_columns():
    row = {"id": 1, "name": "Oscar"}
    assert tables.normalize_table_row(row) == [1, "Oscar"]


def test_normalize_table_row_from_object_with_columns():
    row = Person(id=2, name="Karina")
    assert tables.normalize_table_row(row, columns=["id", "name"]) == [2, "Karina"]


def test_normalize_table_row_from_tuple_or_list():
    assert tables.normalize_table_row((1, "Activo")) == [1, "Activo"]
    assert tables.normalize_table_row([2, "Inactivo"]) == [2, "Inactivo"]


def test_normalize_table_row_from_simple_value():
    assert tables.normalize_table_row("Texto") == ["Texto"]


def test_tables_module_all_is_defined():
    assert "normalize_table_row" in tables.__all__
    assert "load_table" in tables.__all__
    assert "current_row_values" in tables.__all__
    assert "current_cell_text" in tables.__all__
