# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QDesktopWidget, QHBoxLayout

from .EntradaTexto import EntradaTexto
from .Etiquetas import Etiqueta
from .Fechas import FechaLine
from .utiles import icono_sistema


class Formulario(QDialog):

    lblStatusBar = None
    centraform = True
    controles = {}

    def __init__(self, parent=None):
        QDialog.__init__(self, parent=None)
        self.setModal(False)
        self.Exception = self.Traceback = ""
        self.LanzarExcepciones = False
        self.setWindowIcon(icono_sistema())
        # self.setWindowModality(Qt.NonModal)
        self._want_to_close = False
        flags = Qt.WindowMinMaxButtonsHint | Qt.WindowCloseButtonHint
        self.setWindowFlags(flags)
        self.setMinimumSize(420, 160)
        # Los formularios ya no aplican un CSS propio. El estilo debe venir del
        # QApplication (por ejemplo, el QSS global de RND) o, si no existe un
        # tema global, del estilo nativo de Qt. Mantener esta llamada como no-op
        # conserva compatibilidad con subclases/codigo historico que puedan
        # invocar EstablecerTema() explicitamente.
        self.EstablecerTema()
        # self.EstablecerOrden()

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
        QDialog.resizeEvent(self, QResizeEvent)

    def addStatusBar(self, layout=None):
        if layout:
            self.lblStatusBar = Etiqueta()
            layout.addWidget(self.lblStatusBar)

    def setTextStatusBar(self, text=''):
        if self.lblStatusBar:
            self.lblStatusBar.setText(text)

    def ArmaEntrada(self, nombre="", boxlayout=None, texto='', *args, **kwargs):
        if not nombre:
            return
        if not boxlayout:
            boxlayout = QHBoxLayout()
            lAgrega = True
        else:
            lAgrega = False

        if not texto:
            if isinstance(nombre, str):
                texto = nombre.capitalize()
            else:
                if not 'control' in kwargs:
                    if nombre.field_type in ['DATE']:
                        kwargs['control'] = FechaLine()
                texto = nombre.verbose_name if nombre.verbose_name else nombre.name.capitalize()


        if not isinstance(nombre, str): #si no es un campo texto intento convertir de un campo de pewee
            nombre = nombre.name

        labelNombre = Etiqueta(texto=texto)
        labelNombre.setObjectName("labelNombre")
        boxlayout.addWidget(labelNombre)

        if 'control' in kwargs:
            lineEditNombre = kwargs['control']
        else:
            lineEditNombre = EntradaTexto()

        if 'relleno' in kwargs:
            lineEditNombre.relleno = kwargs['relleno']

        if 'inputmask' in kwargs:
            lineEditNombre.setInputMask(kwargs['inputmask'])

        lineEditNombre.setObjectName(nombre)
        #print(type(lineEditNombre))
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
        """Compatibilidad: no aplica temas CSS por formulario.

        El tema visual debe definirse una sola vez a nivel de QApplication.
        Esto evita que configuraciones legacy como TEMA/darkblue/qdark
        sobrescriban el QSS global y, si no hay QSS, deja que Qt utilice su
        estilo nativo.
        """
        return None

    def EstablecerOrden(self):
        pass
