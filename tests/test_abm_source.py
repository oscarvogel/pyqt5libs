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


def test_abm_source_defines_responsive_form_layout_modes():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "form_layout_mode" in source
    assert "form_columns" in source
    assert "form_auto_columns_threshold" in source
    assert "single" in source
    assert "two_columns" in source
    assert "auto" in source
    assert "gridLayoutFormulario" in source
    assert "_agrega_layout_campo" in source


def test_abm_source_defines_real_responsive_form_container():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "QScrollArea" in source
    assert "QSizePolicy" in source
    assert "scrollDetalleABM" in source
    assert "formPanelABM" in source
    assert "form_field_min_width" in source
    assert "_configura_control_formulario" in source
    assert "_configura_boton_formulario" in source
    assert "setMinimumWidth" in source
    assert "setWidgetResizable" in source


def test_abm_source_defines_split_view_mode():
    source = Path("libs/vistas/ABM.py").read_text(encoding="utf-8")

    assert "view_mode" in source
    assert "split_sizes" in source
    assert "QSplitter" in source
    assert "splitterABM" in source
    assert "_usa_modo_split" in source
    assert "_configura_contenedor_principal" in source
    assert "_mostrar_listado" in source
    assert "_mostrar_ficha" in source


def test_fluent_style_module_exists():
    source = Path("pyqt5libs/styles/fluent.py").read_text(encoding="utf-8")

    assert "fluent_abm_stylesheet" in source
    assert "Segoe UI" in source
    assert "#0f6cbd" in source
    assert "formPanelABM" in source
    assert "btnAceptar" in source


def test_autoabm_example_applies_fluent_style():
    source = Path("examples/autoabm_clientes/main.py").read_text(encoding="utf-8")

    assert "fluent_abm_stylesheet" in source
    assert "app.setStyleSheet" in source
    assert "setMinimumSize(1180, 720)" in source
