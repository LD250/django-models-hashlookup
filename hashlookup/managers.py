from querysets import HashFilterQuerySet
from django.db import models


class ManagerHashMixin(object):

    def get_queryset(self):
        return HashFilterQuerySet(self.model, using=self._db)


class ManagerHash(ManagerHashMixin, models.Manager):
    pass

