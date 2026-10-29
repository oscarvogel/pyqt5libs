# -*- coding: utf-8 -*-
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QCursor, QGuiApplication
from PyQt5.QtWidgets import QApplication, QDialog, QHBoxLayout

from .EntradaTexto import EntradaTexto
from .Etiquetas import Etiqueta
from .Fechas import FechaLine
from .utiles import icono_sistema


def _pantalla_de(objeto):
    actual = objeto
    while actual is not None:
        handle = actual.windowHandle()
        if handle is not None and handle.screen() is not None:
            return handle.screen()
        actual = actual.parentWidget()
    return None


def pantalla_referencia(widget=None):
    """Devuelve la pantalla donde debe abrirse una ventana nueva.

    Prioriza la pantalla de la ventana padre o de la ventana activa. Si no hay
    una referencia valida usa la pantalla bajo el cursor y, como ultimo
    recurso, la pantalla principal.
    """
    actual = widget
    while actual is not None:
        pantalla = _pantalla_de(actual)
        if pantalla is not None:
            return pantalla
        actual = actual.parentWidget()

    app = QApplication.instance()
    if app is not None:
        pantalla = _pantalla_de(app.activeWindow())
        if pantalla is not None:
            return pantalla

    pantalla = QGuiApplication.screenAt(QCursor.pos())
    if pantalla is not None:
        return pantalla
    return QGuiApplication.primaryScreen()


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
        # Hay que devolver el resultado de QDialog.exec_(): el codigo del
        # dialogo (Accepted / Rejected) es lo que permite al llamador decidir
        # si guardar. Sin este return la funcion terminaba en None y todo
        # `if dialogo.exec_() != dialogo.Accepted: return` salia siempre antes
        # de guardar, sin error ni aviso. La API que ya usaba Qt es result().
        return QDialog.exec_(self)

    def Center(self):
        if self.isMaximized() or self.isFullScreen():
            return
        pantalla = pantalla_referencia(self)
        if pantalla is None:
            return
        qr = self.frameGeometry()

        # center point of the reference screen
        cp = pantalla.availableGeometry().center()

        # move rectangle's center point to screen's center point
        qr.moveCenter(cp)

        # top left of rectangle becomes top left of window centering it
        self.move(qr.topLeft())

    def showMaximized(self):
        pantalla = pantalla_referencia(self)
        if pantalla is not None:
            self.setGeometry(pantalla.availableGeometry())
        super().showMaximized()

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
