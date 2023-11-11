from django.db import models


class LinkPair(models.Model):
    long_link = models.URLField()
    short_link = models.CharField(max_length=6, null=True, unique=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    is_custom = models.BooleanField(default=False)
