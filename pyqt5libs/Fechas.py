# coding=utf-8
import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDateEdit, QStyledItemDelegate, QItemDelegate, QHBoxLayout
from PyQt5.uic.properties import QtGui

from . import Ventanas
from .EntradaTexto import EntradaTexto
from .Etiquetas import Etiqueta


class Fecha(QDateEdit):

    proximoWidget = None
    tamanio = 10

    def __init__(self, *args, **kwargs):
        QDateEdit.__init__(self, *args)
        self.setCalendarPopup(True)
        #self.cw = QNCalendarWidget(n=1, columns=1)
        #self.setCalendarWidget(self.cw)

        if 'enabled' in kwargs:
            self.setEnabled(kwargs['enabled'])
        if 'tamanio' in kwargs:
            self.tamanio = kwargs['tamanio']
        font = QFont()
        font.setPointSizeF(self.tamanio)
        self.setFont(font)
        if 'fecha' in kwargs:
            self.setFecha(kwargs['fecha'])

    def setFecha(self, fecha=datetime.datetime.today(), format=None):
        if format:
            if format == "Ymd":
                fecha = datetime.date(year=int(fecha[:4]),
                                      month=int(fecha[4:6]),
                                      day=int(fecha[-2:]))
        if isinstance(fecha, int):
            if fecha > 0:
                self.setDate(datetime.date.today() + datetime.timedelta(days=fecha))
            else:
                self.setDate(datetime.date.today() - datetime.timedelta(days=abs(fecha)))
        else:
            self.setDate(fecha)

    def keyPressEvent(self, QKeyEvent, *args, **kwargs):
        teclaEnter = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab]
        if QKeyEvent.key() in teclaEnter:
            if self.proximoWidget:
                self.proximoWidget.setFocus()
        QDateEdit.keyPressEvent(self, QKeyEvent, *args, **kwargs)

    def getFechaSql(self):
        fecha = str(self.text())
        fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y").date().strftime('%Y%m%d')
        return fecha

    def setText(self, fecha=datetime.datetime.today()):
        if isinstance(fecha, (str)):
            fecha = datetime.datetime.today()
        self.setFecha(fecha)

    def toPyDate(self):
        return self.date().toPyDate()

    def getPeriodo(self):
        periodo = self.getFechaSql()[:6]
        return periodo

class FechaDelegate(QItemDelegate):

    def __init__(self):
        super().__init__()

    def createEditor(self,parent, option, index):
        editor = Fecha(parent, fecha=datetime.datetime.today())

        return editor

    # def paint(self, QPainter, QStyleOptionViewItem, QModelIndex):
    #     value = QModelIndex.data(Qt.DisplayRole)
    #     print("valor de paint {}".format(value))
    #
    #     # QItemDelegate.paint(self, QPainter, QStyleOptionViewItem, QModelIndex)
    #     super(FechaDelegate, self).paint(QPainter, QStyleOptionViewItem, QModelIndex)
    # #
    # def setEditorData(self, fecha, index):
    #     value = index.model().data(index, Qt.EditRole)
    #     if isinstance(value, QtCore.QDate):
    #         value = value.toPyDate()
    #         fecha.setFecha(value)
    #     # qdate = QtCore.QDate().fromString(value, "dd/mm/yyyy")
    #     print("valor editor data {}".format(value))
    #     # fecha.setFecha(qdate)
    #
    # def setModelData(self, fecha, model, index):
    #     value = fecha.date()
    #
    #     model.setData(index, value, Qt.EditRole)
    #
    # def updateEditorGeometry(self, editor, option, index):
    #     editor.setGeometry(option.rect)

class RangoFechas(QHBoxLayout):

    etiqueta_desde = "Desde fecha"
    etiqueta_hasta = "Hasta fecha"

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        lblDesdeFecha = Etiqueta(texto=self.etiqueta_desde)
        self.desde_fecha = Fecha(fecha=0)
        lblHastaFecha = Etiqueta(texto=self.etiqueta_hasta)
        self.hasta_fecha = Fecha(fecha=0)
        self.addWidget(lblDesdeFecha)
        self.addWidget(self.desde_fecha)
        self.addWidget(lblHastaFecha)
        self.addWidget(self.hasta_fecha)

