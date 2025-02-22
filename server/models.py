from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Server_owner")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="Server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="Server_members")


class Channel(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Channel_owner")
    topic = models.CharField(max_length=100)
    server = models.ForeignKey(
        Server, on_delete=models.CASCADE, related_name="Channel_server")

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Channel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
