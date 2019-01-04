# PFPI (Paguelo Facil Payment Interface)
Easy python module to do payments through Paguelo Facil payment gateway.

## Requirements
- Python 2.7.x

## Installing
1) Install the pfpi module:
```shell
$ pip install pfpi
```

## How to add a new credit card.
```python
from pfpi.models import CreditCardService
commerce_key = 'abcdef'
production_mode = False # Change to True if you want use the production environment
cc = CreditCardService(
    commerce=commerce_key, firstname='first name', lastname='last name', email='example@domain.com',
    description='payment description', cc_number='4111111111111111', ccv2='123', cc_expiration='2019-12',
    production_mode=production_mode)
result = cc.call() # Add new credit card
print result # return a JSON object with the result
```

## How to do Payment.
```python
from pfpi.models import PaymentService
commerce_key = 'abcdef'
production_mode = False # Change to True if you want use the production environment
p = PaymentService(
    commerce=commerce_key, firstname='first name', lastname='last name', email='example@domain.com',
    description='payment description', amount=25.00, cc_number='4111111111111111', ccv2='123',
    cc_expiration='2019-12', production_mode=production_mode)
result = p.call() # Do Payment
print result # return a JSON object with the result
```

## How to do Payment using  Token given from credit card
```python
from pfpi.models import TokenPaymentService, CreditCardService
commerce_key = 'abcdef'
production_mode = False # Change to True if you want use the production environment
cc = CreditCardService(
    commerce=commerce_key, firstname='first name', lastname='last name', email='example@domain.com',
    description='payment description', cc_number='4111111111111111', ccv2='123', cc_expiration='2019-12',
    production_mode=production_mode)
result = cc.call() # get the credit card token
token = result['token']
p = TokenPaymentService(
    commerce=commerce_key, firstname='first name', lastname='last name', email='example@domain.com',
    description='payment description', amount=25.00, token=token, production_mode=production_mode)
result = p.call() # Do Payment
print result # return a JSON object with the result
```

## Uninstall pfpi
```shell
$ pip uninstall pfpi
```

## Additional Info
This module is based on the follow documentation [link](https://pfserver.net/plugins/api-transacciones/)

## Releases notes:

- 1.0.0: Services added to add credit cards and do payments.
- 1.0.1: Applying Validations before to call api services.