import json, boto3, time
from datetime import datetime
from boto3.dynamodb.conditions import Key, Attr

def get_data(proy, month, year):
    #0° resultados iniciales
    mensajes=0
    tiempo=0
    llamadas=[]
    #1° generamos la fecha
    fecha=str(year)+'/'+str(month)
    #2° buscaremos todos los registros correspondientes al año y mes - BDAlertas
    dynamodb = boto3.resource('dynamodb',region_name = 'us-east-1')
    table = dynamodb.Table('DBAlertas')
    kce = Key('YEAR').eq(str(year)) & Key('FECHA').begins_with(fecha)
    response = table.query(IndexName='FECHAMES-index', KeyConditionExpression = kce, ScanIndexForward = False)
    items=response['Items']
    #3° recorremos para extraer datos
    for item in items:
        if item['ID_PROY']==str(proy):
            #recorremos los intentos
            for intento in item['INTENTOS']:
                if item['INTENTOS'][intento]["INICIO_LLAMADA"]:
                    #sumamos los mensajes
                    mensajes=mensajes+int(item['INTENTOS'][intento]['INTENTO'])
                    #almacenaremos datos de llamadas(nombre/num/inicio/fin)
                    llamada={}
                    inicio=item['INTENTOS'][intento]["INICIO_LLAMADA"]
                    fin=item['INTENTOS'][intento]["FIN_LLAMADA"]
                    duracion=get_duracion(inicio,fin)
                    #llenamos el dic llamada
                    llamada['numero']=item['INTENTOS'][intento]["NUMERO"]
                    llamada['alerta']=str(item['ID_ALERTA'])
                    llamada['inicio']=inicio
                    llamada['fin']=fin
                    llamada['duracion']=str(duracion)
                    #fin llenado
                    tiempo=tiempo + duracion
                    llamadas.append(llamada)
    data = [mensajes, tiempo ,llamadas ]
    return data
    
def get_duracion(inicio,fin):
    inicioF = inicio[11: 19]
    inicioT=datetime.strptime(inicioF, '%H:%M:%S')
    finF = fin[11: 19]
    finT=datetime.strptime(finF, '%H:%M:%S')
    duracion=finT-inicioT
    return duracion.seconds

