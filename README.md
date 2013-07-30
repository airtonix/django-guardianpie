See the docstring in `guardianpie/authorization.py` for more details.

Here is a basic example:

### Settings

```
#project/settings.py
API_PRIVATETHING_PERMISSIONS_CREATE = "add_something"
API_PRIVATETHING_PERMISSIONS_VIEW = "view_something"
API_PRIVATETHING_PERMISSIONS_UPDATE = "change_something"
API_PRIVATETHING_PERMISSIONS_DELETE = "delete_something"
```

### Api Resources

```
#project/something/api/resources.py
from django.conf import settings

from tastypie.resources import ModelResource
from guardianpie.authorizations import GuardianAuthorization

from .. import models


class SomethingResource(ModelResource):
    class Meta:
        queryset = models.PrivateThing.objects.all()
        authorization = GuardianAuthorization(
            create_permission_code=settings.API_PRIVATETHING_PERMISSIONS_CREATE,
            view_permission_code=settings.API_PRIVATETHING_PERMISSIONS_VIEW,
            update_permission_code=settings.API_PRIVATETHING_PERMISSIONS_UPDATE,
            delete_permission_code=settings.API_PRIVATETHING_PERMISSIONS_DELETE)
```

### Models

if you create, update and delete permission codenames match the default django permission
codenames for those actions, then you don't need to define them in the `Meta` class.

```
#project/something/models.py
from django.conf import settings
from django.db import models

from guardian.shortcuts import assign_perm


class PrivateThing(models.Model):
	creator = models.ForiegnKey('auth.User')

	...

    class Meta:
        permissions = (
            (settings.API_SOMETHING_PERMISSIONS_VIEW, u'View Something'),
        )

```

### Signals

Now you'll need some way to allow the user to do stuff with the model

```
#project/something/signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver, Signal
from django.contrib.auth.models import User

from guardian.shortcuts import assign_perm

from .models import PrivateThing

@receiver(post_save, sender=User)
def allow_user_to_create_privatethings(user=None, **kwargs):
    if not user:
        return None

    user.user_permissions.add(settings.API_PRIVATETHING_PERMISSIONS_CREATE)


@receiver(post_save, sender=PrivateThing)
def allow_user_to_edit_privatethings(self, thing=None, *args, **kwargs):
	if not thing or not isinstance(thing, PrivateThing):
		return None

    assign_perm(settings.API_PRIVATETHING_PERMISSIONS_VIEW, user_or_group=thing.creator, obj=thing)
    assign_perm(settings.API_PRIVATETHING_PERMISSIONS_UPDATE, user_or_group=thing.creator, obj=thing)
    assign_perm(settings.API_PRIVATETHING_PERMISSIONS_DELETE, user_or_group=thing.creator, obj=thing)

```