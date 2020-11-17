# coding=utf-8
import datetime
import decimal
import operator
import re

import xlsxwriter
from PyQt5 import QtCore
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QFileDialog, QTableView

from controladores.PadronAfip import PadronAfip
from libs import Ventanas, Constantes
from libs.EntradaTexto import CUITDelegate
from libs.Fechas import FechaDelegate
from libs.utiles import EsVerdadero, AbrirArchivo, saveFileDialog, inicializar_y_capturar_excepciones
from modelos.Bancos import Banco
from modelos.Cuentas import Cuenta
from modelos.MovimientosDeCaja import MovCaja
from modelos.TipoDeValores import TipoDeValor


class Grilla(QTableWidget):

    #columnas a ocultar
    columnasOcultas = []

    #lista con las cabeceras de la grilla
    cabeceras = []

    #tabla desde la cual obtener los datos
    tabla = None

    #campos de la tabla
    campos = None

    #condiciones para filtrar los datos
    condiciones = None

    #cantidad de registros a mostrar
    limite = 100

    #columnas habilitadas
    columnasHabilitadas = []

    #campos tabla
    camposTabla = None

    #valores a cargar
    data = None

    #indica si esta en la grilla
    engrilla = False

    #indica si las columnas son seleccionables o no
    enabled = True

    #widget para las columnas
    widgetCol = {}

    #color para la columna
    backgroundColorCol = {}

    #tamaño de la fuente
    tamanio = 10

    #emit signal
    keyPressed = QtCore.pyqtSignal(int, bool, bool)

    when = QtCore.pyqtSignal()

    #modificadores de teclas
    shift = False
    ctrl = False

    #indica si permite agregar registros
    permiteagregar = True

    #controla la tecla enter para pasar al siguiente campo
    controlaenter = False

    def __init__(self, *args, **kwargs):

        QTableWidget.__init__(self, *args)
        if 'tamanio' in kwargs:
            self.tamanio = kwargs['tamanio']
        font = QFont()
        font.setPointSizeF(self.tamanio)
        self.setFont(font)
        if 'habilitarorden' in kwargs:
            self.setSortingEnabled(kwargs['habilitarorden'])
        else:
            self.setSortingEnabled(True)
        if 'enabled' in kwargs:
            self.setEnabled(kwargs['enabled'])

    def ArmaCabeceras(self, cabeceras=None):

        if not cabeceras:
            cabeceras = self.cabeceras

        self.setColumnCount(len(cabeceras))

        for col in range(0, len(cabeceras)):
            self.setHorizontalHeaderItem(col, QTableWidgetItem(cabeceras[col]))

        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        self.cabeceras = cabeceras
        self.OcultaColumnas()

    def AgregaItem(self, items=None,
                   backgroundColor=QColor(255,255,255), readonly=False):

        if items:
            col = 0
            cantFilas = self.rowCount() + 1
            self.setRowCount(cantFilas)
            for x in items:
                flags = QtCore.Qt.ItemIsSelectable
                if isinstance(x, (bool)):
                    item = QTableWidgetItem(x)
                    if x:
                        item.setCheckState(QtCore.Qt.Checked)
                    else:
                        item.setCheckState(QtCore.Qt.Unchecked)
                elif isinstance(x, (int, float, decimal.Decimal)):
                    item = QTableWidgetItem(str(x))
                    item.setTextAlignment(Qt.AlignRight)
                elif isinstance(x, (datetime.date)):
                    fecha = x.strftime('%d/%m/%Y')
                    item = QTableWidgetItem(fecha)
                elif isinstance(x, (bytes)):
                    if EsVerdadero(x):
                        item = 'Si'
                    else:
                        item = 'No'
                    item = QTableWidgetItem(QTableWidgetItem(x))
                else:
                    item = QTableWidgetItem(QTableWidgetItem(x))

                if readonly:
                    flags = QtCore.Qt.ItemIsSelectable
                elif col in self.columnasHabilitadas:
                    if isinstance(x, (bool)):
                        flags |= QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsEnabled
                    else:
                        flags |= QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
                else:
                    if self.enabled and not readonly:
                        flags |= QtCore.Qt.ItemIsEnabled

                item.setFlags(flags)
                if col in self.backgroundColorCol:
                    item.setBackground(self.backgroundColorCol[col])

                if backgroundColor and isinstance(backgroundColor, QColor):
                    item.setBackground(backgroundColor)

                self.setItem(cantFilas - 1, col, item)
                # if self.widgetCol:
                #     self.ArmaWidgetCol(col)
                if col in self.widgetCol:
                   widgetColumna = self.widgetCol[col]
                   self.setItemDelegateForColumn(col, widgetColumna)
                   # self.setItemDelegate(widgetColumna)
                   # self.setCellWidget(cantFilas - 1, col, widgetColumna)
                col += 1
            self.resizeRowsToContents()
            self.resizeColumnsToContents()

    # def ArmaWidgetCol(self, col):
    #     for x in range(self.rowCount()):
    #         if col in self.widgetCol:
    #             # self.setCellWidget(x, col, self.widgetCol[col])
    #             self.setItemDelegate(widgetColumna)
    #
    def OcultaColumnas(self):
        for x in self.columnasOcultas:
            if not isinstance(x, int):
                numCol = self.cabeceras.index(x)
            else:
                numCol = x
            self.hideColumn(numCol)

    def ModificaItem(self, valor, fila, col, backgroundColor=None):
        """

        :param fila: la fila que se quiere modificar
        :param valor: valor a modificar
        :type col: entero en caso de indicar un numero de columna y string si quiero el nombre
        """
        if isinstance(valor, (int, float, decimal.Decimal)):
            item = QTableWidgetItem(str(valor))
        elif isinstance(valor, (datetime.date)):
            fecha = valor.strftime('%d/%m/%Y')
            item = QTableWidgetItem(fecha)
        else:
            item = QTableWidgetItem(valor)

        if not isinstance(col, int):
            numCol = self.cabeceras.index(col)
        else:
            numCol = col

        if numCol in self.columnasHabilitadas:
            item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable)
        else:
            # item.setFlags(QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled)
            item.setFlags(QtCore.Qt.ItemIsSelectable)

        if col in self.backgroundColorCol:
            item.setBackground(self.backgroundColorCol[col])

        self.setItem(fila, numCol, item)
        self.resizeColumnsToContents()
        #self.dataChanged()

    def ObtenerItem(self, fila, col):

        if isinstance(col, int):
            numCol = col
        else:
            numCol = self.cabeceras.index(col)

        try:
            item = self.item(fila, numCol)
            if item.checkState() == QtCore.Qt.Checked:
                item = True
            else:
                item = item.text()
                item = item.replace(',', '.') #if item else 0

        except:
            item = ''

        # return item.replace(',','.') if item else 0
        return item

    def ObtenerItemNumerico(self, fila, col):

        if isinstance(col, int):
            numCol = col
        else:
            numCol = self.cabeceras.index(col)

        try:
            item = self.item(fila, numCol)
            if item.checkState() == QtCore.Qt.Checked:
                item = True
            else:
                item = item.text()
                item = re.sub("[^-0123456789\.]","",item)

            item = float(item)
        except:
            item = 0

        # return item.replace(',','.') if item else 0
        return item

    def CargaDatos(self, avance=None):
        self.blockSignals(True)
        self.setRowCount(0)
        self.blockSignals(False)

    def focusInEvent(self, *args, **kwargs):
        self.engrilla = True
        if self.rowCount() == 0:
            self.AgregaNuevo()
        super().focusInEvent(*args, **kwargs)
        self.when.emit()

    def focusOutEvent(self, *args, **kwargs):
        self.engrilla = False
        super().focusOutEvent(*args, **kwargs)

    def HabilitaColumnas(self, fila=1):

        for col in range(self.columnCount()):
            valor = self.ObtenerItem(fila=fila, col=col)
            self.ModificaItem(valor=valor, fila=fila, col=col)

    def ExportaExcel(self, columnas=None, archivo=""):
        if not columnas:
            columnas = self.cabeceras

        archivo = archivo.replace('.', '').replace('/', '')
        if not archivo.startswith("excel"):
            archivo = "excel/" + archivo

        cArchivo = saveFileDialog(filename=archivo,
                                  files="Archivos de Excel (*.xlsx)")
        # cArchivo = QFileDialog.getSaveFileName(caption="Guardar archivo", directory="", filter="*.XLSX")
        if not cArchivo:
            return

        workbook = xlsxwriter.Workbook(cArchivo)
        worksheet = workbook.add_worksheet()

        fila = 0
        col = 0
        for c in columnas:
            worksheet.write(fila, col, c)
            col += 1

        fila +=1
        for row in range(self.rowCount()):
            col = 0
            for c in columnas:
                dato = self.ObtenerItem(fila=row, col=c).strip()
                try:
                    dato = float(dato)
                except:
                    if dato.isdigit():
                        dato = int(dato)
                worksheet.write(fila, col, dato)
                col += 1
            fila += 1

        workbook.close()
        AbrirArchivo(cArchivo)

    def keyPressEvent(self, event):
        super(Grilla, self).keyPressEvent(event)
        self.shift = False
        self.ctrl = False
        if (event.modifiers() & Qt.ShiftModifier):
            self.shift = True
        if (event.modifiers() & Qt.ControlModifier):
            self.ctrl = True

        col = self.currentColumn()
        row = self.currentRow()
        if event.key() in [Qt.Key_Return, Qt.Key_Enter] and self.controlaenter:
            if col + 1 == self.columnCount() and row + 1 == self.rowCount():
                if self.permiteagregar:
                    item = ['' for x in self.cabeceras]
                    self.AgregaItem(item)
                    self.Activar(row=self.rowCount(), col=0)
            elif col == self.columnCount():
                self.Activar(row=row + 1, col=0)
            else:
                self.Activar(col=col + 1)
        elif event.key() == Qt.Key_Down and row + 1 == self.rowCount():
            if self.permiteagregar:
                item = ['' for x in self.cabeceras]
                self.AgregaItem(item)
                # self.Activar(row=row + 1, col=0)

        self.keyPressed.emit(event.key(), self.shift, self.ctrl)

    def SumaTodo(self, col=None):
        total = 0.
        for row in range(self.rowCount()):
            monto = float(self.ObtenerItem(fila=row, col=col) or '0')
            total += monto
        return total

    def Activar(self, row=-1, col=0):
        if row == -1:
            row = self.rowCount() - 1
        self.setCurrentCell(row, col)
        self.setFocus()

    def BorraItemCodigo(self, codigo=None, col=0):
        if not codigo:
            return 0

        cant = 0
        for row in range(self.rowCount()):
            dato = self.ObtenerItem(fila=row, col=col)
            if dato == codigo:
                self.removeRow(row)
                cant += 1
        return cant

    def AgregaNuevo(self):
        items = ['' for x in self.cabeceras]
        self.AgregaItem(items)


