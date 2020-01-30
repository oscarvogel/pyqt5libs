ACTIVO = b'\01'

SISTEMA = "CONTABLE"
EMPRESA = "Steffen Hnos"
IDSISTEMA = 8

CLIENTE_CF = 1

CHEQUE_DEVUELTO = 6

CONSUMIDOR_FINAL = 5
RESPONSABLE_INSCRIPTO = 1

LOGO = "imagenes/logo.png"

DECIMALES = 2

FACTURA_A = '1'
FACTURA_B = '6'
FACTURA_C = '11'

NOTA_CREDITO_A = '3'
NOTA_CREDITO_B = '8'
NOTA_CREDITO_C = '13'

SERVER_SMTP = 'mail.ferreteriaavenida.com.ar'
PUERTO_SMTP = 587
USUARIO_SMTP = 'info@ferreteriaavenida.com.ar'
CLAVE_SMTP = 'Fasa0298'

TIPO_MOVIMIENTOS = {
    'I':'Ingreso', 'E':'Egreso'
}

CLIENTESCUIT = [1, 2, 3, 4, 6, 9, 11]

CHOFER_SINDETALLE = 38
TRANSPORTE_SINDETALLE = 21

CAJAPORDEFECTO = 1

COEFICIENTE_IVA_21 = 1.21


LOCALIDAD_ORIGEN = 1

TIPO_COMP = {
    'F':'FAC',
    'C':'CRE',
    'D':'DEB'
}

REG_IVA = {
    'F':'CONSUMIDOR FINAL',
    'X':'EXENTO',
    'C':'RESPONSABLE INSCRIPTO',
    'M':'RESPONSABLE MONOTRIBUTO',
    ' ':'SIN CATEGORIZACION'
}

ID_EMPRESA_FASA = 1
ID_EMPRESA_STEFFEN = 2
ID_EMPRESA_TRANSPORTE = 3

REMCDESCUENTO = 'REMCDES'

DESCUENTO_BI_10 = {
    2019:7003.68
}


CTAS_ACTIVO = '1'
CTAS_PASIVO = '2'
CTAS_PN = '3'
CTAS_RES_POS = '4'
CTAS_RES_NEG = '5'

ALICUOTA_AFIP = {0:"0003", 10.5:"0004", 21:"0005", 27:"0006", 2.5:"0009"}

UBICACIONIMPREM = {
    '01':{'x':10,'y':5},
    '02':{'x':100,'y':5},
    '03': {'x': 10, 'y': 30},
    '04': {'x': 100, 'y': 30},
    '05': {'x': 10, 'y': 60},
    '06': {'x': 100, 'y': 60},
    '07': {'x': 10, 'y': 90},
    '99': {'x': 100, 'y': 90},
}

UBICACIONIMPFAC = {
    '01':{'x':10,'y':5},
    '02':{'x':10,'y':50},
    '03': {'x': 10, 'y': 80},
    '04': {'x': 10, 'y': 130},
    '05': {'x': 10, 'y': 160},
    '06': {'x': 10, 'y': 190},
    '07': {'x': 10, 'y': 230},
    '99': {'x': 10, 'y': 260},
}