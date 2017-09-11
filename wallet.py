import boto3
from decimal import Decimal
import uuid



def last_record():
    return {
        "amount_after": 100,
        "difference": -20,
        "description": "bread"
    }

def get_new_record(amount, description):
    last = last_record()
    after = last['amount_after'] - amount
    new_record = {
        "amount_after": Decimal(str(after)),
        "description": description
    }
    return new_record


def save(new_record):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('operation')
    new_record['OperationId'] = str(uuid.uuid4())[0:6]
    item = new_record
    table.put_item(
        Item = item
    )


def my_handler(event, context):
    new_record = {}
    if event['op_type'] == 'spending':
        print("received new spending")
        last = last_record()
        print("last time we had: %s", last)
        new_record = get_new_record(event['amount'], event['description'])
        print("now we will write new record: %s" % new_record)
        save(new_record)

    else:
        raise Exception("Operation Type %s not known " % event['op_type'])


    return new_record