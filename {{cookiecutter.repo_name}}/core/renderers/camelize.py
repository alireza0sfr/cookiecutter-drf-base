from rest_framework.renderers import JSONRenderer
from rest_framework_camel_case.render import CamelCaseJSONRenderer


class CamelizeRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        renderer_context = renderer_context or {}
        response = renderer_context.get("response")
        status_code = response.status_code if response else 200

        if isinstance(data, dict):
            if "key" in data and "errors" in data:
                camelized_data = CamelCaseJSONRenderer().render(
                    data.get("data", {}), accepted_media_type, renderer_context
                )
                response_data = {
                    "success": data.get("success", status_code < 400),
                    "code": status_code,
                    "message": data.get("message", ""),
                    "key": data.get("key", ""),
                    "errors": data.get("errors", {}),
                    "data": camelized_data,
                }
            else:
                camelized_data = CamelCaseJSONRenderer().render(
                    data, accepted_media_type, renderer_context
                )
                response_data = {
                    "success": status_code < 400,
                    "code": status_code,
                    "message": "",
                    "key": "",
                    "errors": {},
                    "data": camelized_data,
                }
        else:
            response_data = {
                "success": status_code < 400,
                "code": status_code,
                "message": "",
                "key": "",
                "errors": {},
                "data": data,
            }

        return super().render(response_data, accepted_media_type, renderer_context)
