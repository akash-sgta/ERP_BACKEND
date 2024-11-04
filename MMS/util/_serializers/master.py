# =====================================================================
from util._serializers.change_log import ChangeLog as Serializer
from util._models.master import Master as Model

# =====================================================================


class ChangeLog(Serializer):
    class Meta:
        model = Model
        _hidden_fields = Serializer._hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in _hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer._read_only_fields + ()

    def to_internal_value(self, data, *args, **kwargs):
        unique_together = self.Meta.model._meta.unique_together
        if len(unique_together) > 0:
            for unique_stack in unique_together:
                for unique_field in unique_stack:
                    try:
                        data[unique_field] = data[unique_field].upper()
                    except KeyError:
                        pass
        return super(ChangeLog, self).to_internal_value(data, *args, **kwargs)

    def is_valid(self, *args, **kwargs):
        # Get Unique ref stack obj
        unique_together = self.Meta.model._meta.unique_together
        expression = str()
        if len(unique_together) > 0:
            expression = "self.Meta.model.objects.get("
            for unique_stack in unique_together:
                for unique_field in unique_stack:
                    try:
                        self.initial_data[unique_field]
                    except KeyError:
                        pass
                    else:
                        try:
                            self.initial_data[unique_field] = self.initial_data[unique_field].upper()
                            expression = "{}{}=self.initial_data['{}'],".format(
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

        is_valid = super(ChangeLog, self).is_valid(*args, **kwargs)

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
            for error_index in range(len(self.errors["non_field_errors"])):
                try:
                    if type(self.errors["non_field_errors"][error_index]) == ErrorDetail:
                        if self.errors["non_field_errors"][error_index].code == "unique":
                            self._errors["non_field_errors"][error_index] = ErrorDetail(string=_message_01, code="admin")
                except KeyError:
                    pass

        return is_valid
