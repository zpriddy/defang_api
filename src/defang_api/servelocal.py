"""
Serves a local Flask application for GLaDOS bots/plugins
"""
# temp fix for now (https://github.com/jarus/flask-testing/issues/143)
import werkzeug

werkzeug.cached_property = werkzeug.utils.cached_property

from flask import Flask, request, make_response
from defang import refang
from flask_restx import Api, fields
from urllib.parse import unquote
import click

from .helpers.helpers import (
    ResponseObject,
    defang_post_json,
    defang_get,
    refang_post_json,
    b64_decode,
    b64_encode,
)
from .helpers.parsers import (
    defang_json_parser,
    defang_get_parser,
    refang_get_parser,
    refang_json_parser,
    b64_get_parser,
    b64_json_parser,
)

app = Flask(__name__)
app.debug = True
api = Api(
    app,
    version="1.0",
    title="Defang API",
    description="A Defang API",
    prefix="/",
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


@ds.route("/defang")
class DefangPostResource(ResponseObject):
    """Defanging operations"""

    parser = defang_get_parser()
    parser_json = defang_json_parser()
    defang_json_resource = api.model(
        "DefangRequest",
        {
            "url": fields.List(
                fields.String(min_length=5),
                description="URL or comma separated array of URLs to defang",
                example=["https://example.com", "https://foo.bar"],
            ),
            "colons": fields.Boolean(
                default=False, description="Defang all colons?"
            ),
            "dots": fields.Boolean(
                default=False, description="Defang all dots?"
            ),
        },
    )

    @ds.expect(parser)
    @ds.doc(id="defang_url_get")
    def get(self):
        """simple defang of a string"""
        self.get_args(self.parser)
        self.args["url"] = request.query_string.decode()[4:]
        return defang_get(self)

    @ds.expect(defang_json_resource)
    @ds.doc(id="defang_url_json")
    @ds.doc(body=defang_json_resource)
    def post(self):
        """json post"""
        # This is to verify the args
        self.get_args(self.parser_json)
        # Using the more raw data as input
        self.args = api.payload
        return defang_post_json(self)


@ds.route("/refang")
class RefangPostResource(ResponseObject):
    """Defanging operations"""

    parser = refang_get_parser()
    parser_json = refang_json_parser()
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

    @ds.expect(parser)
    @ds.doc(id="refang_url_get")
    def get(self):
        """simple refang of a string"""
        if self.get_args(self.parser):
            url = request.query_string.decode()[4:]
            self.output = refang(url)
        return self.response

    @ds.expect(resource_fields)
    @ds.doc(id="refang_url_json")
    @ds.doc(body=resource_fields)
    def post(self):
        """json post"""
        # This is to verify the args
        self.get_args(self.parser_json)
        # Using the more raw data as input
        self.args = api.payload
        if self.args:
            refang_post_json(self)


@ds.route("/b64e")
class Base64encode(ResponseObject):
    """Encode a string in Base64"""

    parser = b64_get_parser()
    json_parser = b64_json_parser()

    @ds.expect(parser)
    @ds.doc(id="b64_encode_query")
    def get(self):
        """Encode data with base 64"""
        self.get_args(self.parser)
        self.data = unquote(request.query_string.decode()[5:]).encode()
        return b64_encode(self)

    @ds.expect(json_parser)
    @ds.doc(id="b64_encode_json")
    def post(self):
        """Encode data with base 64"""
        self.get_args(self.json_parser)
        self.data = self.args.get("data", "").encode()
        return b64_encode(self)


@ds.route("/b64d")
class Base64decode(ResponseObject):
    """Decode a string in Base64

    Decode base64 encoded string
    """

    parser = b64_get_parser()
    json_parser = b64_json_parser()

    @ds.expect(parser)
    @ds.doc(id="b64_decode_query")
    def get(self):
        """Decode base 64 encoded data"""
        self.get_args(self.parser)
        self.data = unquote(request.query_string.decode()[5:])
        return b64_decode(self)

    @ds.expect(json_parser)
    @ds.doc(id="b64_decode_json")
    def post(self):
        """Decode base 64 encoded data"""
        self.get_args(self.json_parser)
        self.data = self.args.get("data", "").encode()
        return b64_decode(self)


@click.command()
@click.option("--host", default="localhost", help="Flask Host")
@click.option("--port", default=5000, help="Flask Port")
def run(host, port):

    app.run(host=host, port=port)


if __name__ == "__main__":
    run()
