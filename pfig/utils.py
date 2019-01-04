# -*- coding: utf-8 -*-
import calendar
from datetime import datetime


class Constant(object):
    CREDIT_CARD_DEFAULT_DESCRIPTION = 'Adding the Credit card number {0} from the user {1} {2}, Email: {3}'
    CREDIT_CARD_NUMBER_AVAILABLE_PATTERN = ['4\d{15}$', '[2,5]\d{15}$']
    CCV2_AVAILABLE_PATTERN = ['\d{3}$']
    EXPIRATION_DATE_AVAILABLE_PATTERN = ["20[1-9][0-9]-(0?[1-9]|1[012])$"]
    EMAIL_AVAILABLE_PATTERN = ["(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"]
    CREDIT_CARD_TOKEN_TYPE = "storage"
    TRANSACTION_TOKEN_TYPE = "token"
    TRANSACTION_TYPES_LIST = [CREDIT_CARD_TOKEN_TYPE, TRANSACTION_TOKEN_TYPE]
    METHODS_UNAVAILABLE_LIST = ['valid', 'is_valid', 'to_json', 'to_url', 'call', 'production_mode']
    PRODUCTION_ENDPOINT = "https://recurrentes.paguelofacil.com/api/tokens"
    DEVELOPMENT_ENDPOINT = "https://recurrentes.pfserver.net/api/tokens"


class Messages(object):
    FIELD_REQUIRED_MISSING = "The {0} field is null, this value is required."
    OPTION_SELECTED_INVALID = "The value selected is not a valid option."
    FLOAT_INVALID = "The value should be a float, another type is given."
    RE_INVALID_FORMAT = "The {0} field has an invalid format."
    AMOUNT_REQUIRED = "The {0} field should be greater to zero."
    CREDIT_CARD_EXPIRED = "The Credit Card is expired."
    BOOLEAN_FIELD_INVALID = "The value should be a boolean, another type is given."


class Utils(object):

    @staticmethod
    def get_last_day(month, year):
        output = None
        last_day = calendar.monthrange(year=year, month=month)
        if last_day and last_day[1]:
            output = last_day[1]
        return output

    @staticmethod
    def get_date_obj(date_str, format):
        date_obj = datetime.strptime(date_str, format)
        return date_obj.date()

    @staticmethod
    def get_current_date():
        return datetime.now().date()
