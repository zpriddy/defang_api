from defang import defang, refang
from flask_restx import Resource
from flask_restx.reqparse import RequestParser
from urllib.parse import unquote

class ResponseObject(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.url = None
        self.output = None
        self.errors = list()

    def error(
        self, property=None, message=None, errors=None, exception=None, **kwargs
    ):
        if exception:
            self.errors.append({"exception": str(exception)})
        elif errors:
            self.errors.append(errors)
        else:
            self.errors.append({property: message})

    def get_args(self, parser: RequestParser):
        self.args = parser.parse_args()
        return True

    @property
    def response(self):
        response = {"output": self.output, "error": self.errors}
        self.errors = list()
        self.output = None
        self.data = None
        return response


def defang_post_json(payload: ResponseObject):
    """Defang the json payload for a post.

    Parameters
    ----------
    payload : ResponseObject
        The object containing the urls and arguments

    Returns
    -------
    dict: The payload response
    """
    if payload.args:
        is_list = True
        urls = payload.args["url"]
        if type(urls) is str:
            is_list = False
            urls = [urls]
        payload.output = defang(
            "\n".join(urls),
            all_dots=payload.args["dots"],
            colon=payload.args["colons"],
        ).splitlines()
        if not is_list:
            payload.output = payload.output[0]
    return payload.response


def defang_get(payload: ResponseObject):
    payload.output = defang(unquote(payload.args["url"]))
    return payload.response


def refang_post_json(payload: ResponseObject):
    is_list = True
    urls = payload.args["url"]
    if type(urls) is str:
        is_list = False
        urls = [urls]
    payload.output = refang("\n".join(urls),).splitlines()
    if not is_list:
        payload.output = payload.output[0]
    return payload.response


from base64 import b64decode, b64encode


def b64_decode(payload: ResponseObject):
    try:
        payload.output = b64decode(payload.data).decode()
    except Exception as e:
        payload.error(exception=e)
    return payload.response


def b64_encode(payload: ResponseObject):
    try:
        payload.output = b64encode(payload.data).decode()
    except Exception as e:
        payload.error(exception=e)
    return payload.response
