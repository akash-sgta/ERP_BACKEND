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
