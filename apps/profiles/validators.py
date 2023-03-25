from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible


@deconstructible
class CustomUsernameValidator(RegexValidator):
    regex = r'^[a-zA-Z0-9]+([-]?[a-zA-Z0-9]+)*$'
    message = 'Username may only contain English letters, numbers, and dashes ("-"), and cannot start or end with a ' \
              'dash'
