from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


UNFOLD = {
    "DASHBOARD_CALLBACK": "apps.dashboard.views.dashboard_callback",
    "ENVIRONMENT": "apps.dashboard.utils.environment_callback",
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
    # # "SITE_LOGO": lambda request: static("dashboard/images/logo.svg"),  # both modes, optimise for 32px height
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
    "TABS": [
        {
            "models": ["messaging.group", "messaging.groupuser"],
            "items": [
                {"title": _("Groups"), "icon": "article", "link": reverse_lazy("admin:messaging_group_changelist")},
                {"title": _("Group Users"), "icon": "article", "link": reverse_lazy("admin:messaging_groupuser_changelist")},
            ],
        },
    ],
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": False,  # Top border
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",  # Supported icon set: https://fonts.google.com/icons
                        "link": reverse_lazy("admin:index"),
                        # "badge": "sample_app.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                ],
            },
                  {
                "title": _("account management"),
                "separator": True,
                "items": [
                    {
                        "title": _("Admin Users"),
                        "icon": "shield_person",
                        "link": reverse_lazy("admin:account_adminuserproxy_changelist"),
                    },
                    {
                        "title": _("Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_normaluserproxy_changelist"),
                    },
                    {
                        "title": _("New Users"),
                        "icon": "person",
                        "link": reverse_lazy("admin:account_newuserproxy_changelist"),
                        "badge": "apps.account.utils.new_user_badge_callback",
                    },
                ],
            },
            {
                "title": _("Wallet Management"),
                "separator": False,
                "items": [
                    {"title": _("Wallets"), "icon": "wallet", "link": reverse_lazy("admin:wallet_wallet_changelist")},
                    {
                        "title": _("Transactions"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:wallet_wallettransaction_changelist"),
                    },
                ],
            },
            {
                "title": _("Messaging"),
                "separator": False,
                "items": [
                    {"title": _("Groups"), "icon": "groups", "link": reverse_lazy("admin:messaging_group_changelist")},
                    {
                        "title": _("Group Messages"),
                        "icon": "cell_tower",
                        "link": reverse_lazy("admin:messaging_groupmessage_changelist"),
                    },
                    {
                        "title": _("User Messages"),
                        "icon": "sms",
                        "link": reverse_lazy("admin:messaging_usermessage_changelist"),
                    },
                ],
            },
        ],
    },
    "STYLES": [],
    "SCRIPTS": [],
}
