from pathlib import Path


def test_abm_source_uses_friendlier_ui_texts():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "Gestión de" in source
    assert "Listado" in source
    assert "Ficha" in source
    assert "Buscar por nombre" in source
    assert "btnLimpiarBusqueda" in source
    assert "print(d)" not in source
