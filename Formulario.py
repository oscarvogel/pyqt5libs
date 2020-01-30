# -*- coding: utf-8 -*-
from functools import partial

import peewee
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QDesktopWidget, QHBoxLayout, QGridLayout

from libs.Botones import Boton
from libs.EntradaTexto import EntradaTexto
from libs.Etiquetas import Etiqueta
from libs.Spinner import Spinner
from libs.utiles import icono_sistema


class Formulario(QDialog):

    lblStatusBar = None
    centraform = True
    controles = {}

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.Exception = self.Traceback = ""
        self.LanzarExcepciones = False
        self.setWindowIcon(icono_sistema())
        # self.setWindowModality(Qt.ApplicationModal)
        self._want_to_close = False

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

    def addStatusBar(self, layout=None):
        if layout:
            self.lblStatusBar = Etiqueta()
            layout.addWidget(self.lblStatusBar)

    def setTextStatusBar(self, text=''):
        if self.lblStatusBar:
            self.lblStatusBar.setText(text)

    def ArmaEntrada(self, nombre="", boxlayout=None, texto='', *args, **kwargs):
        if boxlayout is None:
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

    def ArmaEntradaCampo(self, campo=peewee.Field, boxlayout=None, texto = '', *args, **kwargs):
        if boxlayout is None:
            boxlayout = QHBoxLayout()
            lAgrega = True
        else:
            lAgrega = False

        lblNombreCodigo = None
        nombre = campo.name

        if not texto:
            texto = campo.verbose_name.capitalize() if campo.verbose_name else campo.name.capitalize()
        labelNombre = Etiqueta(texto=texto)

        if isinstance(boxlayout, QGridLayout) and 'posicion' in kwargs:
            boxlayout.addWidget(labelNombre, kwargs['posicion'][0], kwargs['posicion'][1])
        else:
            boxlayout.addWidget(labelNombre)

        if 'control' in kwargs:
            lineEditNombre = kwargs['control']
            if kwargs['valida']:
                lblNombreCodigo = Etiqueta()
                lineEditNombre.widgetNombre = lblNombreCodigo
        else:
            if isinstance(campo, (peewee.CharField, )):
                lineEditNombre = EntradaTexto()
            elif isinstance(campo, (peewee.IntegerField, peewee.DecimalField)):
                lineEditNombre = Spinner()
            else:
                lineEditNombre = EntradaTexto()
        if 'relleno' in kwargs:
            lineEditNombre.relleno = kwargs['relleno']

        if 'inputmask' in kwargs:
            lineEditNombre.setInputMask(kwargs['inputmask'])

        if isinstance(boxlayout, QGridLayout) and 'posicion' in kwargs:
            boxlayout.addWidget(lineEditNombre, kwargs['posicion'][2], kwargs['posicion'][3])
            if lblNombreCodigo:
                boxlayout.addWidget(lblNombreCodigo, kwargs['posicion'][2], kwargs['posicion'][3] + 1)
        else:
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

    def run(self):
        self.show()

    # def closeEvent(self, evnt):
    #     if self._want_to_close:
    #         super(Formulario, self).closeEvent(evnt)
    #     else:
    #         evnt.ignore()
    #         #self.setWindowState(QtCore.Qt.WindowMinimized)

    def keyPressEvent(self, QKeyEvent):
        QKeyEvent.ignore()

class Menu(Formulario):

    opciones = []
    nRetorno = 0
    parent = None
    botones = {}
    valoresRetorno = []
    valorSeleccionado = None

    def __init__(self, *args, **kwargs):
        Formulario.__init__(self)

        self.opciones = kwargs['opciones']
        if 'valores' in kwargs:
            self.valoresRetorno = kwargs['valores']

        self.setupUi(self)
        self.Center()

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.setWindowTitle("Opciones de menu")
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")

        i = 0
        for x in self.opciones:
            self.botones[str(i)] = Boton(Dialog, texto=x)
            self.botones[str(i)].setObjectName(x)
            self.botones[str(i)].clicked.connect(partial(self.onClicked, i))
            self.botones[str(i)].setMinimumHeight(50)
            self.botones[str(i)].setMinimumWidth(200)
            self.verticalLayout.addWidget(self.botones[str(i)])
            i += 1
        print(self.botones)

    def onClicked(self, n):
        self.nRetorno = n
        if self.valoresRetorno:
            self.valorSeleccionado = self.valoresRetorno[n]
        self.Cerrar()
