from django.conf import settings
from rest_framework.throttling import UserRateThrottle
from core.utils.ip import IPService


class CustomRateThrottle(UserRateThrottle):
    scope_attr = "throttle_scope"

    THROTTLE_RATES = {
        "crucial": "10/hour",
        "high": "20/min",
        "medium": "25/min",
        "low": "35/min",
    }

    def get_rate(self):
        if settings.DEBUG:
            return "1000/hour"

        scope = getattr(self.view, self.scope_attr, None)
        if scope is None:
            return None

        try:
            return self.THROTTLE_RATES.get(scope, "35/min")
        except AttributeError:
            return None

    def throttle_success(self):
        ip_whitelist = getattr(settings, "IP_WHITELIST", [])
        client_ip = IPService.get_client_ip(self.request)

        if client_ip in ip_whitelist:
            return True

        return super().throttle_success()
