"""
Serves a local Flask application for GLaDOS bots/plugins
"""
# temp fix for now (https://github.com/jarus/flask-testing/issues/143)
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from flask_restx.reqparse import RequestParser
from flask import Flask, request, make_response
from defang import defang, refang
from flask_restx import Api, Resource, fields

import click
from flask_restx import reqparse
from base64 import b64decode, b64encode


app = Flask(__name__)
app.debug = True
api = Api(
    app, version="1.0", title="Defang API", description="A Defang API", prefix="/api",
)


def output_text(data, *args, **kwargs):
    if type(data.get("output")) is list:
        return make_response(",".join(data["output"]))
    if type(data.get("output")) is str:
        return make_response(data.get("output"))
    return make_response(data)


def output_json(data, *args, **kwargs):
    return make_response(data)


api.representations["text/plain"] = output_text
api.representations["application/json"] = output_json

ds = api.namespace("api", description="Defang API Server")


class ResponseObject(Resource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = None
        self.url = None
        self.output = None
        self.errors = list()

    def error(self, property=None, message=None, errors=None, exception=None, **kwargs):
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


def defang_get(payload: ResponseObject):
    payload.output = defang(payload.args["url"])
    return payload.response


@ds.route("/defang")
class DefangPostResource(ResponseObject):
    """Defanging operations"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "url", type=str, help="url is required for defanging.", required=True
    )

    @ds.expect(parser)
    @ds.doc(id="defang_url_get")
    def get(self):
        """simple defang of a string"""
        self.get_args(self.parser)
        self.args["url"] = request.query_string.decode()[4:]
        return defang_get(self)

    parser_json = api.parser()
    parser_json.add_argument(
        "url",
        help="URL or comma separated array of URLs to defang",
        location="json",
        required=True,
        type=str,
    )
    parser_json.add_argument(
        "dots", help="Defang all dots?", default=False, type=bool, location="json",
    )
    parser_json.add_argument(
        "colons", help="Defang all dots?", default=False, type=bool, location="json",
    )

    resource_fields = api.model(
        "DefangRequest",
        {
            "url": fields.List(
                fields.String(min_length=5),
                description="URL or comma separated array of URLs to defang",
                example=["https://example.com", "https://foo.bar"],
            ),
            "colons": fields.Boolean(default=False, description="Defang all colons?"),
            "dots": fields.Boolean(default=False, description="Defang all dots?"),
        },
    )

    @ds.expect(resource_fields)
    @ds.doc(id="defang_url_json")
    @ds.doc(body=resource_fields)
    def post(self):
        """json post"""
        # This is to verify the args
        self.get_args(self.parser_json)
        # Using the more raw data as input
        self.args = api.payload
        return defang_post_json(self)


def defang_post_json(pyaload: ResponseObject):
    if pyaload.args:
        is_list = True
        urls = pyaload.args["url"]
        if type(urls) is str:
            is_list = False
            urls = [urls]
        pyaload.output = defang(
            "\n".join(urls),
            all_dots=pyaload.args["dots"],
            colon=pyaload.args["colons"],
        ).splitlines()
        if not is_list:
            pyaload.output = pyaload.output[0]
    return pyaload.response


@ds.route("/refang")
class RefangPostResource(ResponseObject):
    """Defanging operations"""

    parser = reqparse.RequestParser()
    parser.add_argument(
        "url", type=str, help="url is required for refanging.", required=True
    )

    @ds.expect(parser)
    @ds.doc(id="refang_url_get")
    def get(self):
        """simple refang of a string"""
        if self.get_args(self.parser):
            url = request.query_string.decode()[4:]
            self.output = refang(url)
        return self.response

    parser_json = api.parser()
    parser_json.add_argument(
        "url",
        help="URL or comma separated array of URLs to refang",
        location="json",
        required=True,
        type=str,
    )

    resource_fields = api.model(
        "RefangRequest",
        {
            "url": fields.List(
                fields.String(min_length=5),
                description="URL or comma separated array of URLs to refang",
                example=["hXXps[:]//example[.]com", "hXXps[:]//foo[.]bar"],
            )
        },
    )

    @ds.expect(resource_fields)
    @ds.doc(id="refang_url_json")
    @ds.doc(body=resource_fields)
    def post(self):
        """json post"""
        # This is to verify the args
        self.get_args(self.parser_json)
        # Using the more raw data as input
        self.args = api.payload
        print(self.args)
        if self.args:
            is_list = True
            urls = self.args["url"]
            if type(urls) is str:
                is_list = False
                urls = [urls]
            self.output = refang("\n".join(urls),).splitlines()
            if not is_list:
                self.output = self.output[0]
        return self.response


@ds.route("/b64e")
class Base64encode(ResponseObject):
    """Encode a string in Base64"""

    parser = reqparse.RequestParser()
    parser.add_argument("data", type=str, help="data to use as input", required=True)

    @ds.expect(parser)
    @ds.doc(id="b64_encode_query")
    def get(self):
        """Encode data with base 64"""
        if self.get_args(self.parser):
            try:
                data = request.query_string.decode()[5:]
                self.data = data.encode()
                self.output = b64encode(self.data).decode()
            except Exception as e:
                self.error(exception=e)
        return self.response

    json_parser = reqparse.RequestParser()
    json_parser.add_argument(
        "data", type=str, help="data to use as input", required=True, location="json",
    )

    @ds.expect(json_parser)
    @ds.doc(id="b64_encode_json")
    def post(self):
        """Encode data with base 64"""
        self.get_args(self.json_parser)
        try:
            self.data = self.args.get("data", "").encode()
            self.output = b64encode(self.data).decode()
        except Exception as e:
            self.error(exception=e)
        return self.response


@ds.route("/b64d")
class Base64decode(ResponseObject):
    """Decode a string in Base64

    Decode base64 encoded string
    """

    parser = reqparse.RequestParser()
    parser.add_argument("data", type=str, help="data to use as input", required=True)

    @ds.expect(parser)
    @ds.doc(id="b64_decode_query")
    def get(self):
        """Decode base 64 encoded data"""
        if self.get_args(self.parser):
            try:
                data = request.query_string.decode()[5:]
                self.output = b64decode(data).decode()
            except Exception as e:
                self.error(exception=e)
        return self.response

    json_parser = reqparse.RequestParser()
    json_parser.add_argument(
        "data", type=str, help="data to use as input", required=True, location="json",
    )

    @ds.expect(json_parser)
    @ds.doc(id="b64_decode_json")
    def post(self):
        """Decode base 64 encoded data"""
        self.get_args(self.json_parser)
        try:
            self.data = self.args.get("data", "").encode()
            self.output = b64decode(self.data).decode()
        except Exception as e:
            self.error(exception=e)
        return self.response


@click.command()
@click.option("--host", default="localhost", help="Flask Host")
@click.option("--port", default=5000, help="Flask Port")
def run(host, port):

    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
