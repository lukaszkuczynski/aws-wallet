import boto3
from decimal import Decimal
import uuid
from datetime import datetime
s3_client = boto3.client('s3')
BUCKET_NAME = 'luk-thoughts'
import json
import certifi
from elasticsearch import Elasticsearch
import os

def last_record():
    s3 = boto3.resource('s3')

    obj = s3.Object(BUCKET_NAME, 'last')
    last_text = obj.get()['Body'].read().decode('utf-8')
    if last_text:
        last = json.loads(last_text)
        last['amount_after'] = Decimal(last['amount_after'])
        return last
    else:
        return {
            "amount_after": 100,
            "difference": -20,
            "description": "bread"
        }

def get_new_record(amount, description):
    last = last_record()
    after = last['amount_after'] - Decimal(amount)
    new_record = {
        "amount": str(amount),
        "amount_after": Decimal(str(after)),
        "description": description,
        "timestamp": datetime.strftime(datetime.now(), '%Y-%m-%d_%H:%M:%S')
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
    new_record['amount_after'] = str(new_record['amount_after'])
    jsoned = json.dumps(new_record)
    s3_client.put_object(
        Bucket = BUCKET_NAME,
        Key = 'last',
        Body = jsoned
    )
    index_es(jsoned)


def index_es(doc):
    host = os.environ['ES_HOST']
    es = Elasticsearch(hosts=[host], use_ssl=True, ca_certs=certifi.where())
    es.index('wallet', 'spending', doc)


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