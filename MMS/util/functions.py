# =====================================================================
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError, transaction
from django.apps import apps
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ModelSerializer
from django.core.exceptions import ValidationError
import re
import hashlib
from math import floor
import string
import random

from rest_framework.views import APIView
from django.http import QueryDict
from django.template.response import TemplateResponse
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.response import Response
from rest_framework import status
from django.db.models import ManyToOneRel

C_BLANK_RESPONSE = ReturnList([], serializer=None)
C_FORM_POP = ("csrfmiddlewaretoken",)
C_KEYS = ("id",)


# ===================================================================== VIEW
def cust_get_vars(_model: APIView = None, **kwargs):
    data = dict()
    for key in C_KEYS:
        try:
            if kwargs[key] == "":
                raise KeyError
            data[key] = kwargs[key]
        except KeyError:
            pass
    if len(data) == 0:
        data = None
    return data


def cust_get(_model: APIView, *args, **kwargs):
    vars = _model._get_vars(**kwargs)
    if vars is None:
        model_ref = _model.model.objects._all()
    else:
        try:
            model_ref = _model.model.objects._filter(**vars)
            if len(model_ref) == 0:
                raise _model.model.DoesNotExist
        except _model.model.DoesNotExist:
            model_ref = None
    if model_ref is not None:
        serializer_ref = _model.serializer_class(model_ref, many=True)
        _response = Response(data=serializer_ref.data, status=status.HTTP_200_OK)
    else:
        _response = Response(data=C_BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    return _response


def cust_post(_model: APIView, data: dict, *args, **kwargs):
    from util._models.company import Company

    # =======================================================
    data = data.copy()
    for element in C_FORM_POP:
        data.pop(element, None)
    if type(data) == QueryDict:
        data_dict = dict()
        for key in data.keys():
            pair = {key: data.getlist(key)[0]}
            data_dict.update(pair)
        data = data_dict
        del data_dict, pair

    serializer_ref = _model.serializer_class(data=data)
    # TODO : Get the company connection from the user data
    serializer_ref.initial_data["company"] = Company.objects._get(id=1)
    if serializer_ref.is_valid():
        serializer_ref.save()
        _response = Response(data=serializer_ref.data, status=status.HTTP_201_CREATED)
    else:
        _response = Response(data=serializer_ref.errors, status=status.HTTP_400_BAD_REQUEST)
    return _response


def cust_put(_model: APIView, data: dict, *args, **kwargs):
    data = data.copy()
    vars = cust_get_vars(_model=_model, **kwargs)
    if vars is None:
        _response = Response(data=C_BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            model_ref = _model.model.objects._filter(**vars)
            if len(model_ref) == 0:
                raise _model.model.DoesNotExist
        except _model.model.DoesNotExist:
            model_ref = None
    if model_ref is not None:
        model_ref = model_ref[0]
        data = data.copy()
        for element in C_FORM_POP:
            data.pop(element, None)
        if type(data) == QueryDict:
            data_dict = dict()
            for key in data.keys():
                pair = {key: data.getlist(key)[0]}
                data_dict.update(pair)
            data = data_dict
            del data_dict, pair
        serializer_ref = _model.serializer_class(model_ref, data=data)
        if serializer_ref.is_valid():
            serializer_ref.save()
            _response = Response(data=serializer_ref.data, status=status.HTTP_202_ACCEPTED)
        else:
            _response = Response(data=serializer_ref.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        _response = Response(data=C_BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    return _response


def cust_delete(_model: APIView, *args, **kwargs):
    vars = cust_get_vars(_model=_model, **kwargs)
    if vars is None:
        _response = Response(data=C_BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    else:
        try:
            model_ref = _model.model.objects._filter(**vars)
            if len(model_ref) == 0:
                raise _model.model.DoesNotExist
        except _model.model.DoesNotExist:
            model_ref = None
    if model_ref is not None:
        serializer_ref = _model.serializer_class(model_ref, many=True)
        model_ref = model_ref[0]
        model_ref.delete()
        _response = Response(data=serializer_ref.data, status=status.HTTP_204_NO_CONTENT)
    else:
        _response = Response(data=C_BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND)
    return _response


def cust_options(_model: APIView, request, *args, **kwargs):

    name = _model.model._meta.model_name.capitalize()
    fields = dict()
    for field in _model.model._meta.get_fields():
        if (
            field.name not in _model.serializer_class.Meta.hidden_fields
            and field.name not in _model.serializer_class.Meta.read_only_fields
            and not (isinstance(field, ManyToOneRel))  # No back reference
        ):
            fields.update({field.name: f"{field.get_internal_type()}:{getattr(field, 'max_length', None)}"})

    custom_data = {
        "description": f"This is the API for managing {name} data.",
        "allowed_methods": _model.allowed_methods,
        "fields": fields,
    }

    return Response(custom_data, status=status.HTTP_200_OK)


# ===================================================================== SERIALIZER
def cust_is_valid(_model: ModelSerializer, *args, **kwargs):
    try:
        is_valid = kwargs["is_valid"]
    except KeyError:
        is_valid = True

    # Get Unique ref stack obj
    unique_together = _model.Meta.model._meta.unique_together
    expression = str()
    if len(unique_together) > 0:
        expression = "_model.Meta.model.objects.get("
        for unique_stack in unique_together:
            for unique_field in unique_stack:
                try:
                    _model.initial_data[unique_field]
                except KeyError:
                    pass
                else:
                    try:
                        _model.initial_data[unique_field] = _model.initial_data[unique_field].upper()
                        expression = "{}{}=_model.initial_data['{}'],".format(
                            expression,
                            unique_field,
                            unique_field,
                        )
                    except Exception as e:
                        pass
        expression = "{})".format(expression[:-1])
    if len(expression) > 0:
        try:
            obj_ref = eval(expression)
        except ObjectDoesNotExist:
            obj_ref = None

    if not is_valid:
        if obj_ref is None:
            _message_01 = "Contact Administrator : email@gmail.com"
        else:
            if obj_ref.is_active:
                _message_01 = "Entry Exists"
            else:
                if not settings.DEBUG:
                    _message_01 = "Contact Administrator : email@gmail.com"
                else:
                    _message_01 = "Deleted Entry Exists"
        try:
            for error_index in range(len(_model.errors["non_field_errors"])):
                try:
                    if type(_model.errors["non_field_errors"][error_index]) == ErrorDetail:
                        if _model.errors["non_field_errors"][error_index].code == "unique":
                            _model._errors["non_field_errors"][error_index] = ErrorDetail(string=_message_01, code="admin")
                except KeyError:
                    pass
        except KeyError:
            pass

    return is_valid


def cust_to_internal_value(_model: ModelSerializer, data: dict):
    unique_together = _model.Meta.model._meta.unique_together
    if len(unique_together) > 0:
        for unique_stack in unique_together:
            for unique_field in unique_stack:
                try:
                    data[unique_field] = data[unique_field].upper()
                except KeyError:
                    pass
                except AttributeError:
                    pass
    return data


# ===================================================================== MODEL
def cust_check_save(_model: models.Model, *args, **kwargs):
    try:
        _model.full_clean()
    except IntegrityError as e:
        is_valid, messages = False, e.messages
    except ValidationError as e:
        is_valid, messages = False, e.messages
    else:
        is_valid, messages = True, None
    return is_valid, messages


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
    # ===============================

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


def validate_phone_number(value):
    pattern = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
    if re.match(pattern, value) is not None:
        return value
    else:
        raise ValidationError("Invalid Phone Number")


def validate_file_name(file_name):
    from util._models.file_type import FileType

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
    pattern = f"^[{create_random(randomize=False)}]" + "{" + f"{stlen}" + "}$"
    if len(text) == 0 or re.match(pattern, text) is not None:
        return text
    else:
        raise ValidationError("Invalid String Length")


# ===================================================================== OTHERS
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
    sha256_hash = hashlib.sha256(input_string.encode()).digest()
    _bytes = floor(bits / 8)
    sha_digest = sha256_hash[:_bytes]
    return sha_digest.hex()


def create_random(
    randomize=True,
    upper_case=True,
    lower_case=True,
    numbers=True,
    symbols=True,
    stlen=127,
):
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
