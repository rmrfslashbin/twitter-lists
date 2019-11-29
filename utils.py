import json


def jsonPrint(data):
    print(
        json.dumps(
            data,
            sort_keys=True,
            indent=2,
            separators=(',', ': ')
        )
    )
