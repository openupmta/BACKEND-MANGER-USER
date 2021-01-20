from flask import Blueprint, request
from app.schema.schema_validator import data_validator
from app.models import Data
from app.utils import send_result, send_error
import uuid
from jsonschema import validate

api = Blueprint('data', __name__)


@api.route('', methods=['POST'])
# @jwt_required
def create_data():
    """ This is api for the city management create city.

        Request Body:

        Returns:

        Examples::
    """

    try:
        json_data = request.get_json()
        # Check valid params
        validate(instance=json_data, schema=data_validator)
    except Exception as ex:
        return send_error(message=str(ex))
    _id = str(uuid.uuid1())
    json_data['id'] = _id
    instance = Data()
    for key in json_data.keys():
        instance.__setattr__(key, json_data[key])
    try:
        instance.save_to_db()
    except Exception as ex:
        return send_error(message="Insert to database error: " + str(ex))

    return send_result(data=json_data, message="Create city successfully!")


@api.route('/<data_id>', methods=['PUT'])
# @jwt_required
# @admin_required()
def update_city(data_id):
    """ This is api for the city management edit the city.

        Request Body:

        Returns:

        Examples::

    """

    data = Data.find_by_id(data_id)
    if data is None:
        return send_error(message="Not found data!")

    try:
        json_data = request.get_json()
        # Check valid params
        validate(instance=json_data, schema=data_validator)
    except Exception as ex:
        return send_error(message=str(ex))
    for key in json_data.keys():
        data.__setattr__(key, json_data[key])
    try:
        data.save_to_db()
    except Exception as ex:
        return send_error(message="Database error: " + str(ex))

    return send_result(data=json_data, message="Update city successfully!")


@api.route('/<data_id>', methods=['DELETE'])
# @jwt_required
# @admin_required()
def delete_data(data_id):
    """ This api for the city management deletes the cities.

        Returns:

        Examples::

    """
    data = Data.find_by_id(data_id)
    if data is None:
        return send_error(message="Not found data!")

    # Also delete all children foreign key
    data.delete_from_db()

    return send_result(data=None, message="Delete city successfully!")


@api.route('', methods=['GET'])
def get_all_data():
    """ This api gets all cities.
        Returns:
        Examples:
    """
    results = []
    datas = Data.get_all()
    for data in datas:
        results.append(data.convert_json())
    return send_result(data=list(results), message="Successfully")


@api.route('/<data_id>', methods=['GET'])
def get_city_by_id(data_id):
    """ This api get information of a city.

        Returns:

        Examples::

    """

    data = Data.find_by_id(data_id)
    if not data:
        return send_error(message="city not found.")
    return send_result(data=data.convert_json())
