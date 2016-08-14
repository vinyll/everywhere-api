

from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask.ext.cors import CORS


app = Flask(__name__)
CORS(app, resources=r'/*', allow_headers='Content-Type')
api = Api(app)
parser = reqparse.RequestParser()


ressources = {
    'block1': 'hey <b>bobby</b>',
    'block2': 'hoo'
}

content_parser = api.parser()
content_parser.add_argument('id', help='ID (name) of the content',
                            required=True)

edit_parser = content_parser.copy()
edit_parser.add_argument('body', help='JSON formatted data object',
                         location='form')


@api.route('/content/<string:id>/')
class ContentView(Resource):
    def get(self, id):
        return {
            'id': id,
            'body': ressources.get(id, '')
        }


@api.route('/content/')
@api.expect(edit_parser)
class ContentEdit(Resource):
    def post(self):
        args = edit_parser.parse_args()
        ressources[args['id']] = args['body']
        return {
            'success': True
        }


if __name__ == '__main__':
    app.run(debug=True)
