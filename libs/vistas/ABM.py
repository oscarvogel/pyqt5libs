# coding=utf-8
import datetime
import decimal
import logging

from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QVBoxLayout, QTabWidget, QWidget, QGridLayout, QHBoxLayout, QLineEdit, QCheckBox, QComboBox, \
    QApplication, QMessageBox, QSplitter

from modelos.ModeloBase import reconnect_if_needed
from pyqt5libs.libs.vistas.VistaBase import VistaBase
from pyqt5libs.pyqt5libs import Ventanas
from pyqt5libs.pyqt5libs.BarraProgreso import Avance
from pyqt5libs.pyqt5libs.Botones import Boton
from pyqt5libs.pyqt5libs.Checkbox import CheckBox
from pyqt5libs.pyqt5libs.EntradaTexto import EntradaTexto
from pyqt5libs.pyqt5libs.Etiquetas import Etiqueta
from pyqt5libs.pyqt5libs.Fechas import Fecha, FechaLine
from pyqt5libs.pyqt5libs.Grillas import Grilla
from pyqt5libs.pyqt5libs.Spinner import Spinner
from pyqt5libs.pyqt5libs.Validaciones import ValidaConTexto
from pyqt5libs.pyqt5libs.utiles import inicializar_y_capturar_excepciones, EsVerdadero, imagen


