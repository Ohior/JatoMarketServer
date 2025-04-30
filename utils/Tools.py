import uuid


def generateUUid():
    return str(uuid.uuid4().hex)
