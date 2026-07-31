import contextlib
import copy
from typing import Any, Dict, List, Optional

from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.db import models
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html
from jalali_date import date2jalali, datetime2jalali
from jalali_date.admin import ModelAdminJalaliMixin
from jalali_date.fields import JalaliDateField, SplitJalaliDateTimeField
from jalali_date.widgets import AdminJalaliDateWidget, AdminSplitJalaliDateTime
from unfold.admin import ModelAdmin
from unfold.widgets import UnfoldBooleanSwitchWidget

from core.models import MoneyField, format_number_with_commas

overrides = {
    models.DateField: {"form_class": JalaliDateField, "widget": AdminJalaliDateWidget},
    models.DateTimeField: {"form_class": SplitJalaliDateTimeField, "widget": AdminSplitJalaliDateTime},
}


class BaseModelAdmin(ModelAdminJalaliMixin, ModelAdmin):
    list_per_page = 30
    compressed_fields = True

    class Media:
        js = ("money.js",)

    # # Override the formfield_for_dbfield method to customize DateTimeField widgets
    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if isinstance(db_field, models.BooleanField) and db_field.null is True:
            return self.formfield_for_nullboolean_field(db_field, request, **kwargs)

        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        if formfield and isinstance(formfield.widget, RelatedFieldWidgetWrapper):
            formfield.widget.template_name = "unfold/widgets/related_widget_wrapper.html"
        # Check if the field is a DateTimeField
        if isinstance(db_field, models.DateField):
            db_field.widget = JalaliDateField()

        return formfield

    def get_list_display(self, request):
        fields = super().get_list_display(request)
        read_only_fields = {*self.list_editable}

        new_fields = []
        for field in fields:
            try:
                obj_field = self.model._meta.get_field(field)
            except Exception:
                new_fields.append(field)
                continue

            if isinstance(obj_field, MoneyField) and field not in read_only_fields:
                display_field = f"{field}_money_display"

                def custom_field(obj, field=field, obj_field=obj_field):
                    return self.get_field_display(obj, field, obj_field)

                custom_field.short_description = obj_field.verbose_name
                setattr(self, display_field, custom_field)
                new_fields.append(display_field)
            else:
                new_fields.append(field)

        return new_fields

    def get_actions_detail(self, request: HttpRequest, object_id: int = None) -> List[Any]:
        return self._filter_unfold_actions_by_permissions(request, self._get_base_actions_detail())

    def get_fieldsets(self, request, obj=None):
        fieldsets = dict(super().get_fieldsets(request, obj))
        new_fieldsets = []
        read_only_fields = self.get_readonly_fields(request, obj)

        for key, value in fieldsets.items():
            fields = value.get("fields", [])
            new_fields = []
            for field in fields:
                display_field = f"{field}_display"
                if display_field in read_only_fields:
                    new_fields.append(display_field)
                else:
                    new_fields.append(field)
            fieldsets[key]["fields"] = new_fields

            new_fieldsets.append((key, {"fields": new_fields, **fieldsets[key]}))

        return new_fieldsets

    def get_readonly_fields(self, request, obj=None):
        # NOTE: we remove default read-only fields methods and change them with a custom display method to control over value and output
        #       of them

        # Retrieve readonly fields from parent and ensure custom display fields are added
        readonly_fields = super().get_readonly_fields(request, obj)

        display_fields = []
        for field in readonly_fields:
            # custom display fields on model admin don't has field on model
            try:
                obj_field = self.model._meta.get_field(field)
            except Exception:
                display_fields.append(field)
                continue

            display_field = f"{field}_display"

            def custom_field(obj, field=field, obj_field=obj_field):
                return self.get_field_display(obj, field, obj_field)

            custom_field.short_description = obj_field.verbose_name
            setattr(self, display_field, custom_field)

            display_fields.append(display_field)

        if "slug" not in readonly_fields and hasattr(self.model, "slug"):
            display_fields.append("slug")

        return display_fields

    def get_field_display(self, obj, field_name, db_field):
        value = getattr(obj, field_name, None)
        if isinstance(db_field, models.DateTimeField):
            strftime = settings.JALALI_DATE_DEFAULTS["Strftime"]["datetime"]
            value = datetime2jalali(value).strftime(strftime)
        elif isinstance(db_field, models.DateField):
            strftime = settings.JALALI_DATE_DEFAULTS["Strftime"]["date"]
            value = date2jalali(value).strftime(strftime)
        elif isinstance(db_field, MoneyField):
            value = format_number_with_commas(value)
        return format_html("<span>{}</span>", value if type(value) is not None else "-")

    def changeform_view(
        self,
        request: HttpRequest,
        object_id: Optional[str] = None,
        form_url: str = "",
        extra_context: Optional[Dict[str, bool]] = None,
    ) -> Any:
        if extra_context is None:
            extra_context = {}

        new_formfield_overrides = copy.deepcopy(self.formfield_overrides)
        new_formfield_overrides.update({models.BooleanField: {"widget": UnfoldBooleanSwitchWidget}})

        self.formfield_overrides = new_formfield_overrides

        actions = []
        if object_id:
            for action in self.get_actions_detail(request, object_id):
                if not hasattr(action.method, "attrs"):
                    raise AttributeError(f"Action {action.description} does not have 'attrs' attribute.")
                actions.append(
                    {
                        "title": action.description,
                        "attrs": action.method.attrs,
                        "path": reverse(f"admin:{action.action_name}", args=(object_id,)),
                    }
                )

        with contextlib.suppress(Exception):
            extra_context.update(
                {"actions_submit_line": self.get_actions_submit_line(request, object_id), "actions_detail": actions}
            )

        return super(ModelAdmin, self).changeform_view(request, object_id, form_url, extra_context)
