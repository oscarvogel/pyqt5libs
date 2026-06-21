from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QApplication, QPushButton

from pyqt5libs.styles.action_icons import apply_action_icon


def test_action_icon_uses_button_icon_size():
    app = QApplication.instance() or QApplication([])
    button = QPushButton("Guardar")
    button.setIconSize(QSize(32, 32))

    apply_action_icon(button, "save")

    pixmap = button.icon().pixmap(button.iconSize())
    assert pixmap.width() == 32
    assert pixmap.height() == 32
    assert app is not None
