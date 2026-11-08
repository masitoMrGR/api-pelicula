import boto3
import uuid
import os
import json

def lambda_handler(event, context):
    try:
        # Entrada (json)
        tenant_id = event['body']['tenant_id']
        pelicula_datos = event['body']['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # Log INFO
        log = {
            'tipo': 'INFO',
            'log_datos': {
                'mensaje': 'Pelicula creada correctamente',
                'pelicula': pelicula
            }
        }
        print(json.dumps(log))

        # Salida (json)
        return {
            'statusCode': 200,
            'pelicula': pelicula,
            'response': response
        }

    except Exception as e:
        # Log ERROR
        log = {
            'tipo': 'ERROR',
            'log_datos': {
                'mensaje': 'Error al crear pelicula',
                'error': str(e),
                'tipo_error': type(e).__name__,
                'entrada': event.get('body')
            }
        }
        print(json.dumps(log, default=str))

        return {
            'statusCode': 500,
            'error': str(e)
        }
