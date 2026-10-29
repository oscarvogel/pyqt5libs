import os
import sys

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5.QtWidgets import QApplication, QDialog, QWidget  # noqa: E402

from pyqt5libs.ubicacion_pantalla import (  # noqa: E402
    UbicacionPantallaMixin,
    VistaDialogo,
    pantalla_referencia,
)

app = QApplication.instance() or QApplication(sys.argv)


def test_pantalla_referencia_devuelve_una_pantalla():
    assert pantalla_referencia() is not None


def test_vista_dialogo_es_un_qdialog():
    dialogo = VistaDialogo()
    assert isinstance(dialogo, QDialog)
    dialogo.close()


def test_vista_dialogo_respeta_el_parent():
    padre = QWidget()
    dialogo = VistaDialogo(padre)
    assert dialogo.parent() is padre
    dialogo.close()


def test_vista_dialogo_se_centra_al_mostrarse():
    dialogo = VistaDialogo()
    dialogo.resize(400, 300)
    dialogo.move(-5000, -5000)

    dialogo.show()
    app.processEvents()

    pantalla = pantalla_referencia()
    assert pantalla.availableGeometry().contains(dialogo.frameGeometry().center())
    dialogo.close()


def test_mixin_mantiene_comportamiento_conservador_por_defecto():
    assert UbicacionPantallaMixin.respetar_parent is False
    assert UbicacionPantallaMixin.centrar_en_pantalla_activa is True