class MiTableModel(QAbstractTableModel):
    #columnas habilitadas
    columnasHabilitadas = []
    #_colorColumn = {2:QColor(255, 255, 204),4:QColor(255, 128, 128)}
    _colorColumn = {}

    def __init__(self, datain, headerdata, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.headerdata = headerdata

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.arraydata)

    def columnCount(self, parent=None, *args, **kwargs):
        if self.arraydata:
            return len(self.arraydata[0])
        else:
            return 0

    def data(self, index, role=None):
        if not index.isValid():
            return None
        value = self.arraydata[index.row()][index.column()]
        if role == Qt.EditRole:
            return value
        elif role == Qt.DisplayRole:
            return value
        elif role == Qt.ItemIsSelectable:
            return value
        elif role == Qt.BackgroundRole and index.column() in(self._colorColumn):
            return self._colorColumn[index.column()]
        return QVariant()

    def headerData(self, col, orientation, role=None):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.headerdata[col])
        return QVariant()

    def sort(self, col, order=None):
        self.layoutAboutToBeChanged.emit()
        self.arraydata = sorted(self.arraydata, key=operator.itemgetter(col))
        if order == Qt.DescendingOrder:
            self.arraydata.reverse()
        self.layoutChanged.emit()

    def flags(self, index):
        flags = super(self.__class__, self).flags(index)
        flags |= Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
        if index.column() in self.columnasHabilitadas:
            flags |= Qt.ItemIsEditable
        return flags

    def setData(self, index, value, role=None):
        if role == Qt.EditRole:
            row = index.row()
            column = index.column()
            ch = (value)
            self.arraydata[row][column] = ch
            self.dataChanged.emit(index,index)
            return True

    def ModificaDato(self, fila=0, col=0, valor=None):
        self.arraydata[fila][col] = valor

