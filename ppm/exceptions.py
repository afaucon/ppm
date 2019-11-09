# -*- coding: utf-8 -*-

"""
ppm.exceptions
==============
This module contains the set of ppm exceptions.
"""

class GenericException(Exception):
    """
    The generic class for all exceptions.
    It is not meant to be directly instantiated.
    """

class NotYetImplementedException(GenericException):
    """
    This exception is raised when attempting to reach code that has not yet been implemented.
    """

class UndefinedPythonProjectsPath(GenericException):
    """
    PYTHON_PRJ environment variable is not declared.
    """

class PythonProjectsPathDoesNotExist(GenericException):
    """
    PYTHON_PRJ environment variable does not contain a valid directory path.
    """