from src.process_request import run


def handler(event, context):
    response = run(event)
    return response
