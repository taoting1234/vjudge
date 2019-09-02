import json

from flask_restful import reqparse


def json_data(data):
    return json.loads(data)


search_parser = reqparse.RequestParser()
search_parser.add_argument('page', type=int)
search_parser.add_argument('page_size', type=int)
search_parser.add_argument('order', type=json_data)
