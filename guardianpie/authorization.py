import logging
from django.conf import settings

from tastypie.authorization import DjangoAuthorization
from tastypie.http import HttpForbidden, HttpApplicationError
from guardian.shortcuts import get_objects_for_user


logger = logging.getLogger(__name__)
ALWAYS_ALLOW_STAFF = getattr(settings, 'GUARDIANPIE_ALWAYS_ALLOW_STAFF', True)


class GuardianAuthorization(DjangoAuthorization):
    """

    GuardianAuthorization

        Object level permission checking with django-guardian for django models exposed via tastypie.

    :param requires_view_code: the permission code that signifies the user can view the detail
    :type requires_view_code: boolean
    :param view_permission_code: the permission code that signifies the user can view the detail
    :type view_permission_code: string

    :param requires_create_code: will permission checks be carried out for create operations?
    :type requires_create_code: boolean
    :param create_permission_code: the permission code that signifies the user can create one of these objects
    :type create_permission_code: string

    :param requires_update_code: will permission checks be carried out for update operations?
    :type requires_update_code: boolean
    :param update_permission_code: the permission code that signifies the user can update one of these objects
    :type update_permission_code: string

    :param requires_remove_code: will permission checks be carried out for update operations?
    :type requires_remove_code: boolean
    :param remove_permission_code: the permission code that signifies the user can remove one of these objects
    :type remove_permission_code: string

    :return values:
        Empty list : When user requests a list of resources for which they have no
                     permissions for any of the items
        HttpForbidden : When user does not have nessecary permissions for an item
        HttpApplicationError : When resource being requested isn't a valid django model.



        class Something(models.Model):
            name = models.CharField()

        class SomethingResource(ModelResource):
            class Meta:
                queryset = Something.objects.all()
                authorization = GuardianAuthorization(
                    view_permission_code = 'can_view',
                    create_permission_code = 'can_create',
                    update_permission_code = 'can_update',
                    delete_permission_code = 'can_delete'
                    )

    """

    def __init__(self, *args, **kwargs):
        self.requires_view_code = kwargs.pop("requires_view_code", True)
        self.view_permission_code = kwargs.pop("view_permission_code", 'can_view')

        self.requires_create_code = kwargs.pop("requires_create_code", True)
        self.create_permission_code = kwargs.pop("create_permission_code", 'can_create')

        self.requires_update_code = kwargs.pop("requires_update_code", True)
        self.update_permission_code = kwargs.pop("update_permission_code", 'can_update')

        self.requires_delete_code = kwargs.pop("requires_delete_code", True)
        self.delete_permission_code = kwargs.pop("delete_permission_code", 'can_delete')

    def is_site_moderator(self, user=None):
        if user.is_superuser:
            return True
        elif user.is_staff and ALWAYS_ALLOW_STAFF:
            return True
        return False

    def requires_check(self, permission):
        if permission is self.create_permission_code and not self.requires_create_code:
            return False
        elif permission is self.view_permission_code and not self.requires_view_code:
            return False
        elif permission is self.update_permission_code and not self.requires_update_code:
            return False
        elif permission is self.delete_permission_code and not self.requires_delete_code:
            return False
        return True

    def generic_base_check(self, object_list, bundle):
        """
            Raises a HttpApplicationError exception if either:
                a) if the `object_list.model` doesn't have a `_meta` attribute
                b) the `bundle.request` object doesn have a `user` attribute
        """
        if not self.base_checks(bundle.request, object_list.model):
            return HttpApplicationError("Invalid resource.")
        return True

    def generic_item_check(self, object_list, bundle, permission):
        """
            Single item check, returns boolean indicating that the user
            can access the item resource.
        """
        user = bundle.request.user
        self.generic_base_check(object_list, bundle)
        if self.is_site_moderator(user) or not self.requires_check(permission):
            return True
        if not user.has_perm(permission, bundle.obj):
            return HttpForbidden("You are not allowed to access that resource.")

        return True

    def generic_list_check(self, object_list, bundle, permission):
        """
            Multiple item check, returns queryset of resource items the user
            can access.

            TODO: debating whether to return an empty list or HttpNoContent
        """
        user = bundle.request.user
        self.generic_base_check(object_list, bundle)

        if self.is_site_moderator(user) or not self.requires_check(permission):
            return object_list
        return get_objects_for_user(user, permission, object_list)

    # List Checks
    def create_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.create_permission_code)

    def read_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.view_permission_code)

    def update_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.update_permission_code)

    def delete_list(self, object_list, bundle):
        return self.generic_list_check(object_list, bundle, self.delete_permission_code)

    # Item Checks
    def create_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.create_permission_code)

    def read_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.view_permission_code)

    def update_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.update_permission_code)

    def delete_detail(self, object_list, bundle):
        return self.generic_item_check(object_list, bundle, self.delete_permission_code)
