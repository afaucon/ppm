# -*- coding: utf-8 -*-

"""
ppm.exceptions
==============
This module contains the set of ppm exceptions.
"""

class BasePpmException(Exception):
    """ 
    The base class for all ppm exceptions.
    It is not meant to be directly instantiated, unlike specific exceptions here below.
    """

class UndefinedPythonProjectsPath(BasePpmException):
    """
    PYTON_PRJ environment variable is not declared.
    """

class PythonProjectsPathDoesNotExist(BasePpmException):
    """
    PYTON_PRJ environment variable does not contain a valid directory path.
    """

class NotYetImplementedException(BasePpmException):
    """
    This exception is raised when attempting to reach code that has not yet been implemented.
    """