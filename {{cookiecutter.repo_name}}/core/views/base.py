from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from core.utils.context import AppContext
from core.exceptions.exceptions import PermissionDeniedException, NotAuthenticatedException


class BaseViewSet(ModelViewSet):
    """Base viewset with input/output serializer support"""

    def get_input_serializer_class(self):
        return self.get_serializer_class()

    def get_output_serializer_class(self):
        return self.get_serializer_class()

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_input_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)


class BaseAPIView(APIView):
    """Base API view with context support"""

    def initialize_request(self, request, *args, **kwargs):
        request = super().initialize_request(request, *args, **kwargs)
        AppContext.set("request", request)
        AppContext.set("view", self)
        return request

    def permission_denied(self, request, message=None):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticatedException(detail=message)
        raise PermissionDeniedException(detail=message)