class MiQTableView(QTableView):
    def __init__(self, *args, **kwargs):
        QTableView.__init__(self, *args, **kwargs) #Use QTableView constructor


class GrillaModel(MiQTableView):

    #columnas a ocultar
    columnasOcultas = []

    #emit signal
    keyPressed = QtCore.pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__()
        font = QFont()
        font.setPointSizeF(12)
        self.setFont(font)

    def ObtenerItem(self, fila=0, col=0):
        #en caso de que le pase el nombre de la columnna busco el indice del header
        if isinstance(col, (str,)):
            col = self.model().headerdata.index(col)

        index = self.model().index(fila, col)

        return index.data()

    def ModificaItem(self, fila=0, col=0, valor=''):
        #en caso de que le pase el nombre de la columnna busco el indice del header
        if isinstance(col, (str,)):
            col = self.model().headerdata.index(col)

        index = self.model().index(fila, col)
        if isinstance(valor, (int, float, decimal.Decimal)):
            valor = str(valor)

        self.model().setData(index, valor, role=Qt.EditRole)

    def OcultarColumnas(self):
        for i in self.columnasOcultas:
            if isinstance(i, (str,)):
                col = self.model().headerdata.index(i)
            else:
                col = i

            self.hideColumn(col)

    def keyPressEvent(self, event):
        super(GrillaModel, self).keyPressEvent(event)
        self.keyPressed.emit(event.key())

