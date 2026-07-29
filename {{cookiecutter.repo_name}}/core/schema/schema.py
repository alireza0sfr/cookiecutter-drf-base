from drf_spectacular.openapi import AutoSchema
from drf_spectacular.plumbing import get_lib_doc_excludes


def custom_get_lib_doc_excludes():
    result = get_lib_doc_excludes()
    return result


class CustomAutoSchema(AutoSchema):
    def get_request_serializer(self):
        view = self.view

        get_input_serializer_class = getattr(view, "get_input_serializer_class", None)

        if get_input_serializer_class and callable(get_input_serializer_class):
            return get_input_serializer_class()

        return super().get_request_serializer()

    def get_response_serializers(self):
        view = self.view

        get_output_serializer_class = getattr(view, "get_output_serializer_class", None)

        if get_output_serializer_class and callable(get_output_serializer_class):
            return get_output_serializer_class()

        return super().get_response_serializers()
