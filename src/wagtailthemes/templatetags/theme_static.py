import os.path
from django import template
from django.conf import settings
from django.templatetags.static import StaticNode
from wagtailthemes.models import ThemeSettings

register = template.Library()

class ThemeStaticNode(StaticNode):
    def url(self, context):
        path = self.path.resolve(context)
        theme_settings = ThemeSettings.for_site(context.request.site)
        if theme_settings.theme:
            theme_path = getattr(settings, 'WAGTAIL_THEME_PATH', "")
            path = os.path.join(theme_path, theme_settings.theme, path)
        return self.handle_simple(path)

@register.tag('theme_static')
def do_theme_static(parser, token):
    """
    Works just like the standard Django static tag, but when a theme is active,
    it will also prefix the theme path.  E.g. If the theme brand is active
    {% theme_static img/logo.png %} will give /static/theme/brand/img/logo.png
    but if no theme was active it'd just give /static/img/logo.png
    """
    return ThemeStaticNode.handle_token(parser, token)

