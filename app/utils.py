from time import strftime

from flask import jsonify, request
from app.extensions import parser, logger
from marshmallow import fields, validate as validate_
import joblib
from functools import wraps

import werkzeug


def parse_req(argmap):
    """
    Parser request from client
    :param argmap:
    :return:
    """
    return parser.parse(argmap)


def send_result(data=None, message="OK", code=200, version=2, status=True):
    """
    Args:
        data: simple result object like dict, string or list
        message: message send to client, default = OK
        code: code default = 200
        version: version of api
    :param data:
    :param message:
    :param code:
    :param version:
    :param status:
    :return:
    json rendered sting result
    """
    res = {
        "status": status,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version(version)
    }
    logger.info(res)
    return jsonify(res), 200


def send_error(data=None, message="Error", code=400, version=2, status=False):
    """

    :param data:
    :param message:
    :param code:
    :param version:
    :param status:
    :return:
    """
    res_error = {
        "status": status,
        "code": code,
        "message": message,
        "data": data,
        "version": get_version(version)
    }
    logger.error(res_error)
    return jsonify(res_error), code


def get_version(version):
    """
    if version = 1, return api v1
    version = 2, return api v2
    Returns:

    """
    return "v2.0" if version == 2 else "v1.0"


class FieldString(fields.String):
    """
    validate string field, max length = 1024
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 1024  # 1 kB

    def __init__(self, validate=None, requirement=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        if requirement is not None:
            validate = validate_.NoneOf(error='Dau vao khong hop le!', iterable={'full_name'})
        super(FieldString, self).__init__(validate=validate, required=requirement, **metadata)


class FieldNumber(fields.Number):
    """
    validate number field, max length = 30
    Args:
        des:

    Returns:

    """
    DEFAULT_MAX_LENGTH = 30  # 1 kB

    def __init__(self, validate=None, **metadata):
        """

        Args:
            validate:
            metadata:
        """
        if validate is None:
            validate = validate_.Length(max=self.DEFAULT_MAX_LENGTH)
        super(FieldNumber, self).__init__(validate=validate, **metadata)




def logger_accountability(func):
    """ Timing and logging all input and output of the function
    :param func: takes any method which elapsed time needs to be calculated
    :return: the result of method with logging the time taken
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        ts = strftime('[%Y-%b-%d %H:%M]')
        result = func(*args, **kwargs)
        logger.info('%s %s %s %s %s %s',
                         ts,
                         request.remote_addr,
                         request.method,
                         request.scheme,
                         request.full_path,
                         result[1])
        logger.info(f"{ts} {func.__name__} output parameters {result[0].json['data']}" )
        # elapsed: float = time() - start
        # pretty = "=" * 50
        # logger.debug(f"{pretty} {func.__name__} {pretty}")
        # logger.info(f"{ts} {func.__name__} took {round(elapsed, 2)}ms")
        # logger.debug(f"{ts} {func.__name__} input parameters {kwargs}")
        # logger.debug(f"{ts} {func.__name__} output parameters {result}")
        # logger.debug("=" * 100)
        return result

    return wrapper

def is_password_contain_space(password):
    """

    Args:
        password:

    Returns:
        True if password contain space
        False if password not contain space

    """
    return ' ' in password


def hash_password(str_pass):
    return werkzeug.security.generate_password_hash(str_pass)

