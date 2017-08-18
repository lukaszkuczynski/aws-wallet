def my_handler(event, context):
    print('Someone is invoking me!')
    message = 'Hello {} {}!'.format(event['first_name'],
                                    event['last_name'])
    return {
        'message' : message
    }