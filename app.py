from os import environ

from flask import Flask
from flask_restplus import Resource, Api, reqparse
from flask.ext.cors import CORS

import storage


app = Flask(__name__)
CORS(app, resources=r'/*', allow_headers='Content-Type')

api = Api(app, version='1.0', title='Everywhere API',
    description='Everywhere content management API',
)

user_ns = api.namespace('users', description='Users operations')
content_ns = api.namespace('contents', description='Contents operations')

edit_parser = reqparse.RequestParser()
edit_parser.add_argument('key', help='the owner\'s key', location='form')
edit_parser.add_argument('body', help='the value of the content',
                         location='form')


@user_ns.route('/user/<string:name>/')
class UserView(Resource):
    @user_ns.doc('create new user')
    def post(self, name):
        try:
            return storage.create_owner(name)
        except storage.DuplicateException:
            return {
                'error': 'A user with that name already exists'
            }, 409


@content_ns.route('/content/<string:user>/<string:name>/')
class ContentView(Resource):
    @content_ns.doc('get content')
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

    @api.expect(edit_parser)
    @content_ns.doc('create or update content')
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
            port=environ.get('PORT', 5000),
            debug=environ.get('DEBUG', False))
