# coding=utf-8
"""Regresion de ERR-20261120163418-B700277E.

Si la ventana del formulario se cierra mientras el dialogo de busqueda (F2)
tiene el loop de eventos anidado, al volver de ``exec_()`` el QLineEdit ya no
existe en C++ y ``setText`` lanzaba:

    RuntimeError: wrapped C/C++ object of type Validaciones has been deleted
"""

import os

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

from PyQt5 import sip
from PyQt5.QtWidgets import QApplication

_APP = None


def _app():
    global _APP
    _APP = QApplication.instance() or _APP or QApplication([])
    return _APP


def _nucleo(func):
    """Saltea los decoradores para probar el cuerpo sin capturador de errores."""
    while hasattr(func, "__wrapped__"):
        func = func.__wrapped__
    return func


class _VentanaQueCierraElFormulario:
    """El modal se cierra porque destruyeron el formulario que lo abrio."""

    lRetval = True
    ValorRetorno = "10"

    def __init__(self, widget):
        self._widget = widget

    def CargaDatos(self):
        pass

    def exec_(self):
        sip.delete(self._widget)


def test_busqueda_no_toca_el_campo_si_fue_eliminado():
    _app()
    from pyqt5libs.pyqt5libs.Validaciones import Validaciones

    campo = Validaciones()
    campo.clasebusqueda = lambda: _VentanaQueCierraElFormulario(campo)

    _nucleo(Validaciones.busqueda)(campo, None)

    assert sip.isdeleted(campo)
