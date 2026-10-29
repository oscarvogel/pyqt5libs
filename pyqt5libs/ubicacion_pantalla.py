# -*- coding: utf-8 -*-
"""Utilidades para ubicar ventanas en la pantalla activa.

Este modulo es aditivo: ``Formulario`` mantiene su comportamiento historico y
las pantallas nuevas pueden usar ``VistaDialogo`` para respetar el ``parent`` y
abrir en el monitor donde esta trabajando el usuario.
"""
from PyQt5.QtGui import QCursor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QDialog


def pantalla_de(objeto):
    """Devuelve la pantalla actual de un widget, o ``None`` si no se puede."""
    actual = objeto
    while actual is not None:
        try:
            handle = actual.windowHandle()
            if handle is not None and handle.screen() is not None:
                return handle.screen()
            actual = actual.parentWidget()
        except RuntimeError:
            # El objeto Qt ya fue destruido mientras seguia referenciado.
            return None
    return None


def pantalla_referencia(widget=None, excluir=None):
    """Devuelve la pantalla donde debe abrirse una ventana nueva.

    Prioriza la pantalla de la ventana padre o de la ventana activa. Si no hay
    una referencia valida usa la pantalla bajo el cursor y, como ultimo
    recurso, la pantalla principal. ``excluir`` permite ignorar la ventana que
    se esta ubicando para no tomar su posicion provisoria.
    """
    actual = widget
    while actual is not None:
        pantalla = pantalla_de(actual)
        if pantalla is not None:
            return pantalla
        actual = actual.parentWidget()

    app = QApplication.instance()
    if app is not None:
        activa = app.activeWindow()
        if activa is not None and activa is not excluir:
            pantalla = pantalla_de(activa)
            if pantalla is not None:
                return pantalla

    pantalla = QGuiApplication.screenAt(QCursor.pos())
    if pantalla is not None:
        return pantalla
    return QGuiApplication.primaryScreen()


class UbicacionPantallaMixin:
    """Comportamiento comun para centrar una ventana en la pantalla activa."""

    respetar_parent = False
    centrar_en_pantalla_activa = True

    def _pantalla_destino(self):
        return pantalla_referencia(self.parentWidget(), excluir=self)

    def Center(self):
        if not self.centrar_en_pantalla_activa:
            return
        if self.isMaximized() or self.isFullScreen():
            return
        pantalla = self._pantalla_destino()
        if pantalla is None:
            return
        geometria = self.frameGeometry()
        geometria.moveCenter(pantalla.availableGeometry().center())
        self.move(geometria.topLeft())

    def showMaximized(self):
        pantalla = self._pantalla_destino()
        if pantalla is not None:
            self.setGeometry(pantalla.availableGeometry())
        super().showMaximized()


class VistaDialogo(UbicacionPantallaMixin, QDialog):
    """Dialogo base que respeta el ``parent`` y ubica en la pantalla activa.

    A diferencia de ``Formulario``, no impone modalidad ni tamano minimo y si
    propaga el ``parent`` a ``QDialog``. Se centra una sola vez, al mostrarse.
    """

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self._ubicacion_resuelta = False

    def showEvent(self, evento):
        if not self._ubicacion_resuelta:
            self._ubicacion_resuelta = True
            self.Center()
        super().showEvent(evento)
