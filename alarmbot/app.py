from src.process_request import run


def handler(event, context):
    print(event)
    response = run(event)
    return response
