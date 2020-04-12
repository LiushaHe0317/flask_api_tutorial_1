import flask
import flask_restful as rest

app = flask.Flask(__name__)
api = rest.Api(app)


def check_parameters(postedData, funcName='add'):
    if not postedData['x'] or not postedData['y']:
        return 301
    elif funcName == 'div' and postedData['y'] == 0:
        return 302
    return 200

class Add(rest.Resource):
    def post(self):
        postedData = flask.request.get_json()

        status_code = check_parameters(postedData, 'add')

        if status_code == 200:
            x = postedData['x']
            y = postedData['y']

            return flask.jsonify({'eessage': x+y})
        elif status_code == 301:
            return flask.jsonify({'message': 'parameter x or y cannot be empty'})


class Substract(rest.Resource):
    def post(self):
        postedData = flask.request.get_json()

        status_code = check_parameters(postedData, 'sub')

        if status_code == 200:
            x = postedData['x']
            y = postedData['y']

            return flask.jsonify({'eessage': x-y})
        elif status_code == 301:
            return flask.jsonify({'message': 'parameter x or y cannot be empty'})


class Multiply(rest.Resource):
    def post(self):
        postedData = flask.request.get_json()

        status_code = check_parameters(postedData, 'mul')

        if status_code == 200:
            x = postedData['x']
            y = postedData['y']

            return flask.jsonify({'eessage': x*y})
        elif status_code == 301:
            return flask.jsonify({'message': 'parameter x or y cannot be empty'})


class Divide(rest.Resource):
    def post(self):
        postedData = flask.request.get_json()

        status_code = check_parameters(postedData, 'div')

        if status_code == 200:
            x = postedData['x']
            y = postedData['y']

            return flask.jsonify({'eessage': x/y})
        elif status_code == 301:
            return flask.jsonify({'message': 'parameter x or y cannot be empty'})
        elif status_code == 302:
            return flask.jsonify({'message': 'y cannot be 0 in division'})


api.add_resource(Add, '/add')
api.add_resource(Substract, '/substract')
api.add_resource(Multiply, '/multiply')
api.add_resource(Divide, '/divide')

@app.route('/')
def index():
    return 'Welcome to Third API Test Environment.'

if __name__=='__main__':
    app.run(debug=True)