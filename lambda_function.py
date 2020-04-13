import json
from functions import get_data
def lambda_handler(event, context):
    #extraemos los datos
    try:
        token=event['token']
        proy=event['project']
        month=event['month']
        year=event['year']
    except:
        token='0'
#Sino retorna 422 - UNPROCESABLE ENTITY
    if token=='0':
        return  {
            'statusCode': 422,
            'body': json.dumps('Check parameters')
        }
    elif token == 'VAcoG60gSbifBrrnKL_hUw':
        #ya tenemos los inputs y se lo enviamos
        data=get_data(proy, month, year)
        return  {
            'mensajes': data[0],
            'tiempo_total': data[1],
            'llamadas': data[2]
        }
    else:
        return {
            'statusCode': 403,
            'body': json.dumps('Invalid token')
        }
        

