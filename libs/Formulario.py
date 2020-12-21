# -*- coding: utf-8 -*-
import os
from os.path import join

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QHBoxLayout

from .EntradaTexto import EntradaTexto
from .Etiquetas import Etiqueta
from .utiles import icono_sistema, ubicacion_sistema


class Formulario(QDialog):

    lblStatusBar = None
    centraform = True
    controles = {}

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.Exception = self.Traceback = ""
        self.LanzarExcepciones = False
        self.setWindowIcon(icono_sistema())
        self.setWindowModality(Qt.ApplicationModal)
        self._want_to_close = False
        flags = Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.EstablecerTema()

    def Cerrar(self):
        self._want_to_close = True
        self.close()

    def exec_(self):
        if self.centraform:
            self.Center()
        QDialog.exec_(self)

    def Center(self):
        qr = self.frameGeometry()

        # center point of screen
        cp = QDesktopWidget().availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def resizeEvent(self, QResizeEvent):
        self.Center()
        QDialog.resizeEvent(self, QResizeEvent)
        print("Ancho {} Alto {}".format(self.width(), self.height()))

    def addStatusBar(self, layout=None):
        if layout:
            self.lblStatusBar = Etiqueta()
            layout.addWidget(self.lblStatusBar)

    def setTextStatusBar(self, text=''):
        if self.lblStatusBar:
            self.lblStatusBar.setText(text)

    def ArmaEntrada(self, nombre="", boxlayout=None, texto='', *args, **kwargs):
        if not boxlayout:
            boxlayout = QHBoxLayout()
            lAgrega = True
        else:
            lAgrega = False

        if not texto:
            texto = nombre.capitalize()

        labelNombre = Etiqueta(texto=texto)
        labelNombre.setObjectName("labelNombre")
        boxlayout.addWidget(labelNombre)

        if 'control' in kwargs:
            lineEditNombre = kwargs['control']
        else:
            lineEditNombre = EntradaTexto()

        if 'relleno' in kwargs:
            lineEditNombre.relleno = kwargs['relleno']

        lineEditNombre.setObjectName(nombre)
        boxlayout.addWidget(lineEditNombre)
        if 'enabled' in kwargs:
            lineEditNombre.setEnabled(kwargs['enabled'])

        self.controles[nombre] = lineEditNombre

        if lAgrega:
            self.verticalLayoutDatos.addLayout(boxlayout)
        return boxlayout

    def setupUi(self, Form):
        pass

    def ConectarWidgets(self):
        pass

    # def closeEvent(self, evnt):
    #     if self._want_to_close:
    #         super(Formulario, self).closeEvent(evnt)
    #     else:
    #         evnt.ignore()
    #         #self.setWindowState(QtCore.Qt.WindowMinimized)

    def keyPressEvent(self, QKeyEvent):
        QKeyEvent.ignore()

    def EstablecerTema(self):
        tema = join(f'{ubicacion_sistema()}', 'pyqt5libs', 'libs', 'temas', 'ubuntu.css')
        if not os.path.isfile(tema):
            tema = join('temas/ubuntu.css')

        style = open(tema)
        style = style.read()
        self.setStyleSheet(style)
