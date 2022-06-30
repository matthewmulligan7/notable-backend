from flask import request, abort
from flask_restx import Resource
from functools import partial
import json
import os
import random
import requests
from time import time
from typing import Dict, List
import yaml


class LoggerMM:
    """
    This class standardizes log output to a consistent format.
    """

    def __init__(self, logger):
        """
        Initialize class.
        :param logger: logger object to use
        """
        self.logger = logger

    def log(self, message, remote_addr=None, user=None, log_level='INFO'):
        """
        Format and log the given message.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :param log_level: log level from [ERROR, WARN, INFO, DEBUG]
        :return: None
        """
        try:
            if not remote_addr:
                remote_addr = request.remote_addr
        except:
            pass
        try:
            if not user:
                user = request.headers.get('X-Auth-User')
        except:
            pass
        log_level = log_level.upper()
        now_ts = time()
        log_method = self.logger.info
        if log_level == 'ERROR':
            log_method = self.logger.error
        elif log_level == 'WARN' or log_level == 'WARNING':
            log_method = self.logger.warn
        elif log_level == 'DEBUG':
            log_method = self.logger.debug
        log_message = {'level': log_level, 'time': now_ts, 'remote_addr': remote_addr, 'user': user, 'output': message}
        log_method(json.dumps(log_message))

    def debug(self, message, remote_addr=None, user=None):
        """
        Convenience method to log a message at DEBUG level.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :return: None
        """
        self.log(message, remote_addr=remote_addr, user=user, log_level='DEBUG')

    def info(self, message, remote_addr=None, user=None):
        """
        Convenience method to log a message at INFO level.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :return: None
        """
        self.log(message, remote_addr=remote_addr, user=user, log_level='INFO')

    def warn(self, message, remote_addr=None, user=None):
        """
        Convenience method to log a message at WARN level.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :return: None
        """
        self.log(message, remote_addr=remote_addr, user=user, log_level='WARN')

    def warning(self, message, remote_addr=None, user=None):
        """
        Alias for warn function.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :return: None
        """
        self.warn(message, remote_addr=remote_addr, user=user)

    def error(self, message, remote_addr=None, user=None):
        """
        Convenience method to log a message at ERROR level.
        :param message: message to report
        :param remote_addr: calling client's IP address, if available (not needed if client_request is populated)
        :param user: calling client user, if available (not needed if client_request is populated)
        :return: None
        """
        self.log(message, remote_addr=remote_addr, user=user, log_level='ERROR')


class APIResource(Resource):
    def __init__(self, ns):
        super().__init__()
        self.logger = LoggerMM(ns.logger)


class APILogger:
    """
    This is a special type of decorator known as a descriptor (instead of a method it is a class). It will
    automatically log basic accounting info to the logger object it has been provided by the calling method via
    the class instance data.

    IMPORTANT NOTE: When calling @APILogger, it MUST be at the top of any other declared decorators.

    The static methods in this class can also be used on their own as well, of course, they just need a logger
    object passed in.
    """

    def __init__(self, f):
        """
        Initialize class.
        :param f: function to decorate
        """
        self.f = f

    def __call__(self, *args, **kwargs):
        """
        Build and log the message for the wrapped function.
        :param args: ordered args
        :param kwargs: keyword args
        :return: executing function
        """
        message = '{} called.'.format(self.f.__qualname__)
        args[0].logger.info(message)
        return self.f(*args, **kwargs)

    def __get__(self, instance, owner):
        """
        Call the wrapped function and include the calling instance's context.
        :param instance: calling instance
        :param owner: owner of calling instance (not used here)
        :return: executing function
        """
        ret_fun = partial(self.__call__, instance)
        ret_fun.__name__ = self.f.__name__
        ret_fun.__doc__ = self.f.__doc__
        try:
            ret_fun.__apidoc__ = self.f.__apidoc__
        except:
            pass
        return ret_fun


def read_config_file(config_file: str):
    """
    Load parameters from a config file into a dict.
    :param config_file: full path to config file (YAML or JSON)
    :return: dict or None if unsupported config file format
    """
    config_file_lc = config_file.lower()
    with open(config_file, 'r') as f:
        if config_file_lc.endswith('.yaml') or config_file_lc.endswith('.yml'):
            config = yaml.safe_load(f)
        elif config_file_lc.endswith('.json'):
            config = json.load(f)
        else:
            print('Error, unrecognized config file format (YAML and JSON are currently supported).')
            return None
    return config


def str_to_int(*args):
    val_tuple = ()
    for val in args:
        try:
            val_tuple += (int(val),)
        except TypeError:
            val_tuple += (val,)
    return val_tuple


def std_response(message, status: bool) -> Dict:
    """
    Responds in formatted method with True/False arguments
    and contains a string/json
    :param message: String or dictionary
    :param status: Python bool True/False
    """
    return {'message': message, 'status': status}


def abort_response(message, status: int) -> Dict:
    """
    Responds in formatted method with specified http 
    status code and contains a string/json with inherent
    status False
    :param message: String or dictionary
    :param status: Python bool True/False
    """
    return abort(status, {'message': message, 'status': False})


def check_required(request, required: list):
    """
    Checks to see if required arguments are in the request
    Args:
        request (request): request.json or request.args
        required (list): A list of parameters to check for in the request
    Returns:
        boolean:  Returns False on any failure
    """
    try:
        for key in required:
            if key not in request:
                return False
        return True
    except:
        return False


def check_any(request, anylist: List):
    """
    Checks to see if at least one of list members are in the request
    Args:
        request (request): request.json or request.args
        any (list): A list of parameters to check for in the request
    Returns:
        boolean:  Returns True on any member found in list
    """
    exists = False
    try:
        for key in anylist:
            if key in request:
                exists = True
        return exists
    except:
        return False


def check_only(request, onlylist: List):
    """
    Checks to see if only at the list members are in the request
    Args:
        request (request): request.json or request.args
        any (list): A list of parameters to check for in the request
    Returns:
        boolean:  Returns True on any member found in list
    """
    allowed = True
    if check_any(request, onlylist):
        try:
            for k, v in request.items():
                if k not in onlylist:
                    allowed = False
            return allowed
        except:
            return False
    return False