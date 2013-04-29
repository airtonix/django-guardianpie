from tastypie.resources import ModelResource
from tastypie.authentication import MultiAuthentication, SessionAuthentication, ApiKeyAuthentication
from tastypie.utils import trailing_slash

from surlex.dj import surl

# from guardian.models import UserObjectPermission, GroupObjectPermission
# from guardian.core import ObjectPermissionChecker


class PermissionResource(ModelResource):
    """

    """
    class Meta:
        resource_name = 'permission'
        authentication = MultiAuthentication(SessionAuthentication(), ApiKeyAuthentication())
        urlargs = {'name': resource_name, 'slash': trailing_slash()}

    def override_urls(self):
        return [
            surl(r"^<resource_name={name}>/model/<model:s>{slash}$".format(**self._meta.urlargs), self.wrap_view('get_object_list'), name="api_getlist"),
            surl(r"^<resource_name={name}>/model/<model:s>/<pk:#>{slash}$".format(**self._meta.urlargs), self.wrap_view('get_object_detail'), name="api_getobject"),
        ]

    def get_object_list(self, request, **kwargs):
        pass

    def get_object_detail(self, request, **kwargs):
        pass
