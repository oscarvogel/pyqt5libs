from PyQt5.QtWidgets import QApplication

from examples.autoabm_clientes import main as demo


def test_autoabm_can_edit_when_primary_key_is_hidden():
    app = QApplication.instance() or QApplication([])
    demo.initialize_database()
    ClientesABM = demo.build_window_class()
    window = ClientesABM()

    assert "Id" not in window.tableView.cabeceras

    window.tableView.setCurrentCell(0, 0)
    assert window._id_registro_seleccionado() is not None

    window.Modifica()

    assert window.tabDetalle.isEnabled()
    assert app is not None
