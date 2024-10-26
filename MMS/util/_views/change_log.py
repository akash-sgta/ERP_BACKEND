# =====================================================================
from django.db import models
from django.http import QueryDict
from django.template.response import TemplateResponse
from rest_framework.generics import GenericAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from util._models.change_log import ChangeLog as Model
from util._models.continent import Continent
from util._serializers.change_log import ChangeLog as Serializer
from django.db.models import ForeignKey, ManyToOneRel, ManyToManyRel
from rest_framework import serializers


# =====================================================================


class ChangeLog(APIView):
    _status = status
    _Response = Response
    _TemplateResponse = TemplateResponse
    _TemplateHTMLRenderer = TemplateHTMLRenderer
    _JSONRenderer = JSONRenderer
    _pop = ("csrfmiddlewaretoken",)
    _keys = ("id",)
    _blank_return = ReturnList([], serializer=None)
    allowed_methods = "GET,POST,UPDATE,DELETE,OPTIONS".split(",")

    serializer_class = Serializer
    model = Model

    def _get_vars(self, **kwargs):
        data = dict()
        for key in self._keys:
            try:
                if kwargs[key] == "":
                    raise KeyError
                data[key] = kwargs[key]
            except KeyError:
                pass
        if len(data) == 0:
            data = None
        return data

    def get(self, request, *args, **kwargs):
        vars = self._get_vars(**kwargs)
        if vars is None:
            model_ref = self.model.objects._all()
        else:
            try:
                model_ref = self.model.objects._filter(**vars)
                if len(model_ref) == 0:
                    raise self.model.DoesNotExist
            except self.model.DoesNotExist:
                model_ref = None
        if model_ref is not None:
            serializer_ref = self.serializer_class(model_ref, many=True)
            return self._Response(data=serializer_ref.data, status=self._status.HTTP_200_OK)
        else:
            return self._Response(data=self._blank_return, status=self._status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        for element in self._pop:
            data.pop(element, None)
        if type(data) == QueryDict:
            data_dict = dict()
            for key in data.keys():
                pair = {key: data.getlist(key)[0]}
                data_dict.update(pair)
            data = data_dict
            del data_dict, pair
        serializer_ref = self.serializer_class(data=data)
        if serializer_ref.is_valid():
            serializer_ref.save()
            return self._Response(data=serializer_ref.data, status=self._status.HTTP_201_CREATED)
        else:
            return self._Response(data=serializer_ref.errors, status=self._status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        data = request.data.copy()
        vars = self._get_vars(**kwargs)
        if vars is None:
            return self._Response(data=self._blank_return, status=self._status.HTTP_404_NOT_FOUND)
        else:
            try:
                model_ref = self.model.objects._filter(**vars)
                if len(model_ref) == 0:
                    raise self.model.DoesNotExist
            except self.model.DoesNotExist:
                model_ref = None
        if model_ref is not None:
            model_ref = model_ref[0]
            data = request.data.copy()
            for element in self._pop:
                data.pop(element, None)
            if type(data) == QueryDict:
                data_dict = dict()
                for key in data.keys():
                    pair = {key: data.getlist(key)[0]}
                    data_dict.update(pair)
                data = data_dict
                del data_dict, pair
            serializer_ref = self.serializer_class(model_ref, data=data)
            if serializer_ref.is_valid():
                serializer_ref.save()
                return self._Response(data=serializer_ref.data, status=self._status.HTTP_202_ACCEPTED)
            else:
                return self._Response(data=serializer_ref.errors, status=self._status.HTTP_400_BAD_REQUEST)
        else:
            return self._Response(data=self._blank_return, status=self._status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        vars = self._get_vars(**kwargs)
        if vars is None:
            return self._Response(data=self._blank_return, status=self._status.HTTP_404_NOT_FOUND)
        else:
            try:
                model_ref = self.model.objects._filter(**vars)
                if len(model_ref) == 0:
                    raise self.model.DoesNotExist
            except self.model.DoesNotExist:
                model_ref = None
        if model_ref is not None:
            serializer_ref = self.serializer_class(model_ref, many=True)
            model_ref = model_ref[0]
            model_ref.delete()
            return self._Response(data=serializer_ref.data, status=self._status.HTTP_204_NO_CONTENT)
        else:
            return self._Response(data=self._blank_return, status=self._status.HTTP_404_NOT_FOUND)

    def options(self, request, *args, **kwargs):
        response = super().options(request, *args, **kwargs)

        name = self.model._meta.model_name.capitalize()
        fields = dict()
        for field in self.model._meta.get_fields():
            if (
                field.name not in self.serializer_class.Meta._hidden_fields
                and field.name not in self.serializer_class.Meta.read_only_fields
                and not (isinstance(field, ManyToOneRel))  # No back reference
            ):
                fields.update({field.name: f"{field.get_internal_type()}:{getattr(field, 'max_length', None)}"})

        custom_data = {
            "description": f"This is the API for managing {name} data.",
            "allowed_methods": self.allowed_methods,
            "fields": fields,
        }
        response.data.update(custom_data)

        return self._Response(response.data, status=self._status.HTTP_200_OK)
