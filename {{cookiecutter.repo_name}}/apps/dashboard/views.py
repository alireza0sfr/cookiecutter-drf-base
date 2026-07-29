import json
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from apps.wallet.models import Wallet

User = get_user_model()


def dashboard_callback(request, context):
    this_week_users = User.objects.filter(
        date_joined__gte=(timezone.now() - timedelta(days=7)).date()
    ).count()
    last_week_users = (
        User.objects.filter(
            date_joined__lte=(timezone.now() - timedelta(days=7)).date(),
            date_joined__gte=(timezone.now() - timedelta(days=14)).date(),
        ).count()
        or 1
    )
    progress_users = (this_week_users / last_week_users) * 100
    progress_users = round(progress_users, 2)

    progress_text = _("progress from last week")

    wallet_balances = (
        Wallet.objects.all().aggregate(total_balance=Sum("current_balance"))[
            "total_balance"
        ]
        or 0
    )

    context.update(
        {
            "navigation": [
                # {"title": _("Dashboard"), "link": "/admin/", "active": True},
                # {"title": _("Analytics"), "link": "#"},
                # {"title": _("Settings"), "link": "#"},
            ],
            "filters": [
                # {"title": _("All"), "link": "#", "active": True},
                # {
                #     "title": _("New"),
                #     "link": "#",
                # },
            ],
            "kpi": [
                {
                    "title": _("Registered Users"),
                    "metric": this_week_users,
                    "footer": mark_safe(  # noqa: S308
                        f'<strong class="text-green-600 font-medium">+{progress_users}%</strong>&nbsp;{progress_text}'
                    ),
                    # "chart": json.dumps(
                    #     {
                    #         "labels": [WEEKDAYS[day % 7] for day in range(1, 28)],
                    #         "datasets": [{"data": average, "borderColor": "#9333ea"}],
                    #     }
                    # ),
                },
                {"title": _("Wallet Balances"), "metric": f"$ {wallet_balances}"},
            ],
            "chart": json.dumps(
                {
                    "labels": [],
                    "datasets": [
                        # {
                        #     "label": "Avg",
                        #     "type": "line",
                        #     "data": question_product_performance.get_avg(),
                        #     "backgroundColor": "#f0abfc",
                        #     "borderColor": "#f0abfc",
                        # },
                        # {
                        #     "label": "Example 3",
                        #     "data": negative,
                        #     "backgroundColor": "#f43f5e",
                        # },
                    ],
                }
            ),
        }
    )

    return context
