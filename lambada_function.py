import boto3
import json
from custom_encoder import CustomEncoder
import logging 
logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodbTableName = 'DentalV.C.'
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(dynamodbTableName)

getMethod = 'GET'
postMethod = 'POST'
patchMethod = 'PATCH'
deleteMethod = 'DELETE'
healthPath = '/health'
patientPath = '/patient'
patientsPath = '/patients'

def lambda_handler(event, contest):
    logger.info(event)
    httpMethod = event['httpMethod']
    path = event['path']
    if httpMethod == getMethod and path == healthPath:
        response = buildResponse(200)
    elif httpMethod == getMethod and path == patientPath:
        response = getpatient(event['queryStringParameters']['patientId'])
    elif httpMethod == getMethod and path == patientsPath:
        response = getpatients()
    elif httpMethod == postMethod and path == patientPath:
        response = savepatient(json.loads(event['body']))
    elif httpMethod == patchMethod and path == patientPath:
        requestBody = json.loads(event['body'])
        response = modifypatient(requestBody['patientId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == patientPath:
        requestBody = json.loads(event['body'])
        response = deletepatient(requestBody['patientId'])
    else:
        response = buildResponse(404, 'Not Found')

    return response


def getpatient(patientId):
    try:
        response = table.get_item(
            Key={
                'patientId': patientId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse(404, {'Message': 'patientId: %s not found' % patientId})
    except:
        logger.exception('Log it here for now')

def getpatients():
    try:
        response = table.scan()
        result = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            result.extend(response['Items'])

        body = {
            'patients': result
        }
        return buildResponse(200, body)
    except:
        logger.exception('Log it here for now')


def savepatient(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception('Log it here for now')

def modifypatient(patientId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key = {
                'patientId': patientId
            },
            UpdateExpression='set %s = :value' % updateKey,
            ExpressionAttributeValues={
                ':value': updateValue
            },
            ReturnValues='UPDATED_NEW'
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttribute': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Log it here for now')

def deletepatient(patientId):
    try:
        response = table.delete_item(
            Key = {
                'patientId': patientId
            },
            ReturnValues='ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200, body)
    except:
        logger.exception('Log it here for now')

def buildResponse(statusCode, body=None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'ContentType': 'application/json',
            'Access-Control-Allow-Origin': '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls=CustomEncoder)
    return response