from django.db import models
from hashlookup.managers import ManagerHash

class HashLookupTestModel(models.Model):
    url = models.TextField()
    url_hash = models.CharField(max_length=100, unique=True)

    objects = models.Manager()
    objects_hash = ManagerHash()

