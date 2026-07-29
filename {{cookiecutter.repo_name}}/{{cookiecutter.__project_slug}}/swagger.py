from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

schema_view = SpectacularAPIView.as_view()
swagger_ui_view = SpectacularSwaggerView.as_view(url_name="schema")
redoc_view = SpectacularRedocView.as_view(url_name="schema")
