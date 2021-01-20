from flask import Blueprint, request
from app.schema.schema_validator import user_validator
from app.models import User
from app.utils import send_result, send_error
import uuid
from jsonschema import validate

api = Blueprint('user', __name__)


@api.route('', methods=['POST'])
# @jwt_required
def create_user():
    """ This is api for the city management create city.

        Request Body:

        Returns:

        Examples::
    """

    try:
        json_user = request.get_json()
        # Check valid params
        validate(instance=json_user, schema=user_validator)
    except Exception as ex:
        return send_error(message=str(ex))
    _id = str(uuid.uuid1())
    json_user['id'] = _id
    instance = User()
    for key in json_user.keys():
        instance.__setattr__(key, json_user[key])
    try:
        instance.save_to_db()
    except Exception as ex:
        return send_error(message="Insert to userbase error: " + str(ex))

    return send_result(data=json_user, message="Create city successfully!")


@api.route('/<user_id>', methods=['PUT'])
# @jwt_required
# @admin_required()
def update_user(user_id):
    """ This is api for the city management edit the city.

        Request Body:

        Returns:

        Examples::

    """

    user = User.find_by_id(user_id)
    if user is None:
        return send_error(message="Not found user!")

    try:
        json_user = request.get_json()
        # Check valid params
        validate(instance=json_user, schema=user_validator)
    except Exception as ex:
        return send_error(message=str(ex))
    for key in json_user.keys():
        user.__setattr__(key, json_user[key])
    try:
        user.save_to_db()
    except Exception as ex:
        return send_error(message="userbase error: " + str(ex))

    return send_result(data=json_user, message="Update city successfully!")


@api.route('/<user_id>', methods=['DELETE'])
# @jwt_required
# @admin_required()
def delete_user(user_id):
    """ This api for the city management deletes the cities.

        Returns:

        Examples::

    """
    user = User.find_by_id(user_id)
    if user is None:
        return send_error(message="Not found user!")

    # Also delete all children foreign key
    user.delete_from_db()

    return send_result(data=None, message="Delete city successfully!")


@api.route('', methods=['GET'])
def get_all_user():
    """ This api gets all cities.
        Returns:
        Examples:
    """
    results = []
    users = User.get_all()
    for user in users:
        results.append(user.convert_json())
    return send_result(data=list(results), message="Successfully")

@api.route('/search', methods=['GET'])
def get_all_search_user():
    """ This api gets all cities.
        Returns:
        Examples:
    """
    pageSize = request.args.get('pageSize', default=10, type=int)
    pageNumber = request.args.get('pageNumber', default=1, type=int)
    filter_name = request.args.get('filter', default=None, type=str)
    if filter_name == '':
        filter_name = None
    role = request.args.get('role', default=None, type=str)
    if role == '':
        role = None
    status = request.args.get('status', default=None, type=str)
    if status == '':
        status = None

    users = User.find_by_user_filter(filter_name, role, status)
    total = User.get_total_number()

    data = {
        'pageSize': pageSize,
        'pageNumber': pageNumber,
        'total': total,
        'users': users
    }
    return send_result(data=data, message="Successfully")

@api.route('/<user_id>', methods=['GET'])
def get_user_by_id(user_id):
    """ This api get information of a city.

        Returns:

        Examples::

    """

    user = User.get_by_id(user_id)
    if not user:
        return send_error(message="city not found.")
    return send_result(data=user.convert_json())
