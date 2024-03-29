from flask import jsonify


def response_json(ok=True, data=None, message=None, error=None):
    res = {
        'Ok': ok
    }
    if data is not None:
        res['Data'] = data

    if message:
        res['Message'] = message

    if error:
        res['Error'] = error

    return jsonify(res)


def to_int(val):
    return int(val) if val is not None else val
