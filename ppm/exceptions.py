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
    The PYTON_PRJ environment variable is not declared.
    """

class PythonProjectsPathDoesNotExist(BasePpmException):
    """
    Write a description
    """