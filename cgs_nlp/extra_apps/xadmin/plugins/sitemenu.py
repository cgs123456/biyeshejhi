
# pyright: reportIncompatibleMethodOverride=false
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView

BUILDIN_STYLES = {
    'default': 'xadmin/includes/sitemenu_default.html',
    'accordion': 'xadmin/includes/sitemenu_accordion.html',
}


class SiteMenuStylePlugin(BaseAdminPlugin):

    menu_style = None

    def init_request(self, *args, **kwargs):
        return bool(self.menu_style) and self.menu_style in BUILDIN_STYLES

    def get_context(self, context):
        style_key = self.menu_style or 'default'
        context['menu_template'] = BUILDIN_STYLES.get(style_key, BUILDIN_STYLES['default'])
        return context

site.register_plugin(SiteMenuStylePlugin, CommAdminView)
