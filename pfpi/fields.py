# -*- coding: utf-8 -*-
from .exceptions import PfigAttributeError
from .utils import Constant, Messages
from abc import ABCMeta, abstractmethod
import re


class BaseField:
    """
    Protocol to build a Field classes.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_valid(self):
        """
        abstract method return boolean if the object is valid or has errors
        :return:
        """
        raise NotImplementedError()

    @abstractmethod
    def valid(self):
        """
        Abstract method that check if the object has field errors.
        :return:
        """
        raise NotImplementedError()


class CharField(BaseField):
    """
    Class to generate a char field types.
    """

    def __init__(self, required=True, default=None, label=None, value=None, pattern=None):
        """
        Initialize the a char field type.
        :param required: boolean by default is True
        :param default: Default value, by default is None
        :param label:  Label to display the field.
        :param value: The value assigned on the field.
        :param pattern: The Regular expression partner to apply on the field.
        """
        self.required, self.default, self.label, self.value, self.pattern = required, default, label, value, pattern
        if self.default and not self.value:
            self.value = self.default

    def valid(self):
        flag = True
        if self.required:
            if not self.value:
                raise PfigAttributeError(Messages.FIELD_REQUIRED_MISSING.format(self.label))
            else:
                if self.pattern:
                    counter = 0
                    for regular_expression in self.pattern:
                        re_correct = True if re.match(pattern=regular_expression, string=self.value) else False
                        if re_correct:
                            counter += 1
                            break
                    if counter <= 0:
                        raise PfigAttributeError(Messages.RE_INVALID_FORMAT.format(self.label))
        return flag

    def is_valid(self):
        return True if self.valid() else False


class ListField(BaseField):
    """
    Class to generate a list field types.
    """

    def __init__(self, required=True, default=None, label=None, value=None, choices=Constant.TRANSACTION_TYPES_LIST):
        """
        Initialize the a list field type.
        :param required: boolean by default is True
        :param default: Default value, by default is None
        :param label:  Label to display the field.
        :param value: The value assigned on the field.
        :param choices: The available choices list.
        """
        self.required, self.default, self.label, self.value, self.choices = required, default, label, value, choices
        if self.default and not self.value:
            self.value = self.default

    def valid(self):
        flag = True
        if self.required:
            if not self.value:
                raise PfigAttributeError(Messages.FIELD_REQUIRED_MISSING.format(self.label))
            else:
                if self.value not in self.choices:
                    raise PfigAttributeError(Messages.OPTION_SELECTED_INVALID)
        return flag

    def is_valid(self):
        return True if self.valid() else False


class FloatField(BaseField):

    """
    Class to generate Float field types.
    """

    def __init__(self, required=True, default=None, label=None, value=None):
        """
        Initialize the a list field type.
        :param required: boolean by default is True
        :param default: Default value, by default is None
        :param label:  Label to display the field.
        :param value: The value assigned on the field.
        """
        self.required, self.default, self.label, self.value = required, default, label, value
        if self.default is not None:
            self.value = self.default

    def valid(self):
        flag = True
        if self.required:
            if not self.value:
                raise PfigAttributeError(Messages.AMOUNT_REQUIRED.format(self.label))
        if self.value is not None:
            try:
                self.value = float(self.value)
            except ValueError:
                raise PfigAttributeError(Messages.FLOAT_INVALID)
        return flag

    def is_valid(self):
        return True if self.valid() else False


class BooleanField(BaseField):
    """
    Class to generate Boolean field types.
    """

    def __init__(self, default=None, label=None, value=None):
        """
        Initialize the boolean field
        :param default:
        :param label:
        :param value:
        """
        self.default, self.label, self.value = default, label, value
        if self.default is not None:
            self.value = self.default

    def valid(self):
        flag = True
        if self.value is not None:
            try:
                self.value = bool(self.value)
            except ValueError:
                raise PfigAttributeError(Messages.BOOLEAN_FIELD_INVALID)
        return flag

    def is_valid(self):
        return True if self.valid() else False
