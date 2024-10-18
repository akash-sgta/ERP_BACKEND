from django.db import models


def create_new_key(_model: models.Model, field_name: str):
    key = None
    try:
        while True:
            try:
                key = create_random(
                    symbols=False,
                    lower_case=False,
                )
                exec("_model.objects.get({}=key)".format(field_name))
            except _model.DoesNotExist:
                break
    except Exception:
        key = None
    return key


def sha(input_string, bits=256):
    import hashlib
    from math import floor

    # =======================================
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    _bytes = floor(bits / 8)
    sha_digest = sha256_hash[:_bytes]
    return sha_digest.hex()


def validate_phone_number(value):
    import re
    from django.core.exceptions import ValidationError

    # =======================================
    pattern = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
    if re.match(pattern, value) is not None:
        return value
    else:
        raise ValidationError("Invalid Phone Number")


def validate_file_name(file_name):
    from util._models.file_type import FileType
    from django.core.exceptions import ValidationError

    # =======================================
    file_name = file_name.split(".")
    if len(file_name) < 2:
        raise ValidationError("Invalid File Name")
    else:
        try:
            file_ref = FileType.objects.get(code=file_name[1])
        except FileType.DoesNotExist:
            file_ref = FileType.objects.create(code=file_name[1])
    return file_name[0], file_ref


def validate_string_len(text, stlen=15):
    from django.core.exceptions import ValidationError
    import re

    # =======================================
    pattern = f"^[{create_random(randomize=False)}]" + "{" + f"{stlen}" + "}$"
    if len(text) == 0 or re.match(pattern, text) is not None:
        return text
    else:
        raise ValidationError("Invalid String Length")


def create_random(
    randomize=True,
    upper_case=True,
    lower_case=True,
    numbers=True,
    symbols=True,
    stlen=127,
):
    import string
    import random

    # =======================================
    pattern = ""
    text = ""
    if upper_case is True:
        pattern = pattern + string.ascii_uppercase
    if lower_case is True:
        pattern = pattern + string.ascii_uppercase
    if numbers is True:
        pattern = pattern + "0123456789"
    if pattern != "":
        if randomize is True:
            text = "".join(random.choices(pattern, k=stlen)[:stlen])
        else:
            text = pattern
    return text
