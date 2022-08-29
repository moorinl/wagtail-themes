from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from wagtail.core import hooks

from wagtailthemes import views
from wagtailthemes.models import StaticFile, Template, Theme


class ThemeAdmin(ModelAdmin):
    model = Theme
    menu_label = _("Themes")
    list_display = ["name", "pathname", "created"]
    list_filter = []
    search_fields = ["name", "pathname"]


class TemplateAdmin(ModelAdmin):
    model = Template
    menu_label = _("Templates")
    list_display = ["path", "theme", "modified", "modified_by"]
    list_filter = ["theme", "modified"]
    search_fields = ["path"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.select_related("theme")
        qs.select_related("modified_by")
        return qs


class StaticFileAdmin(ModelAdmin):
    model = StaticFile
    menu_label = _("Static files")
    list_display = ["path", "theme", "modified", "modified_by"]
    list_filter = ["theme", "modified"]
    search_fields = ["path"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs.select_related("theme")
        qs.select_related("modified_by")
        return qs


class ThemeAdminGroup(ModelAdminGroup):
    menu_label = _("Themes")
    items = [
        ThemeAdmin,
        TemplateAdmin,
        StaticFileAdmin,
    ]

    def get_submenu_items(self):
        items = super().get_submenu_items()
        items.append(
            ImportExportMenuItem(
                _("Import"),
                reverse("wagtailthemes_import_theme"),
                order=3,
            )
        )
        items.append(
            ImportExportMenuItem(
                _("Export"),
                reverse("wagtailthemes_export_theme"),
                order=4,
            )
        )
        return items


modeladmin_register(ThemeAdminGroup)


class ImportExportMenuItem(MenuItem):
    def is_shown(self, request):
        return request.user.has_perm("wagtailcacheinvalidator.add_invalidationrequest")


@hooks.register("register_admin_urls")
def register_admin_urls():
    return [
        path("themes/import/", views.import_theme, name="wagtailthemes_import_theme"),
        path("themes/export/", views.export_theme, name="wagtailthemes_export_theme"),
    ]