class FechaLine(EntradaTexto):

    proximoWidget = None
    tamanio = 10
    nulldate = False
    fecha = None

    def __init__(self, *args, **kwargs):
        super().__init__()
        # self.setCalendarPopup(True)

        if 'enabled' in kwargs:
            self.setEnabled(kwargs['enabled'])
        if 'tamanio' in kwargs:
            self.tamanio = kwargs['tamanio']
        font = QFont()
        font.setPointSizeF(self.tamanio)
        self.setFont(font)
        if 'fecha' in kwargs:
            self.setFecha(kwargs['fecha'])
        else:
            self.setFecha()

        # reg_ex_str = "^(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})$"
        # reg_ex = QtCore.QRegExp(reg_ex_str)
        # input_validator = QRegExpValidator(reg_ex, self)
        # self.setValidator(input_validator)
        self.setupUi()

    def setupUi(self):
        self.setInputMask("00/00/0000")
        # self.addWidget(self.textFecha)

    def setFecha(self, fecha=datetime.datetime.today(), format=None):
        if format:
            if format == "Ymd":
                fecha = datetime.date(year=int(fecha[:4]),
                                      month=int(fecha[4:6]),
                                      day=int(fecha[-2:]))
        if isinstance(fecha, int):
            if fecha > 0:
                self.setDate(datetime.date.today() + datetime.timedelta(days=fecha))
            else:
                self.setDate(datetime.date.today() - datetime.timedelta(days=abs(fecha)))
        elif not fecha: #quiere decir que viene None de la tabla en mysql es 0000-00-00
            self.nulldate = True
            # self.setSpecialValueText("0000-00-00")
            self.fecha = "0000-00-00"
        else:
            self.setDate(fecha)

        if isinstance(self.fecha, str):
            self.setText(self.fecha)
        else:
            self.setText(self.fecha.strftime('%d/%m/%Y'))

    def setDate(self, date):
        self.fecha = date

    def keyPressEvent(self, QKeyEvent, *args, **kwargs):
        teclaEnter = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab]
        if QKeyEvent.key() in teclaEnter:
            if self.proximoWidget:
                self.proximoWidget.setFocus()
        elif QKeyEvent.key() in [Qt.Key_Delete, Qt.Key_Backspace]:
            self.clear()
        EntradaTexto.keyPressEvent(self, QKeyEvent, *args, **kwargs)

    def getFechaSql(self):
        # fecha = str(self.text())
        # fecha = datetime.datetime.strptime(fecha, "%d/%m/%Y").date().strftime('%Y%m%d')
        fecha = self.fecha.strftime("%Y%m%d")
        return fecha

    # def setText(self, fecha=datetime.datetime.today()):
    #     if isinstance(fecha, (str)): #quiere decir que viene 0000-00-00 de mysql
    #         # fecha = datetime.datetime.today()
    #         self.setFecha(self.minimumDate())
    #         self.nulldate = True
    #     else:
    #         self.nulldate = False
    #         self.setFecha(fecha)

    def getPeriodo(self):
        periodo = self.getFechaSql()[:6]
        return periodo

    def toPyDate(self):
        self.focusOutEvent()
        return self.fecha.date()

    def valor(self):
        return self.fecha

    # def text(self):
    #     return self.valor()

    def minimumDate(self):
        return datetime.date(2000, 1, 1)

    def focusOutEvent(self, QFocusEvent=None):
        if len(self.text()) == 8 or self.text().endswith('/'):
            self.setText(f'{self.text()[:6]}{datetime.datetime.now().year}')
        try:
            self.fecha = datetime.datetime.strptime(self.text(), "%d/%m/%Y")
            self.setStyleSheet("background-color: Dodgerblue")
        except:
            Ventanas.showAlert("Sistema", "Fecha no valida")
            self.setStyleSheet("background-color: Red")

class HoraEntradaSalida(QHBoxLayout):

    etiqueta_desde = "Inicio"
    etiqueta_hasta = "Fin"

    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        lblDesdeHora = Etiqueta(texto=self.etiqueta_desde)
        self.desde_hora = EntradaTexto(inputmask='00:00')
        lblHastaHora = Etiqueta(texto=self.etiqueta_hasta)
        self.hasta_hora = EntradaTexto(inputmask='00:00')
        self.addWidget(lblDesdeHora)
        self.addWidget(self.desde_hora)
        self.addWidget(lblHastaHora)
        self.addWidget(self.hasta_hora)
