"""Estilo visual Fluent/Windows 11 para pantallas AutoABM.

El objetivo es modernizar la interfaz sin cambiar la lógica del ABM histórico.
"""


def fluent_abm_stylesheet():
    return """
    ABM {
        background: #f6f9ff;
        font-family: "Segoe UI", "Arial", sans-serif;
        font-size: 10.5pt;
        color: #1f1f1f;
    }

    #tituloPantalla {
        font-size: 22pt;
        font-weight: 700;
        color: #111827;
        margin-bottom: 2px;
    }

    #subtituloPantalla {
        color: #5f6368;
        font-size: 11pt;
        margin-bottom: 8px;
    }

    #toolbarABM {
        background: transparent;
        border: none;
        margin-bottom: 8px;
    }

    #tabLista, #tabDetalle, #formPanelABM {
        background: #ffffff;
        border: 1px solid #d8dee9;
        border-radius: 12px;
    }

    #scrollDetalleABM {
        background: transparent;
        border: none;
    }

    #lblEstado {
        font-size: 14pt;
        font-weight: 650;
        color: #111827;
        padding-bottom: 10px;
        border-bottom: 1px solid #edf0f5;
        margin-bottom: 8px;
    }

    #lblResumen {
        color: #4b5563;
        padding-top: 8px;
    }

    #labelNombre {
        color: #374151;
        font-size: 10pt;
        font-weight: 600;
        padding-bottom: 2px;
    }

    #lineEditBusqueda, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
        background: #ffffff;
        border: 1px solid #cfd7e3;
        border-radius: 8px;
        padding: 8px 10px;
        min-height: 20px;
        selection-background-color: #2563eb;
    }

    #lineEditBusqueda:focus, QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
        border: 1px solid #2563eb;
        background: #ffffff;
    }

    QCheckBox {
        spacing: 8px;
        color: #1f2937;
    }

    QTableWidget, QTableView {
        background: #ffffff;
        border: none;
        gridline-color: #eef2f7;
        selection-background-color: #dbeafe;
        selection-color: #111827;
        alternate-background-color: #f8fbff;
    }

    QHeaderView::section {
        background: #ffffff;
        color: #374151;
        border: none;
        border-bottom: 1px solid #e5e7eb;
        padding: 10px 12px;
        font-weight: 650;
    }

    QPushButton {
        background: #ffffff;
        color: #111827;
        border: 1px solid #d1d5db;
        border-radius: 8px;
        padding: 8px 14px;
        min-height: 28px;
    }

    QPushButton:hover {
        background: #f3f6fb;
        border-color: #c3cad7;
    }

    QPushButton:disabled {
        color: #9ca3af;
        background: #f3f4f6;
        border-color: #e5e7eb;
    }

    #btnAgregar, #btnAceptar {
        background: #0f6cbd;
        color: #ffffff;
        border: 1px solid #0f6cbd;
        font-weight: 650;
    }

    #btnAgregar:hover, #btnAceptar:hover {
        background: #115ea3;
        border-color: #115ea3;
    }

    #btnBorrar {
        color: #b91c1c;
        border-color: #fecaca;
        background: #fff7f7;
    }

    #btnBorrar:hover {
        background: #fee2e2;
        border-color: #fca5a5;
    }

    #btnCancelar {
        background: #ffffff;
        color: #111827;
    }

    QSplitter::handle {
        background: transparent;
        width: 12px;
    }
    """


__all__ = ["fluent_abm_stylesheet"]
