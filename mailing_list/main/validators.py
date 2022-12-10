from django.core.exceptions import ValidationError
import re


def phone_validator(phone_number):
    if re.match('^7\d{10}$', str(phone_number)) is not None:
        return phone_number
    raise ValidationError(
        'Номер телефона должен быть в формате 7XXXXXXXXXX (X - цифра от 0 до 9)')
