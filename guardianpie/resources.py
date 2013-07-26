import logging

from tastypie.resources import ModelResource
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.utils import trailing_slash
from surlex.dj import surl

logger = logging.getLogger(__name__)


class PermissionResource(ModelResource):
    """

    """
    class Meta:
        resource_name = 'permission'
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        urlargs = {'name': resource_name, 'slash': trailing_slash()}

    def override_urls(self):
        return [
            surl(r"^<resource_name={name}>/model/<applabel:s>/<model:s>{slash}$".format(**self._meta.urlargs), self.wrap_view('get_object_list'), name="api_getlist"),
            surl(r"^<resource_name={name}>/model/<applabel:s>/<model:s>/<pk:#>{slash}$".format(**self._meta.urlargs), self.wrap_view('get_object_detail'), name="api_getobject"),
        ]

    def get_object_list(self, request, **kwargs):
        # TODO return a list of applabel.model objects that the
        # user has permissions on
        pass

    def get_object_detail(self, request, **kwargs):
        # TODO return a list of permission codes that the user has for
        # (applabel.model).objects.get(pk=kwargs.get('pk'))
        pass
