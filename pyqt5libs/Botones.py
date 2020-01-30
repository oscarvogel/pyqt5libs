# coding=utf-8
from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QPushButton, QToolButton

from libs import utiles
from libs.utiles import LeerIni, imagen


class Boton(QPushButton):

    def __init__(self, *args, **kwargs):
        super().__init__()
        texto = ''
        if 'texto' in kwargs:
            texto = kwargs['texto']

        self.setText(texto)

        if 'imagen' in kwargs:
            icono = QIcon(kwargs['imagen'])
            self.setIcon(icono)

            if 'tamanio' in kwargs:
                if kwargs['tamanio'] and isinstance(kwargs['tamanio'],QSize):
                    self.setIconSize(kwargs['tamanio'])
            else:
                self.setIconSize(QSize(32,32))

        if 'tooltip' in kwargs:
            self.setToolTip(kwargs['tooltip'])

        if 'autodefault' in kwargs:
            self.setAutoDefault(kwargs['autodefault'])
        else:
            self.setAutoDefault(True)

        if 'default' in kwargs:
            self.setDefault(kwargs['default'])
        else:
            self.setDefault(False)

        if 'enabled' in kwargs:
            self.setEnabled(kwargs['enabled'])


class BotonEstilo(Boton):
    normal_stylesheet = "    border: 1px solid rgb(54, 209, 80);"\
            "    padding: 8px 30px;"\
            "    border-radius: 3px;"\
            "    color: rgb(62, 175, 42);"\
            "    background-color: rgb(255, 255, 255);"
    hover_stylesheet = "    padding: 10px 30px;"\
                "    border-radius: 3px;"\
                "    color: rgb(255, 255, 255);"\
                "    background-color: rgb(54, 209, 80);"

    hover_stylesheet_disabled = "    border: 1px solid rgb(203, 203, 203);"\
                "    padding: 10px 30px;"\
                "    border-radius: 3px;"\
                "    color: rgb(207, 207, 207);"\
                "    background-color: rgb(255, 255, 255);"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setMouseTracking(True)
        self.setStyleSheet(
            self.normal_stylesheet
        )

    def enterEvent(self, event):
        if self.isEnabled():
            self.setStyleSheet(
                self.hover_stylesheet
            )
        else:
            self.setStyleSheet(
                self.hover_stylesheet_disabled
            )

    def leaveEvent(self, event):
        self.setStyleSheet(
            self.normal_stylesheet
        )

class BotonMain(Boton):

    def __init__(self, *args, **kwargs):
        Boton.__init__(self, *args, **kwargs)
        self.setMinimumHeight(100)
        self.setIconSize(QSize(48,48))

class BotonAceptar(Boton):

    def __init__(self, *args, **kwargs):
        kwargs['texto'] = kwargs['textoBoton'] if 'textoBoton' in kwargs else '&Aceptar'
        kwargs['imagen'] = LeerIni("iniciosistema") + 'imagenes/iconfinder_unit-completed_60215.png'
        kwargs['tamanio'] = QSize(32,32)
        Boton.__init__(self, *args, **kwargs)

class BotonCerrarFormulario(Boton):

    normal_stylesheet = "    border: 1px solid rgb(255,72,72);"\
            "    padding: 8px 30px;"\
            "    border-radius: 3px;"\
            "    color: rgb(255,72,72);"\
            "    background-color: rgb(255, 255, 255);"
    hover_stylesheet = "    padding: 10px 30px;"\
                "    border-radius: 3px;"\
                "    color: rgb(255, 255, 255);"\
                "    background-color: rgb(255,128,128);"

    hover_stylesheet_disabled = "    border: 1px solid rgb(203, 203, 203);"\
                "    padding: 10px 30px;"\
                "    border-radius: 3px;"\
                "    color: rgb(207, 207, 207);"\
                "    background-color: rgb(255, 255, 255);"

    def __init__(self, *args, **kwargs):
        kwargs['texto'] = kwargs['textoBoton'] if 'textoBoton' in kwargs else '&Cerrar'
        kwargs['imagen'] = imagen("iconfinder_free-29_618316.png")
        kwargs['tamanio'] = QSize(32,32)
        Boton.__init__(self, *args, **kwargs)
        self.setDefault(False)


class BotonGrabar(Boton):

    def __init__(self, *args, **kwargs):
        kwargs['texto'] = kwargs['textoBoton'] if 'textoBoton' in kwargs else '&Aceptar'
        kwargs['imagen'] = imagen('guardar.png')
        kwargs['tamanio'] = QSize(32, 32)
        Boton.__init__(self, *args, **kwargs)

class BotonExcel(Boton):

    def __init__(self, parent=None, textoBoton='&Excel'):
        texto = textoBoton
        imagen = self.ubicacionSistema + 'imagenes/Excel.png'
        tamanio = QSize(32,32)
        super().__init__(parent, texto, imagen, tamanio)

class ToolButton(QToolButton):

    texto = '...'
    tamanio = 12

    def __init__(self, *args, **kwargs):
        super().__init__()

        if 'tamanio' in kwargs:
            self.tamanio = kwargs['tamanio']

        if 'texto' in kwargs:
            self.texto = kwargs['texto']

        self.setText(self.texto)
        font = QFont()
        font.setPointSizeF(self.tamanio)
        self.setFont(font)

class BotonEstado(QPushButton):

    normal_stylesheet = "    border: 1px solid rgb(54, 209, 80);"\
            "    padding: 8px 30px;"\
            "    border-radius: 3px;"\
            "    color: rgb(62, 175, 42);"\
            "    background-color: rgb(255, 255, 255);"
    clicked_stylesheet = "    padding: 10px 30px;"\
                "    border-radius: 3px;"\
                "    color: rgb(255, 255, 255);"\
                "    background-color: rgb(54, 209, 80);"

    def __init__(self, parent=None, textoBoton='', *args, **kwargs):
        super().__init__(parent)
        texto = textoBoton
        if 'imagen' in kwargs:
            icono = QIcon(kwargs['imagen'])
            self.setIcon(icono)

            if 'tamanio' in kwargs:
                if kwargs['tamanio'] and isinstance(kwargs['tamanio'],QSize):
                    self.setIconSize(kwargs['tamanio'])
            else:
                self.setIconSize(QSize(32,32))
        # super().__init__(parent, texto=texto, imagen=imagen, tamanio=tamanio)
        # super().__init__(texto, imagen, tamanio)
        self.setText(texto)
        self.setCheckable(True)
        self.setStyleSheet(
            self.normal_stylesheet
        )
        self.setDefault(False)
        self.setAutoDefault(False)

    def CambiaEstado(self):
        # self.toggle()
        if self.isChecked():
            self.setStyleSheet(
                self.clicked_stylesheet
            )
        else:
            self.setStyleSheet(
                self.normal_stylesheet
            )

class BotonImprimir(Boton):

    def __init__(self, parent=None, textoBoton='&Imprimir'):
        texto = textoBoton
        imagen = utiles.imagen('printing.png')
        tamanio = QSize(32,32)
        super().__init__(parent, texto, imagen, tamanio)
