from django.db import models


class LinkPair(models.Model):
    url = models.URLField()
    alias = models.CharField(max_length=50, null=True, unique=True, db_index=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    is_custom = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    request_count = models.IntegerField(default=0)
    is_secured = models.BooleanField(default=False)
    password = models.CharField(max_length=100, null=True)

    class Meta:
        ordering = ['-pk']
