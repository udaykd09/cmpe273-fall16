from flask import Flask, request, Response, jsonify
from model import db, User, CreateDB
from model import app as application
import simplejson as json
from sqlalchemy.exc import IntegrityError
app = Flask(__name__)


""" CONSTANTS """
APP_VERSION = 'v1'
EXPENSES_API = '/' + APP_VERSION + '/' + 'expenses'
JSON_CONTENT = 'application/json'


""" Content type """
def valid_content_type(request_content_type):
    return request_content_type == JSON_CONTENT


""" ERROR 415 Invalid Content-type """
@app.errorhandler(415)
def invalid_content(error=None):
    message = {
        'status': 415,
        'message': 'Invalid Content Type: ' + request.headers['Content-Type']
    }
    resp = jsonify(message)
    resp.status_code = 415
    return resp


""" ERROR 404 Page not Found """
@app.errorhandler(404)
def not_found(error=None):
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.route('/')
def index():
	return 'Hello World! Welcome to the expense manager\n'


def request_parser(request_in):
    # Create User object from request
    request = json.loads(request_in.get_data())
    print("Request: {}".format(request))
    user = User(request['name'],
                request['email'],
                request['category'],
                request['description'],
                request['link'],
                int(request['estimated_costs']),
                request['submit_date'])
    return user


def response_parser(user):
    # Format the response
    data = json.dumps({'id': str(user.id),
                       'name': user.name,
                       'email': user.email,
                       'category': user.category,
                       'description': user.description,
                       'link': user.link,
                       'estimated_costs': str(user.estimated_costs),
                       'submit_date': user.submit_date,
                       'status': user.status,
                       'decision_date': user.decision_date}, indent=4)
    return data

""" POST REQUEST """


@app.route(EXPENSES_API, methods=['POST'])
def add_expense():
    try:
        # Update database
        user = request_parser(request)
        print("User : {}".format(user))
        db.session.add(user)
        db.session.commit()
        print("Post: Insert Successful")
        # Response
        user = User.query.filter_by(email=user.email,
                                    submit_date=user.submit_date,
                                    estimated_costs=user.estimated_costs).first_or_404()
        data = response_parser(user)
        print("Post: Query Successful")
    except IntegrityError:
        return Response(status=400)

    resp = Response(data, status=201, mimetype=JSON_CONTENT)
    return resp

""" GET REQUEST """


@app.route(EXPENSES_API + '/<expense_id>', methods=['GET'])
def get_expense(expense_id):
    # Select expense from db
    try:
        user = User.query.filter_by(id=expense_id).first_or_404()
        print("Get: Query Successful")
        data = response_parser(user)
    except IntegrityError:
        return not_found()

    resp = Response(data, status=200, mimetype=JSON_CONTENT)
    return resp

""" PUT REQUEST """


@app.route(EXPENSES_API + '/<expense_id>', methods=['PUT'])
def update_expense(expense_id):
    try:
        update_data = json.loads(request.get_data())
        print("Update : {} for id {}".format(update_data, expense_id))
        db.session.query(User).filter(User.id == expense_id).\
            update(update_data, synchronize_session=False)
        db.session.commit()
        print("Put: Query Successful")
    except IntegrityError:
        return not_found()
    return Response(status=202)

""" DELETE REQUEST """


@app.route(EXPENSES_API + '/<expense_id>', methods=['DELETE'])
def delete_expense(expense_id):
    try:
        db.session.query(User).filter(User.id == expense_id).delete()
        db.session.commit()
        print("Delete: Query Successful")
    except IntegrityError:
        return not_found()
    return Response(status=204)

""" USERS """


@app.route('/users')
def users():
	try:
		users = User.query.all()
		users_dict = {}
		for user in users:
			users_dict[user.username] = {
							'email': user.email
						}

		return json.dumps(users_dict)
	except IntegrityError:
		return json.dumps({})

""" DB INFO """


@app.route('/info')
def app_status():
	return json.dumps({'server_info': application.config['SQLALCHEMY_DATABASE_URI']})

""" CREATE DB """


def create_database():
    CreateDB()
    print("Database created")
    return json.dumps({'status':'True'})

""" CREATE TABLE """


def create_user_table():
	try:
		db.create_all()
		return json.dumps({'status':'True'})
	except IntegrityError:
		return json.dumps({'status':'False'})

""" MAIN """


if __name__ == '__main__':
    create_database()
    create_user_table()
    print("Table created")
    print("Starting Server --> localhost:80")
    app.run(host="0.0.0.0", port=80, debug=True)
