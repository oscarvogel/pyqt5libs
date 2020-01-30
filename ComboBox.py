# coding=utf-8
import decimal

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QComboBox, QItemDelegate, QApplication, QStyle

class ComboSQL(QComboBox):

    lTodos = False
    cBaseDatos = ''
    cSentencia = ''
    campo1 = ''
    campo2 = ''
    campovalor = ''
    condicion = ''
    tabla = ''
    cOrden = None
    modelo = None
    proximoWidget = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        font = QFont()
        font.setPointSizeF(10)
        self.setFont(font)
        self.CargaDatos()

    def CargaDatos(self):
        self.clear()
        if not self.modelo:
            return

        data = self.modelo.select().dicts()
        if self.condicion:
            data = data.where(self.condicion)

        if self.cOrden:
            data = data.order_by(self.cOrden)

        for r in data:
            if isinstance(r[self.campovalor], (decimal.Decimal,)):
                valor = str(r[self.campovalor])
            else:
                valor = r[self.campovalor]
            if isinstance(r[self.campo1], (decimal.Decimal,)):
                campo1 = str(r[self.campo1])
            else:
                campo1 = r[self.campo1]
            self.addItem(campo1, valor)

    def GetDato(self):
        return self.currentData()

    def text(self):
        if self.currentData():
            return self.currentData()
        else:
            return self.currentText()

    def setText(self, p_str):
        #self.setCurrentIndex()
        self.setCurrentText(p_str)

    def setIndex(self, p_str):
        self.setCurrentIndex(self.findData(p_str))

    def keyPressEvent(self, QKeyEvent):
        teclaEnter = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab]
        if QKeyEvent.key() in teclaEnter:
            if self.proximoWidget:
                self.proximoWidget.setFocus()
        super().keyPressEvent(QKeyEvent)

class Combo(QComboBox):

    proximoWidget = None

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        font = QFont()
        if 'tamanio' in kwargs:
            font.setPointSizeF(kwargs['tamanio'])
        # else:
        #     font.setPointSizeF(12)
        self.setFont(font)

    def CargaDatos(self, data=None):
        if data:
            for r in data:
                self.addItem(r)

    def keyPressEvent(self, QKeyEvent):
        teclaEnter = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab]
        if QKeyEvent.key() in teclaEnter:
            if self.proximoWidget:
                self.proximoWidget.setFocus()
        super().keyPressEvent(QKeyEvent)

    def CargaDatosValores(self, data=None):
        if data:
            for k, v in data.items():
                self.addItem(v, k)

    def text(self):
        if self.currentData():
            return self.currentData()
        else:
            return self.currentText()

    def setText(self, p_str):
        #self.setCurrentIndex()
        self.setCurrentText(p_str.strip())

class ComboSINO(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.CargaDatosValores(data={'S':'SI','N':'NO'})


class FormaPago(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        Combo.__init__(self, parent, *args, **kwargs)
        self.CargaDatosValores(data={'S':'Contado','N':'Cuenta corriente'})

class ComboBoxDelegate(QItemDelegate):
    def __init__(self, parent=None):
        super(ComboBoxDelegate, self).__init__(parent)
        self.items = []

    def setItems(self, items):
        self.items = items

    def createEditor(self, widget, option, index):
        editor = QComboBox(widget)
        editor.addItems(self.items)
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value:
            editor.setCurrentIndex(int(value))

    def setModelData(self, editor, model, index):
        model.setData(index, editor.currentIndex(), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def paint(self, painter, option, index):
        text = self.items[index.row()]
        option.text = text
        QApplication.style().drawControl(QStyle.CE_ItemViewItem, option, painter)

class cboDebeHaber(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        Combo.__init__(self, parent, *args, **kwargs)
        self.CargaDatosValores(data={'D':'Debe','H':'Haber'})

