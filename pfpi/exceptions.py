# -*- coding: utf-8 -*-


class PfigAttributeError(Exception):
    """
    Exception raised when a attribute is wrong or missing
    """
    pass


class PfigTransactionError(Exception):
    """
    Exception raised when a transaction is failed.
    """
    pass
