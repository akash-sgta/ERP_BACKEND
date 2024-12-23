# ===================================================================

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
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.response import Response
from rest_framework import status
from django.db.models import ManyToOneRel

# ===================================================================


class Custom:
    """
    A custom utility class for handling common operations in Django REST framework views.
    """

    BLANK_RESPONSE = ReturnList([], serializer=None)
    FORM_POP = ("csrfmiddlewaretoken",)
    KEYS_FOR_URL = ("id",)
    COMPANY = "company"
    USER = "_user_"
    IS_VALID = "is_valid"
    DEFAULT = "default"
    DEL_FLAG = "del_flag"
    CUSTOM_APPS = tuple("patient,profile,staff,util".split(","))
    FORCED = "forced"

    def cust_get_vars(self, model_ref: APIView = None, **kwargs):
        """
        Retrieves variables from the keyword arguments based on predefined keys.

        Args:
            model_ref (APIView): The API view reference.
            **kwargs: Additional keyword arguments.

        Returns:
            dict: A dictionary containing the retrieved variables.
        """
        data = dict()
        for key in self.KEYS_FOR_URL:
            try:
                if kwargs[key] == "":
                    raise KeyError
                data.update({key: kwargs[key]})
            except KeyError:
                pass
        if len(data) == 0:
            data = None

        return data

    def cust_fetch_company(self, *args, **kwargs):
        """
        Fetches the company associated with the user from the provided keyword arguments.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Company: The company instance if found, otherwise None.
        """
        from profile._models.profile import Profile
        from util._models.company import Company

        try:
            profile_ref = Profile.objects.get(
                user__username=kwargs[self.USER]
            )
            kwargs[self.COMPANY] = Company.objects.get_(
                id=profile_ref.company.id
            )
        except KeyError:
            kwargs[self.COMPANY] = None
        except ObjectDoesNotExist:
            kwargs[self.COMPANY] = None

        return kwargs[self.COMPANY]

    def cust_get(self, model_ref: APIView, *args, **kwargs):
        """
        Handles GET requests for the specified model.

        Args:
            model_ref (APIView): The API view reference.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response with the retrieved data or a blank response if not found.
        """
        vars = model_ref.get_vars(**kwargs)
        if vars is None:
            model_ref = model_ref.model.objects.all_()
        else:
            try:
                model_ref = model_ref.model.objects.filter_(**vars)
                if len(model_ref) == 0:
                    raise model_ref.model.DoesNotExist
            except model_ref.model.DoesNotExist:
                model_ref = None
        if model_ref is not None:
            serializer_ref = model_ref.serializer_class(model_ref, many=True)
            _response = Response(
                data=serializer_ref.data, status=status.HTTP_200_OK
            )
        else:
            _response = Response(
                data=self.BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND
            )

        return _response

    def cust_post(self, model_ref: APIView, data: dict, *args, **kwargs):
        """
        Handles POST requests for the specified model.

        Args:
            model_ref (APIView): The API view reference.
            data (dict): The data to be posted.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response with the posted data or errors if invalid.
        """
        data = data.copy()
        for element in self.FORM_POP:
            data.pop(element, None)
        if type(data) == QueryDict:
            data_dict = dict()
            for key in data.keys():
                pair = {key: data.getlist(key)[0]}
                data_dict.update(pair)
            data = data_dict
            del data_dict, pair

        data.update({self.COMPANY: kwargs[self.COMPANY]})
        data.update({self.USER: kwargs[self.USER]})

        serializer_ref = model_ref.serializer_class(data=data)

        if serializer_ref.is_valid():
            serializer_ref.save()
            _response = Response(
                data=serializer_ref.data, status=status.HTTP_201_CREATED
            )
        else:
            _response = Response(
                data=serializer_ref.errors, status=status.HTTP_400_BAD_REQUEST
            )

        return _response

    def cust_put(self, model_ref: APIView, data: dict, *args, **kwargs):
        """
        Handles PUT requests for the specified model.

        Args:
            model_ref (APIView): The API view reference.
            data (dict): The data to be updated.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response with the updated data or errors if invalid.
        """
        data = data.copy()
        vars = self.cust_get_vars(model_ref=model_ref, **kwargs)
        if vars is None:
            _response = Response(
                data=self.BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND
            )
        else:
            try:
                model_ref = model_ref.model.objects.filter_(**vars)
                if len(model_ref) == 0:
                    raise model_ref.model.DoesNotExist
            except model_ref.model.DoesNotExist:
                model_ref = None
        if model_ref is not None:
            model_ref = model_ref[0]
            data = data.copy()
            for element in self.FORM_POP:
                data.pop(element, None)
            if type(data) == QueryDict:
                data_dict = dict()
                for key in data.keys():
                    pair = {key: data.getlist(key)[0]}
                    data_dict.update(pair)
                data = data_dict
                del data_dict, pair
            serializer_ref = model_ref.serializer_class(model_ref, data=data)
            if serializer_ref.is_valid():
                serializer_ref.save()
                _response = Response(
                    data=serializer_ref.data, status=status.HTTP_202_ACCEPTED
                )
            else:
                _response = Response(
                    data=serializer_ref.errors,
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            _response = Response(
                data=self.BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND
            )

        return _response

    def cust_delete(self, model_ref: APIView, *args, **kwargs):
        """
        Handles DELETE requests for the specified model.

        Args:
            model_ref (APIView): The API view reference.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response confirming the deletion or a blank response if not found.
        """
        vars = self.cust_get_vars(model_ref=model_ref, **kwargs)
        if vars is None:
            _response = Response(
                data=self.BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND
            )
        else:
            try:
                db_model_ref = model_ref.model.objects.filter_(**vars)
                if len(db_model_ref) == 0:
                    raise db_model_ref.model.DoesNotExist
            except db_model_ref.model.DoesNotExist:
                db_model_ref = None
        if db_model_ref is not None:
            serializer_ref = model_ref.serializer_class(
                db_model_ref, many=True
            )
            for db_model_ref_ in db_model_ref:
                db_model_ref_.delete()
            _response = Response(
                data=serializer_ref.data, status=status.HTTP_204_NO_CONTENT
            )
        else:
            _response = Response(
                data=self.BLANK_RESPONSE, status=status.HTTP_404_NOT_FOUND
            )

        return _response

    def cust_options(self, model_ref: APIView, request, *args, **kwargs):
        """
        Handles OPTIONS requests to describe the API for managing a model's data.

        Args:
            model_ref (APIView): The API view reference.
            request: The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The HTTP response with API description and allowed methods.
        """
        name = model_ref.model._meta.model_name.capitalize()
        fields = dict()
        for field in model_ref.model._meta.get_fields():
            if (
                field.name
                not in model_ref.serializer_class.Meta.hidden_fields
                and field.name
                not in model_ref.serializer_class.Meta.read_only_fields
                and not (isinstance(field, ManyToOneRel))  # No back reference
            ):
                fields.update(
                    {
                        field.name: f"{field.get_internal_type()}:{getattr(field, 'max_length', None)}"
                    }
                )

        custom_data = {
            "description": f"This is the API for managing {name} data.",
            "allowed_methods": model_ref.allowed_methods,
            "fields": fields,
        }

        return Response(custom_data, status=status.HTTP_200_OK)

    # ==================== SERIALIZER ====================
    def cust_is_valid(self, model_ref: ModelSerializer, *args, **kwargs):
        try:
            is_valid = kwargs[self.IS_VALID]
        except KeyError:
            is_valid = True

        # Get Unique ref stack obj
        unique_together = model_ref.Meta.model._meta.unique_together
        expression = str()
        if len(unique_together) > 0:
            expression = "model_ref.Meta.model.objects.get("
            for unique_stack in unique_together:
                for unique_field in unique_stack:
                    try:
                        model_ref.initial_data[unique_field]
                    except KeyError:
                        pass
                    else:
                        try:
                            model_ref.initial_data[unique_field] = (
                                model_ref.initial_data[unique_field].upper()
                            )
                            expression = (
                                "{}{}=model_ref.initial_data['{}'],".format(
                                    expression,
                                    unique_field,
                                    unique_field,
                                )
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
                        _message_01 = (
                            "Contact Administrator : email@gmail.com"
                        )
                    else:
                        _message_01 = "Deleted Entry Exists"
            try:
                for error_index in range(
                    len(model_ref.errors["non_field_errors"])
                ):
                    try:
                        if (
                            type(
                                model_ref.errors["non_field_errors"][
                                    error_index
                                ]
                            )
                            == ErrorDetail
                        ):
                            if (
                                model_ref.errors["non_field_errors"][
                                    error_index
                                ].code
                                == "unique"
                            ):
                                model_ref._errors["non_field_errors"][
                                    error_index
                                ] = ErrorDetail(
                                    string=_message_01, code="admin"
                                )
                    except KeyError:
                        pass
            except KeyError:
                pass

        return is_valid

    def cust_to_internal_value(self, model_ref: ModelSerializer, data: dict):
        unique_together = model_ref.Meta.model._meta.unique_together
        if len(unique_together) > 0:
            for unique_stack in unique_together:
                for unique_field in unique_stack:
                    try:
                        data[unique_field] = data[unique_field].upper()
                    except KeyError:
                        pass
                    except AttributeError:
                        pass
        # TODO : Update here

        return data

    # ==================== MODEL ====================
    def cust_check_save(self, model_ref: models.Model, *args, **kwargs):
        try:
            model_ref.full_clean()
        except IntegrityError as e:
            is_valid, messages = False, e.messages
        except ValidationError as e:
            is_valid, messages = False, e.messages
        else:
            is_valid, messages = True, None

        return is_valid, messages

    def update_change_log(self, model_ref: models.Model, *args, **kwargs):
        try:
            model_ref.changedBy = kwargs[self.USER]
        except KeyError:
            model_ref.changedBy = self.DEFAULT
        finally:
            model_ref.changedBy = model_ref.changedBy.upper()

        if model_ref.pk is None:
            model_ref.createdBy = model_ref.changedBy

        return model_ref.changedBy

    def update_active_status(self, model_ref: models.Model, *args, **kwargs):
        is_active_old = model_ref.is_active
        is_active_new = model_ref.is_active

        try:
            kwargs[self.DEL_FLAG]
        except KeyError:
            pass
        else:
            if kwargs[self.DEL_FLAG]:
                is_active_new = False
            else:
                is_active_new = True

        model_ref.is_active = is_active_new

        return is_active_old, is_active_new

    def get_related_model_refs(
        self,
        model_ref: models.Model,
        on_delete_behaviour=models.CASCADE,
        *args,
        **kwargs,
    ):
        related_model_refs = dict()
        custom_model_refs = list(
            model
            for model in apps.getmodel_refs()
            if model._meta.app_label in self.CUSTOM_APPS
        )
        for model in custom_model_refs:
            related_model_refs.update({model: list()})
            for field in model._meta.get_fields():
                if (
                    isinstance(field, models.ForeignKey)
                    and field.remote_field.model == model_ref.__class__
                    and field.remote_field.on_delete == on_delete_behaviour
                ):
                    related_model_refs[model].append(field.name)

        return related_model_refs

    def update_reference_objects(
        self, model_ref: models.Model, *args, **kwargs
    ):
        related_model_refs = self.get_related_model_refs(
            model_ref, *args, **kwargs
        )
        for related_model_ref in related_model_refs.keys():
            if len(related_model_refs[related_model_ref]) > 0:
                expression = "related_model_ref.objects.filter({}=model_ref.pk)".format(
                    related_model_refs[related_model_ref][0]
                )
                try:
                    related_refs = eval(expression)
                    if len(related_refs) == 0:
                        raise related_model_ref.DoesNotExist
                except related_model_ref.DoesNotExist:
                    pass
                except IndexError:
                    pass
                else:
                    for related_ref in related_refs:
                        if model_ref.is_active:
                            related_ref.save()
                        else:
                            related_ref.delete()

        return None

    def validate_phone_number(self, value):
        pattern = r"^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$"
        if re.match(pattern, value) is not None:
            pass
        else:
            raise ValidationError("Invalid Phone Number")

        return value

    def validate_file_name(self, file_name):
        from util._models.file_type import FileType

        file_name = file_name.split(".")
        if len(file_name) < 2:
            raise ValidationError("Invalid File Name")
        else:
            try:
                file_ref = FileType.objects.get(code=file_name[1])
            except FileType.DoesNotExist:
                file_ref = FileType.objects.create(code=file_name[1])

        return file_name[0], file_ref

    def validate_string_len(self, text, stlen=15):
        pattern = (
            f"^[{self.create_random(randomize=False)}]"
            + "{"
            + f"{stlen}"
            + "}$"
        )
        if len(text) == 0 or re.match(pattern, text) is not None:
            return text
        else:
            raise ValidationError("Invalid String Length")

    # ==================== OTHERS ====================
    def create_new_key(self, model_ref: models.Model, field_name: str):
        key = None
        try:
            while True:
                try:
                    key = self.create_random(
                        symbols=False,
                        lower_case=False,
                    )
                    exec("model_ref.objects.get({}=key)".format(field_name))
                except model_ref.DoesNotExist:
                    break
        except Exception:
            key = None

        return key

    def sha(self, input_string, bits=256):
        sha256_hash = hashlib.sha256(input_string.encode()).digest()
        _bytes = floor(bits / 8)
        sha_digest = sha256_hash[:_bytes]

        return sha_digest.hex()

    def create_random(
        self,
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
