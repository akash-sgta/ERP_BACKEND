# =====================================================================
from django.contrib.admin.models import LogEntry
from django.db import models, IntegrityError
from django.apps import apps


# =====================================================================
def update_change_log(_model: models.Model, *args, **kwargs):
    C_USER = "user"
    C_USER_DEFAULT = "DEFAULT"
    # ==========================
    try:
        user_id = kwargs[C_USER]
    except KeyError:
        user_id = C_USER_DEFAULT
    finally:
        user_id = user_id.upper()

    if _model.pk is None:
        _model.createdBy = user_id
    else:
        _model.changedBy = user_id

    return user_id


def update_active_status(_model: models.Model, *args, **kwargs):
    C_DEL_FLAG = "del_flag"
    # ===============================

    is_active_old = _model.is_active
    is_active_new = _model.is_active

    try:
        kwargs[C_DEL_FLAG]
    except KeyError:
        pass
    else:
        if kwargs[C_DEL_FLAG]:
            is_active_new = False
        else:
            is_active_new = True

    _model.is_active = is_active_new

    return is_active_old, is_active_new


def get_related_models(_model: models.Model, on_delete_behaviour=models.CASCADE, *args, **kwargs):
    C_CUSTOM_APPS = tuple("patient,profile,staff,util".split(","))

    related_models = dict()
    custom_models = list(model for model in apps.get_models() if model._meta.app_label in C_CUSTOM_APPS)
    for model in custom_models:
        related_models.update({model: list()})
        for field in model._meta.get_fields():
            if (
                isinstance(field, models.ForeignKey)
                and field.remote_field.model == _model.__class__
                and field.remote_field.on_delete == on_delete_behaviour
            ):
                related_models[model].append(field.name)
    return related_models


def update_reference_objects(_model: models.Model, *args, **kwargs):
    related_models = get_related_models(_model, *args, **kwargs)
    for related_model in related_models.keys():
        if len(related_models[related_model]) > 0:
            expression = "related_model.objects.filter({}=_model.pk)".format(related_models[related_model][0])
            try:
                related_refs = eval(expression)
                if len(related_refs) == 0:
                    raise related_model.DoesNotExist
            except related_model.DoesNotExist:
                pass
            except IndexError:
                pass
            else:
                for related_ref in related_refs:
                    if _model.is_active:
                        related_ref.save()
                    else:
                        related_ref.delete()
    return None


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
