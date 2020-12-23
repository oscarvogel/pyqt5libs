# coding=utf-8

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 3, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTIBILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
# for more details.

#Utilidades varias necesarias en el sistema
import argparse
import calendar
import datetime
import decimal
import hashlib
import locale
import logging
import os
import random
import socket
import subprocess
import sys
import tempfile
import time
import traceback
import platform
from configparser import ConfigParser
from email.mime.text import MIMEText
from functools import wraps
from logging.handlers import RotatingFileHandler
from smtplib import SMTP

try:
    import win32print
except:
    pass
from PyQt5.QtCore import QSettings
from PyQt5.QtWidgets import QFileDialog, QInputDialog, QLineEdit
from os.path import join
from sys import argv
from pyqt5libs.libs.vistas.select_printer import Ui_FormPrinter
from PyQt5 import QtGui
from dateutil.relativedelta import relativedelta

try:
    import win32api
except:
    pass

from libs.pyqt5libs import Constantes, Ventanas

__author__ = "Jose Oscar Vogel <oscar@ferreteriaavenida.com.ar>"
__copyright__ = "Copyright (C) 2019 Steffen Hnos SRL"
__license__ = "GPL 3.0"
__version__ = "0.1"


#abro el archivo con el programa por defecto en windows
#tendria que ver como hacerlo en Linux
def AbrirArchivo(cArchivo=None):
    if cArchivo:
        if platform.system() == 'Darwin':  # macOS
            subprocess.call(('open', cArchivo))
        elif platform.system() == 'Windows':  # Windows
            os.startfile(cArchivo)
        else:  # linux variants
            subprocess.call(('xdg-open', cArchivo))

# leo el archivo de configuracion del sistema
# recibe la clave y el key a leer en caso de que tenga mas de una seccion el archivo
def LeerIni(clave=None, key=None, carpeta=''):
    analizador = argparse.ArgumentParser(description='Sistema.')
    analizador.add_argument("-i", "--inicio", default=os.getcwd(), help="Carpeta de Inicio de sistema.")
    analizador.add_argument("-a", "--archivo", default="fasa.ini", help="Archivo de Configuracion de sistema.")
    argumento = analizador.parse_args()
    retorno = ''
    Config = ConfigParser()
    archivoini = argumento.archivo
    carpeta = argumento.inicio
    # Config.read("fasa.ini")
    if carpeta:
        Config.read(join(carpeta, archivoini))
        # logging.debug("Archivo utilizado {}".format(join(carpeta, archivoini)))
    else:
        Config.read(archivoini)
        # logging.debug("Archivo utilizado {}".format(archivoini))

    try:
        if not key:
            key = 'param'
        retorno = Config.get(key, clave)
    except:
        # Ventanas.showAlert("Sistema", "No existe la seccion {}".format(clave))
        pass
    # print("archivo {} clave {} key {} carpeta {} valor {}".format(archivoini, clave, key, carpeta, retorno))
    return retorno

def GrabarIni(clave=None, key=None, valor=''):
    if not clave or not key:
        return
    Config = ConfigParser()
    Config.read('sistema.ini')
    cfgfile = open("sistema.ini",'w')
    if not Config.has_section(key):
        Config.add_section(key)
    Config.set(key, clave, valor)
    Config.write(cfgfile)
    cfgfile.close()

def ubicacion_sistema():
    cUbicacion = LeerIni("iniciosistema") or os.path.dirname(argv[0])

    return cUbicacion

def imagen(archivo):
    archivoImg = ubicacion_sistema() + join("imagenes", archivo)
    if os.path.exists(archivoImg):
        return archivoImg
    else:
        return ""

def icono_sistema():

    cIcono = QtGui.QIcon(imagen(LeerIni("logo")))
    return cIcono

def validar_cuit(cuit):
    # validaciones minimas
    if len(cuit) != 13 or cuit[2] != "-" or cuit[11] != "-":
        return False

    base = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]

    cuit = cuit.replace("-", "") # remuevo las barras

    # calculo el digito verificador:
    aux = 0
    for i in range(10):
        aux += int(cuit[i])* base[i]

    aux = 11 - (aux - (int(aux / 11)* 11))

    if aux == 11:
        aux = 0
    if aux == 10:
        aux = 9

    return aux == int(cuit[10])

def FechaMysql(fecha=None):

    if isinstance(fecha, str):
        retorno = fecha
    else:
        if not fecha:
            fecha = datetime.datetime.today()
        retorno = fecha.strftime('%Y%m%d')

    return retorno

