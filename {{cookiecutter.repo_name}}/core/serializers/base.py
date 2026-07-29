from enum import Enum
from rest_framework import serializers


class EnumSerializerField(serializers.Field):
    def __init__(self, enum_class, **kwargs):
        super().__init__(**kwargs)
        self.enum_class = enum_class

    def to_representation(self, value):
        if isinstance(value, Enum):
            return {"key": value.name, "value": value.value}
        return {"key": value, "value": value}

    def to_internal_value(self, data):
        if isinstance(data, dict):
            key = data.get("key")
        else:
            key = data

        try:
            return self.enum_class[key]
        except KeyError:
            self.fail("invalid", input=key)


class KeyPairSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.CharField()
