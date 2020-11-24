# coding=utf-8
import decimal

from PyQt5 import QtCore
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
    numero_filas = 0

    def __init__(self, *args, **kwargs):
        super().__init__()
        font = QFont()
        font.setPointSizeF(10)
        self.setFont(font)
        if 'checkeable' in kwargs:
            self.CargaDatos(checkeable=kwargs['checkeable'])
        else:
            self.CargaDatos()

    def CargaDatos(self, checkeable=False, checked=False):
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
            self.agregar_dato(campo1, valor, checkeable, checked)
        self.postCargaDatos()

    def agregar_dato(self, detalle, valor, checkeable=False, checked=False):
        self.numero_filas += 1
        self.addItem(detalle, valor)

        if checkeable:
            item = self.model().item(self.count() - 1, 0)
            item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
            if checked:
                item.setCheckState(QtCore.Qt.Checked)
            else:
                item.setCheckState(QtCore.Qt.Unchecked)

    def itemChecked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == QtCore.Qt.Checked

    def postCargaDatos(self):
        pass

    def GetDato(self):
        return self.currentData()

    def text(self):
        if self.currentData():
            return self.currentData()
        else:
            return self.currentText()

    def setText(self, p_str):
        # self.setCurrentIndex()
        self.setCurrentText(p_str)

    def setIndex(self, p_str):
        self.setCurrentIndex(self.findData(p_str))

    def keyPressEvent(self, QKeyEvent):
        teclaEnter = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab]
        if QKeyEvent.key() in teclaEnter:
            if self.proximoWidget:
                self.proximoWidget.setFocus()
        super().keyPressEvent(QKeyEvent)

    # obtiene el dato de la fila
    def getItem(self, fila):
        try:
            item = self.itemText(fila)
            item = item.replace(',', '.')  # if item else 0
        except:
            item = ''

        return item

    # obtiene el indice de la fila
    def getData(self, fila):
        try:
            item = self.itemData(fila)
            item = item.replace(',', '.')  # if item else 0
        except:
            item = ''

        return item

    def getSelectedItems(self):
        seleccionados = []
        for row in range(self.rowCount()):
            if self.itemChecked(row):
                seleccionados.append(self.getData(row))

        return seleccionados

    def rowCount(self):
        return self.numero_filas

class Combo(QComboBox):
    proximoWidget = None
    data = None
    numero_filas = 0

    def __init__(self, parent=None, *args, **kwargs):
        QComboBox.__init__(self, parent)
        font = QFont()
        if 'tamanio' in kwargs:
            font.setPointSizeF(kwargs['tamanio'])
        else:
            font.setPointSizeF(12)

        if 'enabled' in kwargs:
            self.setEnabled(kwargs['enabled'])

        self.setFont(font)

    def CargaDatos(self, data=None):
        if data:
            for r in data:
                self.addItem(r)
                self.numero_filas += 1

    def CargaDatosValores(self, data=None, checkeable=False, checked=False):
        self.clear()
        if data:
            for k, v in data.items():
                self.addItem(v, k)
                if checkeable:
                    item = self.model().item(self.count() - 1, 0)
                    item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
                    if checked:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                self.numero_filas += 1

    def itemChecked(self, index):
        item = self.model().item(index, 0)
        return item.checkState() == QtCore.Qt.Checked

    # obtiene el dato de la fila
    def getItem(self, fila):
        try:
            item = self.itemText(fila)
            item = item.replace(',', '.')  # if item else 0
        except:
            item = ''

        return item

    # obtiene el indice de la fila
    def getData(self, fila):
        try:
            item = self.itemData(fila)
            item = item.replace(',', '.')  # if item else 0
        except:
            item = ''

        return item

    def getSelectedItems(self):
        seleccionados = []
        for row in range(self.rowCount()):
            if self.itemChecked(row):
                seleccionados.append(self.getData(row))

        return seleccionados

    def text(self):
        # return self.currentText()
        if self.currentData():
            return self.currentData()
        else:
            return self.currentText()
        # return self.itemData(self.currentIndex(), Qt.DisplayRole)

    def setText(self, p_str):
        index = self.findText(p_str)
        self.setCurrentIndex(index)

    def setIndex(self, p_str):
        self.setCurrentIndex(self.findData(p_str))

    def rowCount(self):
        return self.numero_filas


class ComboSINO(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.CargaDatosValores(data={'S': 'SI', 'N': 'NO'})


class FormaPago(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        Combo.__init__(self, parent, *args, **kwargs)
        self.CargaDatosValores(data={'S': 'Contado', 'N': 'Cuenta corriente'})


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


class ComboTablas(Combo):

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent)
        self.CargaDatos(data=[
            'LOCALIDADES',
            'CLIENTES',
            'PROVEEDORES',
            'TRANSPORTES',
            'CHOFERES',
            'ARTICULOS',
            'CENTROS DE COSTOS',
            'RETENCION PROVEEDOR'
        ])


class cboFormaCalculo(Combo):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CargaDatosValores(data={
            'K': 'Kilometros',
            'H': 'Horas',
            'F': 'Fechas',
        })
