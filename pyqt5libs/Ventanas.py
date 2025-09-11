# coding=utf-8
import sys

from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QPushButton, QInputDialog

NO = QMessageBox.Cancel
SI = QMessageBox.Ok

def showAlert(titulo, mensaje):

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()

    return retval

def showConfirmation(titulo, mensaje):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()

    return retval

def showTextInput(titulo, mensaje, texto_por_defecto=""):
    """
    Muestra un cuadro de diálogo para ingresar texto.
    
    Args:
        titulo (str): Título del diálogo.
        mensaje (str): Mensaje que se muestra al usuario.
        texto_por_defecto (str): Texto que aparece por defecto en el campo de entrada.
        
    Returns:
        tuple: (texto_ingresado, ok_presionado)
            - texto_ingresado (str): El texto que ingresó el usuario
            - ok_presionado (bool): True si se presionó OK, False si se canceló
    """
    texto, ok = QInputDialog.getText(None, titulo, mensaje, text=texto_por_defecto)
    return texto, ok

def window():
   app = QApplication(sys.argv)
   w = QWidget()
   b = QPushButton(w)
   b.setText("Show message!")

   b.move(50,50)
   b.clicked.connect(showdialog)
   w.setWindowTitle("PyQt Dialog demo")
   w.show()
   sys.exit(app.exec_())

def showdialog():
    retval = showConfirmation("Sistema", "Desea imprimir el presupuesto?")
    if retval == QMessageBox.Ok:
        print("Valor de retorno {}".format(retval))

def showCustomDialog(titulo, mensaje, botones=["Aceptar", "Cancelar"], por_defecto="Cancelar"):
    """
    Muestra un cuadro de diálogo con botones personalizados.

    Args:
        titulo (str): Título del diálogo.
        mensaje (str): Mensaje a mostrar.
        botones (list of str): Lista con los textos de los botones.
        por_defecto (str): Texto del botón que se considera "por defecto" si se cierra con X o Esc.

    Returns:
        str: El texto del botón presionado, o el valor de `por_defecto` si se cierra sin hacer clic.
    Ejemplo de uso:
        respuesta = showCustomDialog(
            titulo="Acción requerida",
            mensaje="¿Qué acción deseas realizar con este registro?",
            botones=["Dar de alta", "Guardar como borrador", "Cancelar"],
            por_defecto="Cancelar"
        )

        if respuesta == "Dar de alta":
            print("Dando de alta el registro...")
        elif respuesta == "Guardar como borrador":
            print("Guardando como borrador...")
        else:
            print("Operación cancelada.")
    """
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Question)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)

    # Diccionario para asociar botones creados con su texto
    botones_map = {}

    for texto in botones:
        btn = msg.addButton(texto, QMessageBox.ActionRole)  # ActionRole para botones neutrales
        botones_map[btn] = texto

    msg.exec()

    clicked_button = msg.clickedButton()
    if clicked_button is None:  # Se cerró con X o Esc
        return por_defecto

    return botones_map.get(clicked_button, por_defecto)

if __name__ == "__main__":
    window()