def HoraMysql(hora=None):

    if not hora:
        hora = datetime.datetime.now()

    retorno = hora.strftime('%H:%M:%S')

    return retorno

def check_password(hashed_password, user_password):
    password, salt = hashed_password.split(':')
    return hashlib.sha256(salt.encode() + user_password.encode()).hexdigest()

# def encriptar(password):
#     key = Fernet.generate_key()
#     cipher_suite = Fernet(key)
#     cipher_text = cipher_suite.encrypt(password)
#     return cipher_text, key
#
# def desencriptar(encrypted_data, key):
#     cipher_suite = Fernet(key)
#     plain_text = cipher_suite.decrypt(encrypted_data)
#     return plain_text

def GrabaConf(clave=None, valor=None, sistema=None):
    if not sistema:
        sistema = Constantes.SISTEMA
    settings = QSettings(Constantes.EMPRESA, sistema)
    if clave:
        if isinstance(clave, (int, float, decimal.Decimal)):
            clave = str(clave)
        settings.setValue(clave, valor)

def LeerConf(clave=None, sistema=None):
    if not sistema:
        sistema = Constantes.SISTEMA
    settings = QSettings(Constantes.EMPRESA, sistema)
    if clave:
        cValorRetorno = settings.value(clave)
    else:
        cValorRetorno = None

    return cValorRetorno

def BorrarConf(clave=None, sistema=None):
    if not sistema:
        sistema = Constantes.SISTEMA

    settings = QSettings(Constantes.EMPRESA, sistema)
    if clave:
        settings.remove(clave)
    else:
        settings.clear()

#necesario porque en mysql tengo definido el campo boolean como bit
def EsVerdadero(valor):

    return valor == b'\01'


def inicializar_y_capturar_excepciones(func):
    "Decorador para inicializar y capturar errores"
    @wraps(func)
    def capturar_errores_wrapper(self, *args, **kwargs):
        try:
            # inicializo (limpio variables)
            self.Traceback = self.Excepcion = ""
            self.HuboError = False
            return func(self, *args, **kwargs)
        except Exception as e:
            ex = traceback.format_exception( sys.exc_info()[0], sys.exc_info()[1], sys.exc_info()[2])
            self.HuboError = True
            self.Traceback = ''.join(ex)
            self.Excepcion = traceback.format_exception_only( sys.exc_info()[0], sys.exc_info()[1])[0]
            logging.debug(self.Traceback)
            # file = open("errors.log")
            # file.write(self.Traceback)
            # file.close()
            Ventanas.showAlert("Error", "Se ha producido un error \n{}".format(self.Excepcion))
            try:
                remitente = 'fe@servinlgsm.com.ar'
                destinatario = 'fe@servinlgsm.com.ar'
                mensaje = "{} {} Enviado desde mi Software de Gestion desarrollado por http://www.servinlgsm.com.ar".format(
                    self.Traceback, self.Excepcion
                )
                motivo = "Se envia informe de errores de {}".format(LeerIni(clave='nombre_sistema'))
                envia_correo(from_address=remitente, to_address=destinatario,
                             message=mensaje, subject = motivo, password_email = Constantes.CLAVE_SMTP)
            except:
                pass
            if self.LanzarExcepciones:
                raise
        finally:
            pass
    return capturar_errores_wrapper

def getFileName(filename='pdf', base=False):

    tf = tempfile.NamedTemporaryFile(prefix=filename, mode='w+b')
    if base:
        return os.path.basename(tf.name)
    return tf.name


def FormatoFecha(fecha=datetime.datetime.today(), formato='largo'):

    retorno = ''
    if isinstance(fecha, (str)):
        retorno = fecha
    else:
        if formato == 'largo':
            retorno = datetime.datetime.strftime(fecha,'%d %b %Y')
        elif formato == 'corto':
            retorno = datetime.datetime.strftime(fecha, '%d-%b')
        elif formato == 'dma':
            retorno = datetime.datetime.strftime(fecha, '%d/%m/%Y')

    return retorno

def DeCodifica(dato):
    return "{}".format(bytearray(dato, 'latin-1', errors='ignore').decode('utf-8','ignore'))


def saveFileDialog(form=None, files=None, title="Guardar", filename="excel/archivo.xlsx"):
    if not files:
        files = "Todos los archivos (*);;Archivos de texto (*.txt)"
    options = QFileDialog.Options()
    fileName, _ = QFileDialog.getSaveFileName(form, title, filename,
                                              files, options=options)
    return fileName

