from django.db import models


class LinkPair(models.Model):
    """
    Model representing a pair of links, consisting of a long URL and a potentially customized short alias.
    """
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


class Referer(models.Model):
    referer_url = models.URLField(null=True)
    link_pair = models.ForeignKey(LinkPair, on_delete=models.CASCADE, related_name='referers')
    trigger_dt = models.DateTimeField(auto_now_add=True)
