#coding:utf-8
# pyright: reportIncompatibleMethodOverride=false, reportAttributeAccessIssue=false
from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, CommAdminView


class MobilePlugin(BaseAdminPlugin):

    def _test_mobile(self):
        try:
            user_agent = self.admin_view.request.META.get('HTTP_USER_AGENT', '')
            return user_agent.find('Android') >= 0 or user_agent.find('iPhone') >= 0
        except Exception:
            return False

    def init_request(self, *args, **kwargs):
        return self._test_mobile()

    def get_context(self, context):
        #context['base_template'] = 'xadmin/base_mobile.html'
        context['is_mob'] = True
        return context

    # Media
    # def get_media(self, media):
    #     return media + self.vendor('xadmin.mobile.css', )

    def block_extrahead(self, context, nodes):
        nodes.append('<script>window.__admin_ismobile__ = true;</script>')

site.register_plugin(MobilePlugin, CommAdminView)