def openFileNameDialog(form=None, files=None, title='Abrir', filename=''):
    options = QFileDialog.Options()
    # options |= QFileDialog.DontUseNativeDialog
    fileName, _ = QFileDialog.getOpenFileName(form, title, filename,
                                              files, options=options)
    if fileName:
        return fileName
    else:
        return ''

def InicioMes(dFecha=None):
    if not dFecha:
        dFecha = datetime.date.today()

    return dFecha.replace(day=1)

def FinMes(hFecha=None):
    if not hFecha:
        hFecha = datetime.date.today()

    return hFecha.replace(day = calendar.monthrange(hFecha.year, hFecha.month)[1])

def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    # handler = logging.FileHandler(os.path.join(output_dir, "all.log"), "a")
    # handler.setLevel(logging.DEBUG)
    if LeerIni('debug') == 'S':
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(os.path.join(output_dir, "all.log"), maxBytes=2000)
        logger.addHandler(handler)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s", datefmt='%m/%d/%Y %I:%M:%S %p')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

def getText(vista, titulo='', etiqueta=''):
    text, okPressed = QInputDialog.getText(vista, titulo, etiqueta, QLineEdit.Normal, "")
    if okPressed and text != '':
        return text
    else:
        return ''

def GuardarArchivo(caption="Guardar archivo", directory="", filter="", filename=""):

    cArchivo = QFileDialog.getSaveFileName(caption=caption,
                                           directory=join(directory, filename),
                                           filter=filter)
    return cArchivo[0] if cArchivo else ''

def Normaliza(valor):
    valor = DeCodifica(valor)
    return valor.replace('Ñ','N').replace('ñ','n').replace('º','')

def HayInternet():
    retorno = True
    try:
        socket.gethostbyname('google.com')
        c = socket.create_connection(('google.com', 80), 1)
        c.close()
    except socket.gaierror:
        print("DNS error")
        retorno = False
    except socket.error:
        print("Connection error")
        retorno = False

    return retorno

def envia_correo(from_address = '', to_address = '', message = '', subject = '', password_email = '', to_cc=''):
    smtp_email = 'mail.servinlgsm.com.ar'
    mime_message = MIMEText(message)
    mime_message["From"] = from_address
    mime_message["To"] = to_address
    mime_message["Subject"] = subject
    if to_cc:
        mime_message["Cc"] = to_cc
    smtp = SMTP(smtp_email, 587)
    smtp.ehlo()

    smtp.login(from_address, password_email)
    smtp.sendmail(from_address, [to_address, to_cc], mime_message.as_string())
    smtp.quit()

def uniqueid():
    seed = random.getrandbits(32)
    while True:
       yield seed
       seed += 1

#==============================================================================
def getFileProperties(fname):
#==============================================================================
    """
    Read all properties of the given file return them as a dictionary.
    """
    propNames = ('Comments', 'InternalName', 'ProductName',
        'CompanyName', 'LegalCopyright', 'ProductVersion',
        'FileDescription', 'LegalTrademarks', 'PrivateBuild',
        'FileVersion', 'OriginalFilename', 'SpecialBuild')

    props = {'FixedFileInfo': None, 'StringFileInfo': None, 'FileVersion': None}

    try:
        # backslash as parm returns dictionary of numeric info corresponding to VS_FIXEDFILEINFO struc
        fixedInfo = win32api.GetFileVersionInfo(fname, '\\')
        props['FixedFileInfo'] = fixedInfo
        props['FileVersion'] = "%d.%d.%d.%d" % (fixedInfo['FileVersionMS'] / 65536,
                fixedInfo['FileVersionMS'] % 65536, fixedInfo['FileVersionLS'] / 65536,
                fixedInfo['FileVersionLS'] % 65536)

        # \VarFileInfo\Translation returns list of available (language, codepage)
        # pairs that can be used to retreive string info. We are using only the first pair.
        lang, codepage = win32api.GetFileVersionInfo(fname, '\\VarFileInfo\\Translation')[0]

        # any other must be of the form \StringfileInfo\%04X%04X\parm_name, middle
        # two are language/codepage pair returned from above

        strInfo = {}
        for propName in propNames:
            strInfoPath = u'\\StringFileInfo\\%04X%04X\\%s' % (lang, codepage, propName)
            ## print str_info
            strInfo[propName] = win32api.GetFileVersionInfo(fname, strInfoPath)

        props['StringFileInfo'] = strInfo
    except:
        pass

    return props

def gomonth(fecha=datetime.datetime.today(), month=1):
    fecharetorno = fecha + relativedelta(months=month)
    return fecharetorno

