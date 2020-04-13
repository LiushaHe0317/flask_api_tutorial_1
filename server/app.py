import flask
import bcrypt
import flask_restful as rest
from pymongo import MongoClient

app = flask.Flask(__name__)
api = rest.Api(app)

# connect to mongodb and create database and corresponding collections
client = MongoClient("mongodb://db:27017")

db = client.SentencesDatabase

users = db['Users']

def user_match(username, password, method):
    user = users.find({'Username': username})

    if method == 'register':
        if user.count() > 0:
            return 303
        else:
            return 200
    else:
        if user.count() > 0:
            if user[0]['Password'] == bcrypt.hashpw(password.encode('utf-8'), user[0]['Password']):
                return 200
            else:
                return 301
        else:
            return 302


def countToken(username):
    user = users.find({'Username': username})
    return user[0]['No of Token']


class Register(rest.Resource):
    def post(self):
        data = flask.request.get_json()
        username = data['Username']
        password = data['Password']
        status_code = user_match(username, password, 'register')

        if status_code == 200:
            users.insert({
                'Username': username,
                'Password': bcrypt.hashpw(password, bcrypt.gensalt()),
                'Sentence': '',
                'No of Token': 6
            })

            return flask.jsonify({
                'status code': 200,
                'message': 'You have registered successfully.'
            })
        elif status_code == 301:
            return flask.jsonify({
                'status code': 301,
                'message': 'Username and password do not match.'
            })
        elif status_code == 303:
            return flask.jsonify({
                'status code': status_code,
                'message': 'Username already exists.'
            })


class Save(rest.Resource):
    def post(self):
        data = flask.request.get_json()
        username = data['Username']
        password = data['Password']
        sentence = data['Sentence']
        status_code = user_match(username, password, 'save')
        num_token = countToken(username)

        if status_code == 200:
            if num_token <= 0:
                return flask.jsonify({
                    'status_code': 201,
                    'message': 'You have no tokens.'
                })
            else:
                users.update({
                    'Username': username
                }, {'$set': {
                    'Sentence': sentence,
                    'No of Token': num_token - 1
                }})
                return flask.jsonify({
                    'status_code': status_code,
                    'message': 'Sentence saved successfully.'
                })
        elif status_code == 301:
            return flask.jsonify({
                'status code': status_code,
                'message': 'Username and password do not match.'
            })
        elif status_code == 302:
            return flask.jsonify({
                'status_code': status_code,
                'massage': 'User does not exist.'
            })


class Retrieve(rest.Resource):
    def post(self):
        data = flask.request.get_json()
        username = data['Username']
        password = data['Password']

        status_code = user_match(username, password, 'retrieve')

        if status_code == 200:
            user = users.find({'Username': username})
            return flask.jsonify({
                'status code': status_code,
                'Sentence': user[0]['Sentence'],
                'No of Token': user[0]['No of Token']
            })
        elif status_code == 301:
            return flask.jsonify({
                'status code': status_code,
                'message': 'Username and password do not match.'
            })
        elif status_code == 302:
            return flask.jsonify({
                'status_code': status_code,
                'massage': 'User does not exist.'
            })


@app.route('/')
def index():
    return 'Welcome to API Test Environment.'

api.add_resource(Register, '/register')
api.add_resource(Save, '/save')
api.add_resource(Retrieve, '/retrieve')


if __name__=='__main__':
    app.run(host='0.0.0.0', debug=True)