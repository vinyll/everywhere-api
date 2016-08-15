from os import environ

from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask.ext.cors import CORS

import storage


app = Flask(__name__)
CORS(app, resources=r'/*', allow_headers='Content-Type')
api = Api(app)

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('key', help='the owner\'s key', location='form')
edit_parser.add_argument('body', help='the value of the content',
                         location='form')


@api.route('/user/<string:name>/')
class UserView(Resource):
    def post(self, name):
        try:
            return storage.create_owner(name)
        except storage.DuplicateException:
            return {
                'error': 'A user with that name already exists'
            }, 409


@api.route('/content/<string:user>/<string:name>/')
class ContentView(Resource):
    def get(self, user, name):
        owner = storage.get_owner(user)
        content = storage.get_content(name=name, owner=owner)
        if content:
            return {
                'name': content['name'],
                'body': content['value']
            }
        else:
            return {'name': name, 'body': ''}, 404



@api.route('/content/<string:user>/<string:name>/')
class ContentEdit(Resource):
    def post(self, user, name):
        args = edit_parser.parse_args()
        owner = storage.get_owner(name=user)
        if not owner or owner['key'] != args['key']:
            return ({'error': 'Invalid user or key'}, 401)
        content = storage.crupdate_content(name, args['body'], owner)
        return {
            'name': content['name'],
            'body': content['value']
        }


if __name__ == '__main__':
    app.run(host='0.0.0.0',
            port=environ.get('PORT', 80),
            debug=environ.get('DEBUG', False))
