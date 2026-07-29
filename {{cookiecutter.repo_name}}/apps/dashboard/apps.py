import re
import unicodedata

from django.apps import AppConfig
from django.template import defaultfilters
from django.template.defaultfilters import register, stringfilter
from django.utils import text
from django.utils.functional import keep_lazy_text
from jalali_date.admin import ModelAdminJalaliMixin


@keep_lazy_text
def myslugify(value, allow_unicode=True):
    """
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


@register.filter(is_safe=True)
@stringfilter
def slugify(value):
    """
    Convert to ASCII. Convert spaces to hyphens. Remove characters that aren't
    alphanumerics, underscores, or hyphens. Convert to lowercase. Also strip
    leading and trailing whitespace.
    """
    return myslugify(value)


class DashboardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.dashboard"

    def ready(self) -> None:
        text.slugify = myslugify
        defaultfilters.slugify = slugify

        del ModelAdminJalaliMixin.change_form_template