class GrillaValores(Grilla):

    controlaenter = True
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CreaCabecera()
        # self.cellChanged.connect(self.onCurrentCellChanged)

    @inicializar_y_capturar_excepciones
    def keyPressEvent(self, event, *args, **kwargs):
        col = self.currentColumn()
        row = self.currentRow()
        # print(event.key())
        if col == 1 and event.key() == Qt.Key_F2:
            _ventana = TipoDeValor().Busqueda()
            if _ventana.lRetval:
                self.ModificaItem(valor=_ventana.ValorRetorno,
                                                   fila=row, col=1)
                self.ModificaItem(valor=_ventana.campoRetornoDetalle,
                                                   fila=row, col='Detalle')
        elif col == 0 and event.key() == Qt.Key_F2:
            _ventana = Cuenta.Busqueda()
            if _ventana.lRetval:
                self.ModificaItem(valor=_ventana.ValorRetorno,
                                  fila=row, col=0)
        if event.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab] and col == 1:
            codigo = self.ObtenerItem(fila=row, col=1)
            if codigo:
                try:
                    valor = TipoDeValor.get_by_id(codigo)
                    self.ModificaItem(valor=valor.nombre, fila=row, col='Detalle')
                except TipoDeValor.DoesNotExist:
                    self.ModificaItem(valor="", fila=row, col='Detalle')
                if codigo == '1':
                    self.columnasHabilitadas = [0, 1, 4]
                    self.HabilitaColumnas(fila=row)
                else:
                    self.columnasHabilitadas = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                    self.HabilitaColumnas(fila=row)
        # if event.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab] and col == 7:
        #     cuit = self.ObtenerItem(fila=self.currentRow(), col=7)
        #     padron = PadronAfip()
        #     padron.ConsultarPersona(int(str(cuit).replace("-", "")))
        if event.key() in [Qt.Key_Return, Qt.Key_Enter, Qt.Key_Tab] and col == 3:
            interno = self.ObtenerItemNumerico(fila=row, col='Interno')
            valor = self.ObtenerItemNumerico(fila=row, col='Valor')
            if interno != 0:
                movcaja = MovCaja.select().where(
                    MovCaja.tipovalor == valor,
                    MovCaja.interno == interno,
                )
                if movcaja.count() > 1:
                    Ventanas.showAlert("Sistema", "Valor ya entregado en orden de pago")
                elif movcaja.count() == 1:
                    if movcaja[0].caja == 'S':
                        self.ModificaItem(valor=movcaja[0].banco.codigo, fila=row, col='Banco')
                        self.ModificaItem(valor=movcaja[0].sucursal, fila=row, col='Sucursal')
                        if isinstance(movcaja[0].vence, datetime.date):
                            self.ModificaItem(valor=movcaja[0].vence, fila=row, col='Vencimiento')
                        self.ModificaItem(valor=movcaja[0].importe, fila=row, col='Importe')
                        self.ModificaItem(valor=movcaja[0].numero, fila=row, col='Numero')
                        self.ModificaItem(valor=movcaja[0].cuit, fila=row, col='CUIT')
                        self.ModificaItem(valor=movcaja[0].cp, fila=row, col='CP')
                        self.ModificaItem(valor=movcaja[0].ctaban, fila=row, col='Cta Ban')
                    else:
                        Ventanas.showAlert("Sistema", "Valor no encontrado en caja")

        if event.key() == Qt.Key_F2 and col == 5:
            _ventana = Banco().Busqueda()
            if _ventana.lRetval:
                self.ModificaItem(valor=_ventana.ValorRetorno,
                                  fila=row, col=4)
        super().keyPressEvent(event)
        self.keyPressed.emit(event.key(),self.shift, self.ctrl)

    def CreaCabecera(self):
        self.widgetCol = {
            8: FechaDelegate(),
            9: CUITDelegate()
        }
        self.enabled = True
        cabecera = [
            'Caja', 'Valor', 'Detalle', 'Interno', 'Importe', 'Banco', 'Sucursal', 'Numero', 'Vencimiento', 'CUIT', 'Dato',
            'Cta Ban', 'CP', 'id'
        ]
        self.ArmaCabeceras(cabecera)
        self.columnasHabilitadas = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        self.columnasOcultas = [12,]
        self.OcultaColumnas()
        self.AgregaNuevo()

    def AgregaNuevo(self):
        item = [
            Constantes.CAJAPORDEFECTO, '','', '', 0, '', '', '', '', '', '', '', '', 0
        ]
        self.AgregaItem(item)

    @inicializar_y_capturar_excepciones
    def SumaTodo(self, col='', *args, **kwargs):
        nTotal = 0.
        for x in range(self.rowCount()):
            pago = self.ObtenerItemNumerico(fila=x, col='Importe')
            nTotal += float(pago)

        return nTotal

    def Valida(self):
        valido = True
        for row in range(self.rowCount()):
            caja = self.ObtenerItem(fila=row, col='Caja') or '0'
            try:
                cuenta = Cuenta.get_by_id(caja)
            except Cuenta.DoesNotExist:
                Ventanas.showAlert("Sistema", "No existe la caja")
                valido = False
            valor = self.ObtenerItem(fila=row, col='Valor') or '0'
            try:
                banco = TipoDeValor.get_by_id(valor)
            except TipoDeValor.DoesNotExist:
                Ventanas.showAlert("Sistema", "Tipo de valor inexistente")
                valido = False

        return valido

    @inicializar_y_capturar_excepciones
    def onCurrentCellChanged(self, fila1, col1, *args, **kwargs):
        print(fila1, col1)
        row = fila1
        #se busca el interno del valor para cargar los datos
        interno = self.ObtenerItemNumerico(fila=row, col='Interno')
        valor = self.ObtenerItemNumerico(fila=row, col='Valor')
        if interno != 0:
            movcaja = MovCaja.select().where(
                MovCaja.tipovalor == valor,
                MovCaja.interno == interno,
            )
            # cabecera = [
            #     'Caja', 'Valor', 'Detalle', 'Interno', 'Importe', 'Banco', 'Sucursal', 'Numero', 'Vencimiento', 'CUIT',
            #     'Dato',
            #     'Cta Ban', 'CP', 'id'
            # ]
            if movcaja.count() == 1:
                if movcaja[0].caja == 'S':
                    self.ModificaItem(valor=movcaja[0].banco.codigo, fila=row, col='Banco')
                    self.ModificaItem(valor=movcaja[0].sucursal, fila=row, col='Sucursal')
                    if isinstance(movcaja[0].vence, datetime.date):
                        self.ModificaItem(valor=movcaja[0].vence, fila=row, col='Vencimiento')
                    self.ModificaItem(valor=movcaja[0].importe, fila=row, col='Importe')
                    self.ModificaItem(valor=movcaja[0].numero, fila=row, col='Numero')
                    self.ModificaItem(valor=movcaja[0].cuit, fila=row, col='CUIT')
                    self.ModificaItem(valor=movcaja[0].cp, fila=row, col='CP')
                    self.ModificaItem(valor=movcaja[0].ctaban, fila=row, col='Cta Ban')
                    self.columnasHabilitadas = [0, 1, 3]
                    self.HabilitaColumnas(fila=row)
            else:
                self.columnasHabilitadas = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                self.HabilitaColumnas(fila=row)

        #se busca el codigo del valor
        codigo = self.ObtenerItem(fila=row, col=1)
        if codigo:
            try:
                valor = TipoDeValor.get_by_id(codigo)
                self.ModificaItem(valor=valor.nombre, fila=row, col='Detalle')
            except TipoDeValor.DoesNotExist:
                self.ModificaItem(valor="", fila=row, col='Detalle')
            if codigo == '1':
                self.columnasHabilitadas = [0, 1, 4]
                self.HabilitaColumnas(fila=row)
            else:
                self.columnasHabilitadas = [0, 1, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                self.HabilitaColumnas(fila=row)

