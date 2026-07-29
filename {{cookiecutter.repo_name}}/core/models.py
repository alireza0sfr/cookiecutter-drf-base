import locale
import secrets
import string

from django import forms
from django.core.cache import cache
from django.db import models
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django_lifecycle import LifecycleModelMixin, hook, hooks
from unfold.widgets import BASE_INPUT_CLASSES, UnfoldAdminDecimalFieldWidget

from .http import get_client_ip



class BaseModel(LifecycleModelMixin, models.Model):
    created_at = models.DateTimeField(verbose_name=_("Created At"), auto_now_add=True, null=True)

    @hook(hooks.BEFORE_SAVE)
    def auto_generate_slug_on_save(self):
        if hasattr(self, "slug"):
            title = getattr(self, "title", str(self))
            self.slug = slugify(f"{title}", allow_unicode=True)
            while self.__class__.objects.filter(slug=self.slug).exists():
                random_number = "".join([secrets.choice(string.digits) for _ in range(secrets.choice([3, 4, 5, 6]))])
                self.slug = slugify(f"{title}-{random_number}", allow_unicode=True)

    class Meta:
        abstract = True


class AnalyticsBaseModel(models.Model):
    """
    Analytics Base Model
    methods:
        - sey_view: plus view to object and cache ip and object_id with action in redis for 10 minutes
        - set_like: plus like to object and cache ip and object_id with action in redis for 60 minutes
        - set_dislike: plus dislike in object and cache ip and object_id with action in redis for 60 minutes
    """

    views_count = models.IntegerField(_("view count"), default=0, blank=True, editable=False)

    class Meta:
        abstract = True

    @property
    def _key(self):
        """
        Returns cached key
        """
        return "%s_%s_%s" % (self._meta.app_label, self._meta.model_name, self.id)

    def set_view(self, request, force=False):
        # set view per ip
        ip = get_client_ip(request)
        key = "av_%s_%s" % (self._key, ip)
        if force or not cache.get(key):
            # its force or cache is not set
            self.views_count += 1
            self.save()
            cache.set(key, True, 60 * 10)
            return True

        return False


def format_number_with_commas(number):
    # Set the locale to the user's default setting (usually used for commas and periods in numbers)
    try:
        # Convert the number to a float
        number_float = float(number)
        # Use locale to format the number with commas as thousand separators
        return locale.format_string("%f", number_float, grouping=True, monetary=False).rstrip("0").rstrip(".")
    except ValueError:
        # If the value is not a valid number, return the original input
        return number
    except TypeError:
        return None


class UnfoldMoneyWidget(UnfoldAdminDecimalFieldWidget):
    input_type = "text"

    def __init__(self, attrs=None) -> None:
        custom_class = [
            "input-money",
        ]
        super().__init__(
            attrs={"style": "min-width: 98px", "class": " ".join(BASE_INPUT_CLASSES + custom_class), **(attrs or {})}
        )

    def format_value(self, value) -> str | None:
        value = super().format_value(value)
        value = format_number_with_commas(value)
        return value

    def value_from_datadict(self, data, files, name):
        value = super().value_from_datadict(data, files, name) or ""
        return value.replace(",", "")


class MoneyWrapperWidget(forms.DecimalField):
    def __init__(self, *args, **kwargs) -> None:
        kwargs["widget"] = UnfoldMoneyWidget
        super().__init__(*args, **kwargs)

    # def prepare_value(self, value):
    #     return ""


class MoneyField(models.DecimalField):
    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "max_digits": self.max_digits,
                "decimal_places": self.decimal_places,
                "form_class": MoneyWrapperWidget,
                **kwargs,
            }
        )
