from flask_restx import reqparse


def defang_json_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url",
        help="URL or comma separated array of URLs to defang",
        location="json",
        required=True,
        type=str,
    )
    parser.add_argument(
        "dots",
        help="Defang all dots?",
        default=False,
        type=bool,
        location="json",
    )
    parser.add_argument(
        "colons",
        help="Defang all dots?",
        default=False,
        type=bool,
        location="json",
    )
    return parser


def defang_get_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url", type=str, help="url is required for defanging.", required=True
    )
    return parser


def refang_get_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url", type=str, help="url is required for refanging.", required=True
    )
    return parser


def refang_json_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "url",
        help="URL or comma separated array of URLs to refang",
        location="json",
        required=True,
        type=str,
    )
    return parser


def b64_get_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "data", type=str, help="data to use as input", required=True
    )
    return parser


def b64_json_parser():
    parser = reqparse.RequestParser()
    parser.add_argument(
        "data",
        type=str,
        help="data to use as input",
        required=True,
        location="json",
    )
    return parser
