from core.utils.context import AppContext


class AppContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            AppContext.set("request", request)
            response = self.get_response(request)
        finally:
            AppContext.clear()
        return response
