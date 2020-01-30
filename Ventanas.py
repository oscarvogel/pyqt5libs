# coding=utf-8
import sys

from PyQt5.QtWidgets import QMessageBox, QApplication


def showAlert(titulo, mensaje):

    msg = CajaMensaje()
    msg.setIcon(QMessageBox.Information)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok)

    retval = msg.exec_()

    return retval

def showConfirmation(titulo, mensaje):
    msg = CajaMensaje()
    msg.setIcon(QMessageBox.Question)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    retval = msg.exec_()

    return retval

def showMsgAutoClose(titulo, mensaje):
    msg = CajaMensaje()
    msg.setIcon(QMessageBox.Question)
    msg.setText(mensaje)
    msg.setWindowTitle(titulo)
    msg.timeout = 3
    msg.autoClose = True
    msg.setStandardButtons(QMessageBox.Ok)
    retval = msg.exec_()

    return retval


def window():
   app = QApplication(sys.argv)
   # w = QWidget()
   # b = QPushButton(w)
   # b.setText("Show message!")
   #
   # b.move(50,50)
   # b.clicked.connect(showdialog)
   # w.setWindowTitle("PyQt Dialog demo")
   # w.show()
   showMsgAutoClose("Sistema", "Autoclose")
   sys.exit(app.exec_())

def showdialog():
    # retval = showConfirmation("Sistema", "Desea imprimir el presupuesto?")
    # if retval == QMessageBox.Ok:
    #     print("Valor de retorno {}".format(retval))
    showMsgAutoClose("Sistema", "Autoclose")

class CajaMensaje(QMessageBox):

    timeout = 0
    autoClose = False
    currentTime = 0

    def showEvent(self, QShowEvent):
        self.currentTime = 0
        if self.autoClose:
            self.startTimer(1000)

    def timerEvent(self, *args, **kwargs):
        self.currentTime += 1
        if self.currentTime >= self.timeout:
            self.done(0)
            self.close()


if __name__ == "__main__":
    window()
