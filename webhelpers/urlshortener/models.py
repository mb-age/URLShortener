from django.db import models


class LinkPair(models.Model):
    url = models.URLField()
    alias = models.CharField(max_length=8, null=True, unique=True)
    created_dt = models.DateTimeField(auto_now_add=True)
    is_custom = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']
