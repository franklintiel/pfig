# -*- coding: utf-8 -*-
from .fields import CharField, ListField, FloatField, BooleanField
from .utils import Constant, Utils, Messages
from .exceptions import PfigAttributeError, PfigTransactionError
import urllib
import urllib2
import json


class WebService(object):
    """
    Main Web services class.
    """
    commerce = CharField(label='commerce')
    firstname = CharField(label='firstname')
    lastname = CharField(label='lastname')
    description = CharField(label='description')
    var_text = CharField(required=False, label='var_text')
    type = ListField(label='type', choices=Constant.TRANSACTION_TYPES_LIST)
    email = CharField(label='email', pattern=Constant.EMAIL_AVAILABLE_PATTERN)
    production_mode = BooleanField(label='production_mode', default=False)

    @property
    def __fields(self):
        """
        Return a  list with all availables fields.
        :return: all fields list
        """
        return [i for i in dir(self) if i[:1] != '_' and not callable(i) and\
                not i in Constant.METHODS_UNAVAILABLE_LIST]

    @property
    def to_json(self):
        """
        get all attributes as dictionary
        :return: dictionary of attributes
        """
        object = {}
        for field in self.__fields:
            if hasattr(self, field):
                instance = getattr(self, field)
                object[field] = instance.value
        return object

    @property
    def to_url(self):
        """
        url encode the object fields
        :return: fields as url query format
        """
        return urllib.urlencode(query=self.to_json)

    def __init__(self, commerce, type, firstname, lastname, email, description, production_mode=False):
        """
        Instance a web services class.
        :param commerce:
        :param type:
        :param firstname:
        :param lastname:
        :param email:
        :param description:
        """
        self.commerce.value = commerce if commerce else None
        self.type.value = type if type else None
        self.firstname.value = firstname if firstname else None
        self.lastname.value = lastname if lastname else None
        self.email.value = email if email else None
        self.description.value = description if description else None
        self.production_mode.value = production_mode
        self.var_text.value = self.description.value

    def valid(self):
        """
        Validate all availables fields from the class instanced.
        :return:
        """
        counter = 0
        for field in self.__fields:
            if hasattr(self, field):
                instance = getattr(self, field)
                if instance:
                    if instance.is_valid():
                        counter += 1
        return True if counter == len(self.__fields) else False

    def is_valid(self):
        """
        Return a boolean value after to check if the object is valid or has errors.
        :return:
        """
        return True if self.valid() else False

    def call(self):
        """
        call web services from Páguelo Fácil payment gateways.
        :return: response given from the web services called
        """
        endpoint = Constant.PRODUCTION_ENDPOINT if self.production_mode.value else Constant.DEVELOPMENT_ENDPOINT
        try:
            request = urllib2.Request(url=endpoint, data=self.to_url)
            response = urllib2.urlopen(request)
            return json.loads(response.read())
        except Exception as e:
            raise PfigTransactionError(e)


class CreditCardService(WebService):
    """
    class to add Credit cards through Payment Gateway
    """
    cc_number = CharField(label='cc_number', pattern=Constant.CREDIT_CARD_NUMBER_AVAILABLE_PATTERN)
    ccv2 = CharField(label='ccv2', pattern=Constant.CCV2_AVAILABLE_PATTERN)
    cc_expiration = CharField(label='cc_expiration', pattern=Constant.EXPIRATION_DATE_AVAILABLE_PATTERN)

    def __init__(
            self, commerce, firstname, lastname, email, description, cc_number, ccv2, cc_expiration,
            production_mode=False):
        """
        Instance a credit card class
        :param commerce:
        :param firstname:
        :param lastname:
        :param email:
        :param description:
        :param cc_number:
        :param ccv2:
        :param cc_expiration:
        :param production_mode:
        """
        self.type.value = Constant.CREDIT_CARD_TOKEN_TYPE
        super(CreditCardService, self).__init__(
            commerce=commerce, type=self.type.value, firstname=firstname, lastname=lastname, email=email,
            description=description, production_mode=production_mode)
        self.cc_number.value = cc_number
        self.ccv2.value = ccv2
        self.cc_expiration.value = cc_expiration

    def valid(self):
        is_valid = super(CreditCardService, self).valid()
        if self.cc_expiration.value:
            cc_expiration = Utils.get_date_obj(date_str=self.cc_expiration.value, format='%Y-%m')
            if cc_expiration:
                last_day = Utils.get_last_day(month=cc_expiration.month, year=cc_expiration.year)
                if last_day > 0:
                    date_str = '{0}-{1}'.format(self.cc_expiration.value, last_day)
                    date_obj = Utils.get_date_obj(date_str=date_str, format='%Y-%m-%d')
                    if Utils.get_current_date() > date_obj:
                        raise PfigAttributeError(Messages.CREDIT_CARD_EXPIRED)
        return is_valid


class TokenPaymentService(WebService):
    """
    Class to do payments using Token
    """
    token = CharField(label='token')
    amount = FloatField(label='amount')

    def __init__(self, commerce, firstname, lastname, email, description, amount, token, production_mode=False):
        """
        Instance a Payment class
        :param commerce:
        :param firstname:
        :param lastname:
        :param email:
        :param description:
        :param amount:
        :param token:
        :param production_mode:
        """
        self.type.value = Constant.TRANSACTION_TOKEN_TYPE
        self.amount.value = amount if amount else 0.00
        super(TokenPaymentService, self).__init__(
            commerce=commerce, firstname=firstname, lastname=lastname, email=email, description=description,
            type=self.type.value, production_mode=production_mode)
        self.token.value = token


class PaymentService(WebService):
    """
    Class to do payments
    """
    amount = FloatField(label='amount')
    cc_number = CharField(label='cc_number', pattern=Constant.CREDIT_CARD_NUMBER_AVAILABLE_PATTERN)
    ccv2 = CharField(label='ccv2', pattern=Constant.CCV2_AVAILABLE_PATTERN)
    cc_expiration = CharField(label='cc_expiration', pattern=Constant.EXPIRATION_DATE_AVAILABLE_PATTERN)

    def __init__(
            self, commerce, firstname, lastname, email, description, amount, cc_number, ccv2, cc_expiration,
            production_mode=False):
        """
        Instance of Payment Class
        :param commerce:
        :param firstname:
        :param lastname:
        :param email:
        :param description:
        :param amount:
        :param cc_number:
        :param ccv2:
        :param cc_expiration:
        :param production_mode:
        """
        self.type.value = Constant.TRANSACTION_TOKEN_TYPE
        self.amount.value = amount if amount else 0.00
        super(PaymentService, self).__init__(
            commerce=commerce, firstname=firstname, lastname=lastname, email=email, description=description,
            type=self.type.value, production_mode=production_mode)
        self.cc_number.value = cc_number
        self.ccv2.value = ccv2
        self.cc_expiration.value = cc_expiration

    def valid(self):
        is_valid = super(PaymentService, self).valid()
        if self.cc_expiration.value:
            cc_expiration = Utils.get_date_obj(date_str=self.cc_expiration.value, format='%Y-%m')
            if cc_expiration:
                last_day = Utils.get_last_day(month=cc_expiration.month, year=cc_expiration.year)
                if last_day > 0:
                    date_str = '{0}-{1}'.format(self.cc_expiration.value, last_day)
                    date_obj = Utils.get_date_obj(date_str=date_str, format='%Y-%m-%d')
                    if Utils.get_current_date() > date_obj:
                        raise PfigAttributeError(Messages.CREDIT_CARD_EXPIRED)
        return is_valid
