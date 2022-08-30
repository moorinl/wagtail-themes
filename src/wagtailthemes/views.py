import logging

from django.contrib import messages
from django.http import FileResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.translation import gettext as _
from wagtail.admin.auth import permission_required

from wagtailthemes.forms import ExportForm, ImportForm
from wagtailthemes.utils import export_theme_as_zip_file, import_theme_from_zip_file

logger = logging.getLogger(__name__)


@permission_required("wagtailthemes.add_theme")
@permission_required("wagtailthemes.add_template")
def import_theme(request):
    if request.method == "POST":
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            from wagtailthemes.wagtail_hooks import TemplateAdmin

            theme = form.cleaned_data["theme"]
            url_helper = TemplateAdmin().url_helper

            try:
                import_theme_from_zip_file(theme, form.cleaned_data["zip_file"])
            except Exception as err:
                logger.error(err)
                messages.error(request, _("Zip file is not valid."))
                return HttpResponseRedirect(reverse("wagtailthemes_import_theme"))

            messages.success(
                request,
                _(
                    "Successfully imported %s templates for theme %s."
                    % (
                        10,
                        theme.name,
                    )
                ),
            )

            return HttpResponseRedirect(url_helper.get_action_url("index"))
    else:
        form = ImportForm()

    context = {"form": form}

    return TemplateResponse(request, "wagtailthemes/import_theme.html", context)


@permission_required("wagtailthemes.view_theme")
@permission_required("wagtailthemes.view_template")
def export_theme(request):
    if request.method == "POST":
        form = ExportForm(request.POST)

        if form.is_valid():
            theme = form.cleaned_data["theme"]

            zip_file = export_theme_as_zip_file(theme)

            response = FileResponse(open(zip_file.filename, "rb"))
            return response
    else:
        form = ExportForm()

    context = {"form": form}

    return TemplateResponse(request, "wagtailthemes/export_theme.html", context)
