from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QFrame, QSizePolicy, QToolButton

from pyqt5libs.libs.vistas.ABM import ABM
from pyqt5libs.pyqt5libs.Botones import Boton


_WINDOWS = []
_APP = None


def _app():
    global _APP
    _APP = QApplication.instance() or _APP or QApplication([])
    return _APP


def _keep_window(window):
    _WINDOWS.append(window)
    return window


class _BaseAdditionalButtonsABM(ABM):
    autoConectaWidgets = False

    def __init__(self, additional_count=0):
        self.additional_count = additional_count
        self.clicked = []
        super().__init__()

    def BotonesAdicionales(self):
        self.extra_buttons = []
        for index in range(self.additional_count):
            button = Boton(
                self.tabLista,
                texto="Extra {}".format(index + 1),
                tooltip="Accion extra {}".format(index + 1),
            )
            button.setObjectName("btnExtra{}".format(index + 1))
            button.clicked.connect(lambda checked=False, value=index + 1: self.clicked.append(value))
            if index == 1:
                button.setEnabled(False)
            self.extra_buttons.append(button)
            self.horizontalLayout.addWidget(button)


def test_auto_groups_multiple_additional_buttons():
    _app()
    window = _keep_window(_BaseAdditionalButtonsABM(additional_count=2))

    more_button = window.findChild(QToolButton, "btnMasAcciones")

    assert more_button is not None
    assert more_button.text() == "Más acciones"
    assert more_button.menu() is not None
    assert [action.text() for action in more_button.menu().actions()] == ["Extra 1", "Extra 2"]
    assert more_button.menu().actions()[1].isEnabled() is False
    assert window.extra_buttons[0].isHidden() is True
    assert window.extra_buttons[1].isHidden() is True

    more_button.menu().actions()[0].trigger()
    assert window.clicked == [1]


def test_auto_keeps_single_additional_button_visible():
    _app()
    window = _keep_window(_BaseAdditionalButtonsABM(additional_count=1))

    assert window.findChild(QToolButton, "btnMasAcciones") is None
    assert window.extra_buttons[0].isHidden() is False


def test_always_groups_single_additional_button():
    _app()

    class AlwaysABM(_BaseAdditionalButtonsABM):
        agrupar_botones_adicionales = "always"

    window = _keep_window(AlwaysABM(additional_count=1))

    more_button = window.findChild(QToolButton, "btnMasAcciones")

    assert more_button is not None
    assert [action.text() for action in more_button.menu().actions()] == ["Extra 1"]
    assert window.extra_buttons[0].isHidden() is True


def test_never_keeps_additional_buttons_ungrouped():
    _app()

    class NeverABM(_BaseAdditionalButtonsABM):
        agrupar_botones_adicionales = "never"

    window = _keep_window(NeverABM(additional_count=2))

    assert window.findChild(QToolButton, "btnMasAcciones") is None
    assert window.extra_buttons[0].isHidden() is False
    assert window.extra_buttons[1].isHidden() is False


def test_toolbar_uses_consistent_button_sizing_and_visual_groups():
    _app()
    window = _keep_window(_BaseAdditionalButtonsABM(additional_count=2))

    assert window.horizontalLayout.spacing() == 10
    assert window.horizontalLayout.contentsMargins().left() == 0

    expected_buttons = [
        window.btnAgregar,
        window.btnEditar,
        window.btnBorrar,
        window.btnExcel,
        window.btnCerrar,
        window.btnMasAcciones,
    ]
    toolbar_height = expected_buttons[0].minimumHeight()
    assert toolbar_height >= 36
    for button in expected_buttons:
        assert button.minimumHeight() == toolbar_height
        assert button.minimumWidth() >= 104
        assert button.iconSize() == QSize(20, 20)
        assert button.sizePolicy().horizontalPolicy() == QSizePolicy.Minimum
        assert button.sizePolicy().verticalPolicy() == QSizePolicy.Fixed

    separator_export = window.findChild(QFrame, "separatorToolbarABMExport")
    separator_close = window.findChild(QFrame, "separatorToolbarABMCierre")

    assert separator_export is not None
    assert separator_export.frameShape() == QFrame.VLine
    assert separator_close is not None
    assert separator_close.frameShape() == QFrame.VLine
