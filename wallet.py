def last_record():
    return {
        "amount_after": 100,
        "difference": -20,
        "description": "bread"
    }

def get_new_record(amount, description):
    last = last_record()
    new_record = {
        "amount_after": last['amount_after'] - amount,
        "description": description
    }
    return new_record


def save(new_record):
    print("Save not yet implemented")


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