import json
import boto3
from datetime import datetime

#That's the lambda handler, you can not modify this method
# the parameters from JSON body can be accessed like rsuId = event['rsuId']
def lambda_handler(event, context):
    # Instanciating connection objects with DynamoDB using boto3 dependency
    dynamodb = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    
    # Getting the table the table RsuAccidentSignals object
    tableRsuAccidentSignals = dynamodb.Table('RsuAccidentSignals')
    
    # Getting the current datetime and transforming it to string in the format bellow
    timeStamp = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    rsuId = event['rsuId']
    accidentVehicleId = event['accidentVehicleId']
    accidentLongitude = event['accidentLongitude']
    accidentLatitude = event['accidentLatitude']
    
    # Putting a try/catch to log to user when some error occurs
    try:
        
        tableRsuAccidentSignals.put_item(
           Item={
                'timeStamp': timeStamp,
                'rsuId': rsuId,
                'accidentVehicleId': accidentVehicleId,
                'accidentLongitude': accidentLongitude,
                'accidentLatitude': accidentLatitude
            }
        )
        
        return {
            'statusCode': 200,
            'body': json.dumps('Succesfully inserted Accident Signal!')
        }
    except:
        print('Closing lambda function')
        return {
                'statusCode': 400,
                'body': json.dumps('Error saving the Accident Signal')
        }