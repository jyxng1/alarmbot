import src


def handler(event, context):
    response = src.process_request.run(event)
    return response