def goday(fecha=datetime.datetime.today(), format=None, days=0):
    fecharetorno = None
    if format:
        if format == "Ymd":
            fecha = datetime.date(year=int(fecha[:4]),
                                  month=int(fecha[4:6]),
                                  day=int(fecha[-2:]))
    if isinstance(fecha, int):
        if fecha > 0:
            fecharetorno = datetime.date.today() + datetime.timedelta(days=fecha)
        else:
            fecharetorno = datetime.date.today() - datetime.timedelta(days=abs(fecha))
    elif days != 0:
        fecharetorno = datetime.date.today() + datetime.timedelta(days=days)
    else:
        fecharetorno = fecha
    return fecharetorno

def periodo_anterior(periodo=''):
    fecha = datetime.datetime(int(periodo[:4]), int(periodo[4:]), 1, 0, 0, 0)
    retorno = FechaMysql(gomonth(fecha, -1))[:6]

    return retorno


def periodo_siguiente(periodo=''):
    fecha = datetime.datetime(int(periodo[:4]), int(periodo[4:]), 1, 0, 0, 0)
    retorno = FechaMysql(gomonth(fecha, 1))[:6]

    return retorno

def MesIdentificador(dFecha=datetime.datetime.now().date(), formato='largo', periodo=None):
    if periodo:
        dFecha = PeriodoAFecha(periodo)
    MESES = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre',
    ]
    retorno = ''
    if formato == 'largo':
        retorno = '{}/{}'.format(MESES[dFecha.month - 1], dFecha.year)
    elif formato == 'corto':
        retorno = '{}/{}'.format(MESES[dFecha.month - 1][:3], dFecha.year)
    return retorno

def PeriodoAFecha(periodo: str = ''):
    fecha = datetime.date(int(periodo[:4]), int(periodo[4:]), 1)

    return fecha


class WinPrinters(object):
    cDefault = ''

    def __init__(self):
        self.cDefault = win32print.GetDefaultPrinterW()

    def SetPrinter(self, cPrinter=''):
        try:
            win32print.SetDefaultPrinterW(cPrinter)
        except Exception as e:
            # printer = QPrinter()
            #
            # dialog = QPrintDialog(printer)
            # dialog.exec_()
            _ventana = Ui_FormPrinter()
            _ventana.exec_()
            if _ventana.cPrinterSelected != '':
                win32print.SetDefaultPrinterW(_ventana.cPrinterSelected)
            else:
                Ventanas.showAlert("Sistema", "No se encontro la impresora {} en la maquina y se imprimira en {}"
                                   .format(cPrinter, win32print.GetDefaultPrinterW()))
                win32print.SetDefaultPrinterW(win32print.GetDefaultPrinterW())

    def GetDefaultPrinter(self):
        return win32print.GetDefaultPrinterW()

    def SendPDF(self, cPDFName, imprime=False):
        if os.path.isfile(cPDFName):
            try:
                if LeerConf('usuario') == 'OSCAR':
                    if not imprime:
                        win32api.ShellExecute(0, "open", cPDFName, None, ".", 0)
                    else:
                        os.startfile(cPDFName, "print")
                else:
                    # win32api.ShellExecute(
                    #    0,
                    #    "print",
                    #    cPDFName,
                    #    '/d:"%s"' % win32print.GetDefaultPrinter(),
                    #    ".",
                    #    0
                    # )
                    os.startfile(cPDFName, "print")
                # win32api.ShellExecute(0, "print", cPDFName, None, ".", 0)
                time.sleep(5)
                # os.system("taskill /im AcroRd32.exe /f")
            except Exception as e:
                win32api.ShellExecute(0, "open", cPDFName, None, ".", 0)
                Ventanas.showAlert("Sistema", "Para poder imprimir es necesario "
                                              "instalar un visualizador de PDF por defecto")
        else:
            Ventanas.showAlert("Sistema", "No existe el archivo para la impresion")

"""
Para los archivo de texto que se generan deben tener ceros a la izquierda sin coma ni punto decimal
"""
def NumeroTXT(valor=0, largo=12, decimales=2):
    # return str(abs(round(valor, decimales))).replace(',','').replace('.','').zfill(largo)
    return str((round(valor * 10 ** decimales))).replace(',', '').replace('.', '').zfill(largo)


def DiaSemana(fecha=datetime.datetime.now().date()):
    locale.setlocale(locale.LC_ALL, "es")
    retorno = fecha.strftime('%A')

    return retorno