class ABM(VistaBase):
    """Vista base para pantallas de gestión tipo listado + ficha.

    Mantiene compatibilidad con los ABM existentes, pero incorpora mejoras de
    usabilidad: títulos más claros, búsqueda con limpiar, resumen de registros,
    estado visual de alta/modificación, conexiones protegidas, atajos de
    teclado, distribución responsive opcional y modo split listado/ficha.
    """

    controles = {}
    model = None
    tipo = "A"
    camposAMostrar = []
    condicion = None
    limite = 100
    ordenBusqueda = None
    campoClave = None
    autoincremental = True
    campoFoco = None
    colBoton = 0
    titulo = None
    permiteagregar = True
    idtabla = 0
    dynamicBackColor = None
    data = ""
    autoConectaWidgets = True

    # Contenedor principal. `tabs` conserva el comportamiento histórico.
    # `split` muestra listado y ficha al mismo tiempo.
    view_mode = "tabs"
    split_sizes = (520, 380)

    # Layout de ficha. Por defecto se mantiene compatible con el armado histórico.
    # Valores soportados: single, two_columns, auto.
    form_layout_mode = "single"
    form_columns = 1
    form_auto_columns_threshold = 8

    def __init__(self, *args, **kwargs):
        VistaBase.__init__(self, *args, **kwargs)
        self.controles = {}
        self._widgets_conectados = False
        self._ultima_cantidad_registros = 0
        self._form_row = 0
        self._form_column = 0
        self._form_fields_count = 0
        self.initUi()

    def _nombre_pantalla(self):
        if self.titulo:
            return self.titulo
        if self.model:
            return self.model._meta.table_name.title()
        return "Registros"

    def _titulo_gestion(self):
        return "Gestión de {}".format(self._nombre_pantalla())

    def _usa_modo_split(self):
        return self.view_mode == "split"

    def _usa_layout_responsive(self):
        return self.form_layout_mode in ("auto", "two_columns")

    def _columnas_formulario(self):
        if self.form_layout_mode == "two_columns":
            return max(1, int(self.form_columns or 2))
        if self.form_layout_mode == "auto":
            if self._form_fields_count >= self.form_auto_columns_threshold:
                return 2
        return 1

    def _agrega_layout_campo(self, boxlayout):
        if not self._usa_layout_responsive():
            self.verticalLayoutDatos.addLayout(boxlayout)
            return

        columnas = self._columnas_formulario()
        if columnas <= 1:
            self.verticalLayoutDatos.addLayout(boxlayout)
            return

        if not hasattr(self, 'gridLayoutFormulario'):
            self.gridLayoutFormulario = QGridLayout()
            self.gridLayoutFormulario.setObjectName("gridLayoutFormulario")
            self.gridLayoutFormulario.setHorizontalSpacing(18)
            self.gridLayoutFormulario.setVerticalSpacing(8)
            self.verticalLayoutDatos.addLayout(self.gridLayoutFormulario)

        self.gridLayoutFormulario.addLayout(boxlayout, self._form_row, self._form_column, 1, 1)
        self._form_column += 1
        if self._form_column >= columnas:
            self._form_column = 0
            self._form_row += 1

    def _configura_contenedor_principal(self):
        if self._usa_modo_split():
            self.splitter = QSplitter(Qt.Horizontal)
            self.splitter.setObjectName("splitterABM")
            self.splitter.addWidget(self.tabLista)
            self.splitter.addWidget(self.tabDetalle)
            self.splitter.setSizes(list(self.split_sizes))
            self.verticalLayout.addWidget(self.splitter)
        else:
            self.tabWidget = QTabWidget()
            self.tabWidget.addTab(self.tabLista, "Listado")
            self.tabWidget.addTab(self.tabDetalle, "Ficha")
            self.verticalLayout.addWidget(self.tabWidget)
        self.tabDetalle.setEnabled(False)

    def _mostrar_listado(self):
        if self._usa_modo_split():
            self.tabDetalle.setEnabled(False)
            self.tableView.setFocus()
        else:
            self.tabWidget.setCurrentIndex(0)
            self.tabDetalle.setEnabled(False)

    def _mostrar_ficha(self):
        self.tabDetalle.setEnabled(True)
        if self._usa_modo_split():
            self.tabDetalle.setFocus()
        else:
            self.tabWidget.setCurrentIndex(1)

    def _esta_en_listado(self):
        if self._usa_modo_split():
            return True
        return self.tabWidget.currentWidget() == self.tabLista

    def _esta_en_ficha(self):
        if self._usa_modo_split():
            return self.tabDetalle.isEnabled()
        return self.tabWidget.currentWidget() == self.tabDetalle and self.tabDetalle.isEnabled()

    def ActualizaEstado(self, texto=None):
        if not hasattr(self, 'lblEstado'):
            return
        if texto:
            self.lblEstado.setText(texto)
            return
        if self.tipo == 'M':
            self.lblEstado.setText("Editando registro {}".format(self.idtabla or "seleccionado"))
        else:
            self.lblEstado.setText("Nuevo registro")

    def ActualizaResumen(self, mostrados=0, total=0):
        if not hasattr(self, 'lblResumen'):
            return
        if total > self.limite:
            self.lblResumen.setText("Mostrando {} de {} registros".format(mostrados, total))
        else:
            self.lblResumen.setText("{} registro(s) encontrado(s)".format(mostrados))

    @inicializar_y_capturar_excepciones
    def initUi(self, *args, **kwargs):
        self.resize(906, 584)
        self.setWindowTitle(self._titulo_gestion())

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setContentsMargins(18, 18, 18, 14)
        self.verticalLayout.setSpacing(12)

        self.lblTitulo = Etiqueta(tamanio=15, texto=self._titulo_gestion())
        self.lblTitulo.setObjectName("tituloPantalla")
        self.verticalLayout.addWidget(self.lblTitulo)

        self.avance = Avance()
        self.avance.setVisible(False)
        self.verticalLayout.addWidget(self.avance)

        self.tabLista = QWidget()
        self.gridLayout = QGridLayout(self.tabLista)
        self.gridLayout.setContentsMargins(14, 14, 14, 14)
        self.gridLayout.setSpacing(10)

        self.lineEditBusqueda = EntradaTexto(
            self.tabLista,
            placeholderText="Buscar por nombre, código o dato visible..."
        )
        self.lineEditBusqueda.setObjectName("lineEditBusqueda")
        self.gridLayout.addWidget(self.lineEditBusqueda, 0, 0, 1, 1)

        self.btnLimpiarBusqueda = Boton(
            self.tabLista,
            texto="Limpiar",
            imagen=imagen('close.png'),
            tamanio=QSize(24, 24),
            tooltip="Limpiar búsqueda"
        )
        self.btnLimpiarBusqueda.setObjectName("btnLimpiarBusqueda")
        self.gridLayout.addWidget(self.btnLimpiarBusqueda, 0, 1, 1, 1)

        self.tableView = Grilla(self.tabLista)
        self.tableView.setObjectName("tableView")
        self.tableView.enabled = True
        self.tableView.cabeceras = [
            x.verbose_name if x.verbose_name else x.column_name.capitalize()
            for x in self.camposAMostrar
        ]
        self.tableView.ArmaCabeceras()
        self.gridLayout.addWidget(self.tableView, 1, 0, 1, 2)

        self.lblResumen = Etiqueta(texto="Sin registros cargados")
        self.lblResumen.setObjectName("lblResumen")
        self.gridLayout.addWidget(self.lblResumen, 2, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSpacing(8)
        self.horizontalLayout.addStretch()

        self.BotonesAdicionales()

        self.btnAgregar = Boton(self.tabLista, texto="&Agregar",
                                imagen=imagen("new.png"), tamanio=QSize(32, 32),
                                tooltip='Agregar nuevo registro (F2)', enabled=self.permiteagregar)
        self.btnAgregar.setObjectName("btnAgregar")
        self.horizontalLayout.addWidget(self.btnAgregar)

        self.btnEditar = Boton(self.tabLista, imagen=imagen('edit.png'), tamanio=QSize(32, 32),
                               tooltip='Modificar registro seleccionado (F4 o doble clic)', texto='Editar')
        self.btnEditar.setObjectName("btnEditar")
        self.horizontalLayout.addWidget(self.btnEditar)

        self.btnBorrar = Boton(self.tabLista, imagen=imagen('delete.png'), tamanio=QSize(32, 32),
                               tooltip='Borrar registro seleccionado (Delete)', texto='Borrar')
        self.btnBorrar.setObjectName("btnBorrar")
        self.horizontalLayout.addWidget(self.btnBorrar)

        self.btnExcel = Boton(self.tabLista, imagen=imagen("79354_excel_icon.png"), tamanio=QSize(32, 32),
                              tooltip='Exportar listado a Excel', texto='Excel')
        self.horizontalLayout.addWidget(self.btnExcel)

        self.btnCerrar = Boton(self.tabLista, imagen=imagen('close.png'), tamanio=QSize(32, 32),
                               tooltip='Cerrar pantalla', texto='Cerrar')
        self.btnCerrar.setObjectName("btnCerrar")
        self.horizontalLayout.addWidget(self.btnCerrar)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 0, 1, 2)

        self.tabDetalle = QWidget()
        self.ArmaDatos()
        self._configura_contenedor_principal()
        self.ArmaTabla()
        if self.autoConectaWidgets:
            self.ConectaWidgets()

    def BotonesAdicionales(self):
        pass

    @reconnect_if_needed
    @inicializar_y_capturar_excepciones
    def ArmaTabla(self, *args, **kwargs):
        self.tableView.setRowCount(0)
        self.avance.setVisible(True)
        try:
            if self.data:
                data = self.data
            else:
                if not self.model:
                    self.ActualizaResumen(0, 0)
                    return
                data = self.model.select().dicts()
                if self.condicion:
                    for c in self.condicion:
                        data = data.where(c)

            if self.lineEditBusqueda.text():
                data = self.ArmaBusqueda(data)

            total = len(data)
            avance = 0
            data = data.limit(self.limite)
            for d in data:
                color = QColor(255, 255, 255)
                avance += 1
                if total:
                    self.avance.actualizar(avance / total * 100)
                if self.camposAMostrar:
                    item = [d[x.name] for x in self.camposAMostrar]
                else:
                    item = [d[x] for x in d]
                for x in d:
                    if self.dynamicBackColor:
                        if x in self.dynamicBackColor:
                            if d[x] == self.dynamicBackColor[x]['valor']:
                                color = self.dynamicBackColor[x]['color']
                            else:
                                color = QColor(255, 255, 255)
                    else:
                        color = self.DevuelveColor(d)
                self.tableView.AgregaItem(item, backgroundColor=color)
            self._ultima_cantidad_registros = avance
            self.ActualizaResumen(avance, total)
        finally:
            self.avance.setVisible(False)

    def ArmaBusqueda(self, data):
        if self.ordenBusqueda:
            texto = self.lineEditBusqueda.text()
            if isinstance(self.ordenBusqueda, list):
                cond = None
                for campo in self.ordenBusqueda:
                    expr = campo.contains(texto)
                    cond = expr if cond is None else cond | expr
                data = data.where(cond)
            else:
                data = data.where(self.ordenBusqueda.contains(texto))
        else:
            Ventanas.showAlert("Sistema", "No hay campos configurados para realizar la búsqueda")
        return data

    @reconnect_if_needed
    @inicializar_y_capturar_excepciones
    def ArmaDatos(self, *args, **kwargs):
        self.verticalLayoutDatos = QVBoxLayout(self.tabDetalle)
        self.verticalLayoutDatos.setObjectName("verticalLayoutDatos")

        self.lblEstado = Etiqueta(texto="Seleccione un registro o agregue uno nuevo")
        self.lblEstado.setObjectName("lblEstado")
        self.verticalLayoutDatos.addWidget(self.lblEstado)

        self.ArmaCarga()
        self.colBoton = 0

        self.grdBotones = QGridLayout()
        self.grdBotones.setObjectName("grdBotones")
        self.AgregaBotonesDatos()

        self.btnAceptar = Boton(self.tabDetalle, texto='Guardar', imagen=imagen('save.png'), tamanio=QSize(32, 32),
                                tooltip="Guardar cambios (F10)")
        self.btnAceptar.setObjectName("btnAceptar")
        self.grdBotones.addWidget(self.btnAceptar, 0, self.colBoton, 1, 1)

        self.colBoton += 1
        self.btnCancelar = Boton(self.tabDetalle, texto='Cancelar', imagen=imagen('close.png'), tamanio=QSize(32, 32),
                                 tooltip="Cancelar y volver al listado (Esc)")
        self.btnCancelar.setObjectName("btnCancelar")
        self.grdBotones.addWidget(self.btnCancelar, 0, self.colBoton, 1, 1)
        self.verticalLayoutDatos.addLayout(self.grdBotones)
        self.btnCancelar.clicked.connect(self.btnCancelarClicked)
        self.btnAceptar.clicked.connect(self.btnAceptarClicked)
        self.verticalLayoutDatos.addStretch(1)

    def Busqueda(self):
        self.ArmaTabla()

    def LimpiarBusqueda(self):
        self.lineEditBusqueda.clear()
        self.ArmaTabla()
        self.lineEditBusqueda.setFocus()

    def ConectaWidgets(self):
        if self._widgets_conectados:
            return
        self.lineEditBusqueda.textChanged.connect(self.Busqueda)
        self.btnLimpiarBusqueda.clicked.connect(self.LimpiarBusqueda)
        self.btnCerrar.clicked.connect(self.cerrarformulario)
        self.btnBorrar.clicked.connect(self.Borrar)
        self.btnEditar.clicked.connect(self.Modifica)
        self.btnAgregar.clicked.connect(self.Agrega)
        self._conecta_doble_click_grilla()
        self._widgets_conectados = True

    def _conecta_doble_click_grilla(self):
        try:
            self.tableView.doubleClicked.connect(self.Modifica)
        except AttributeError:
            if hasattr(self.tableView, 'cellDoubleClicked'):
                self.tableView.cellDoubleClicked.connect(lambda *_: self.Modifica())

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_F2:
            self.Agrega()
            return
        if key == Qt.Key_F3:
            self.lineEditBusqueda.setFocus()
            self.lineEditBusqueda.selectAll()
            return
        if key == Qt.Key_F4:
            self.Modifica()
            return
        if key == Qt.Key_Delete:
            if self._esta_en_listado():
                self.Borrar()
                return
        if key in (Qt.Key_Return, Qt.Key_Enter):
            if self._esta_en_listado():
                self.Modifica()
                return
        if key == Qt.Key_F10:
            if self._esta_en_ficha():
                self.btnAceptarClicked()
                return
        if key == Qt.Key_Escape:
            if self._esta_en_ficha():
                self.btnCancelarClicked()
            else:
                self.cerrarformulario()
            return
        super().keyPressEvent(event)

    @reconnect_if_needed
    @inicializar_y_capturar_excepciones
    def Borrar(self, *args, **kwargs):
        if not self.tableView.currentRow() != -1:
            Ventanas.showAlert("Sistema", "Seleccione un registro para borrar")
            return

        if not self.campoClave:
            Ventanas.showAlert("Sistema", "No se pudo identificar el registro seleccionado")
            return

        if Ventanas.showConfirmation("Sistema", "¿Desea borrar el registro seleccionado?") == QMessageBox.Ok:
            id = self.tableView.ObtenerItem(fila=self.tableView.currentRow(), col=self.campoClave.column_name.capitalize())
            data = self.model.get_by_id(id)
            data.delete_instance()
            self.ArmaTabla()

    @reconnect_if_needed
    @inicializar_y_capturar_excepciones
    def Modifica(self, *args, **kwargs):
        self.tipo = 'M'
        if not self.tableView.currentRow() != -1:
            Ventanas.showAlert("Sistema", "Seleccione un registro para editar")
            return

        if not self.campoClave:
            Ventanas.showAlert("Sistema", "No se pudo identificar el registro seleccionado")
            return

        id = self.tableView.ObtenerItem(fila=self.tableView.currentRow(),
                                        col=self.campoClave.verbose_name if self.campoClave.verbose_name else
                                        self.campoClave.column_name.capitalize())
        id = id.replace('.', '')
        self.idtabla = id

        if self.campoClave.field_type in ['VARCHAR']:
            data = self.model.select().where(self.campoClave == id).dicts()
        elif self.campoClave.field_type in ['AUTO', 'INTEGER']:
            data = self.model.select().where(self.campoClave == int(id)).dicts()
        else:
            data = self.model.select().where(self.campoClave == id).dicts()
        self._mostrar_ficha()
        self.ActualizaEstado()
        self.CargaDatos(data)
        if self.campoFoco:
            self.campoFoco.setFocus()
        self.PostClickModifica()

    def CargaDatos(self, data=None):
        if not data:
            return
        for d in data:
            logging.debug("%s", d)
            for k in d:
                if k in self.controles:
                    if k == self.campoClave.name:
                        self.controles[k].setEnabled(False)
                    if isinstance(self.controles[k], QLineEdit):
                        if isinstance(d[k], (int, decimal.Decimal, float)):
                            self.controles[k].setText(str(d[k]))
                        elif isinstance(d[k], datetime.date):
                            self.controles[k].setText(d[k].strftime('%d/%m/%Y'))
                        else:
                            self.controles[k].setText(d[k].strip() if d[k] else '')
                    elif isinstance(self.controles[k], (QCheckBox, CheckBox)):
                        self.controles[k].setChecked(bool(EsVerdadero(d[k]) or d[k]))
                    elif isinstance(self.controles[k], QComboBox):
                        if isinstance(d[k], bytes):
                            cursor = getattr(self, 'cursor', {})
                            if EsVerdadero(cursor.get(k)):
                                self.controles[k].setCurrentIndex(self.controles[k].findData('Si'))
                            else:
                                self.controles[k].setCurrentIndex(self.controles[k].findData('No'))
                        elif isinstance(d[k], (int, decimal.Decimal, float)):
                            self.controles[k].setCurrentIndex(self.controles[k].findData(d[k]))
                        else:
                            self.controles[k].setCurrentText(d[k] if d[k] else '')
                    elif isinstance(self.controles[k], Fecha):
                        if self.controles[k]:
                            self.controles[k].setText(d[k])
                    elif isinstance(self.controles[k], Spinner):
                        self.controles[k].setText(d[k])
                    else:
                        if d[k] is None:
                            self.controles[k].setText('')
                        else:
                            self.controles[k].setText(d[k].strip())

                    self.controles[k].setStyleSheet("background-color: white")

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
                if 'control' not in kwargs:
                    if nombre.field_type in ['DATE']:
                        kwargs['control'] = FechaLine()
                texto = nombre.verbose_name if nombre.verbose_name else nombre.name.capitalize()

        if not isinstance(nombre, str):
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
        if 'layout' in kwargs:
            boxlayout.addLayout(lineEditNombre)
        else:
            boxlayout.addWidget(lineEditNombre)
        if 'enabled' in kwargs:
            lineEditNombre.setEnabled(kwargs['enabled'])

        if 'control' in kwargs and isinstance(kwargs['control'], ValidaConTexto):
            self.controles[nombre] = kwargs['control'].lineEditCodigo
        else:
            self.controles[nombre] = lineEditNombre

        if lAgrega:
            self._form_fields_count += 1
            self._agrega_layout_campo(boxlayout)
        return boxlayout

    def btnCancelarClicked(self):
        self._mostrar_listado()
        self.ActualizaEstado("Seleccione un registro o agregue uno nuevo")

    @inicializar_y_capturar_excepciones
    def btnAceptarClicked(self, *args, **kwargs):
        self._mostrar_listado()
        self.ActualizaEstado("Seleccione un registro o agregue uno nuevo")
        self.ArmaTabla()

    def ArmaCarga(self):
        pass

    def Agrega(self):
        self.tipo = 'A'
        for x in self.controles:
            if self.autoincremental and self.campoClave:
                if x in [self.campoClave.column_name,
                         self.campoClave.verbose_name,
                         self.campoClave.name]:
                    self.controles[x].setEnabled(False)
            self.controles[x].setText('')
            self.controles[x].setStyleSheet("background-color: white")
        self._mostrar_ficha()
        self.ActualizaEstado()
        if self.campoFoco:
            self.campoFoco.setFocus()
        self.PostClickAgrega()

    def PostClickModifica(self):
        pass

    def AgregaBotonesDatos(self):
        pass

    def PostClickAgrega(self):
        pass

    def DevuelveColor(self, item):
        return QColor(255, 255, 255)
