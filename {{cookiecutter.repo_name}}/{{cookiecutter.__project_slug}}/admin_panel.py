from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "DASHBOARD_CALLBACK": "apps.dashboard.views.dashboard_callback",
    "ENVIRONMENT": "apps.dashboard.utils.environment_callback",
    # Uncomment and customize these settings as needed:
    # "COLORS": {
    #     "primary": {
    #         "50": "250 245 255",
    #         "100": "243 232 255",
    #         "200": "233 213 255",
    #         "300": "216 180 254",
    #         "400": "40 180 99",
    #         "500": "40 180 99",
    #         "600": "40 180 99",
    #         "700": "126 34 206",
    #         "800": "107 33 168",
    #         "900": "88 28 135",
    #         "950": "59 7 100",
    #     },
    # },
    # "SITE_ICON": {
    #     "light": lambda request: static("dashboard/images/icon.svg"),  # light mode
    #     "dark": lambda request: static("dashboard/images/icon.svg"),  # dark mode
    # },
    # "SITE_LOGO": {
    #     "light": lambda request: static("dashboard/images/logo.svg"),  # light mode
    #     "dark": lambda request: static("dashboard/images/logo.svg"),  # dark mode
    # },
    # "SITE_SYMBOL": "speed",  # symbol from icon set
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/ico+xml",
    #         "href": lambda request: static("favicon.ico"),
    #     },
    # ],
    # Add your custom tabs here
    # Example:
    # "TABS": [
    #     {
    #         "models": ["myapp.mymodel"],
    #         "items": [
    #             {"title": _("My Model"), "icon": "article", "link": reverse_lazy("admin:myapp_mymodel_changelist")},
    #         ],
    #     },
    # ],
    "TABS": [],
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": True,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
            # Add your custom sidebar sections here
            # Example:
            # {
            #     "title": _("Accounts"),
            #     "separator": True,
            #     "items": [
            #         {
            #             "title": _("Users"),
            #             "icon": "person",
            #             "link": reverse_lazy("admin:auth_user_changelist"),
            #         },
            #     ],
            # },
        ],
    },
    "STYLES": [],
    "SCRIPTS": [],
}
