from pathlib import Path


def test_abm_source_uses_friendlier_ui_texts():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "Gestión de" in source
    assert "Listado" in source
    assert "Ficha" in source
    assert "Buscar por nombre" in source
    assert "btnLimpiarBusqueda" in source
    assert "print(d)" not in source


def test_abm_source_defines_shortcuts_and_double_click_editing():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "keyPressEvent" in source
    assert "Qt.Key_F2" in source
    assert "Qt.Key_F3" in source
    assert "Qt.Key_F4" in source
    assert "Qt.Key_Delete" in source
    assert "Qt.Key_F10" in source
    assert "Qt.Key_Escape" in source
    assert "doubleClicked" in source
    assert "cellDoubleClicked" in source
