from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Represent the categories in servers.
    note that this model is above Server and Channel models.

    Attributes:
        name (str): The name of the category.
        description (str, optional): A brief description of the category.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Server(models.Model):
    """
    Represents a server.

    Attributes:
        name (str): The name of the server.
        owner (ForeignKey): A reference to the user who owns the server. 
            This is a foreign key to the user model defined in settings.AUTH_USER_MODEL.
        category (ForeignKey): A reference to the category of the server.
        description (str, optional): A brief description of the server.
        member (ManyToManyField): A many-to-many relationship to the user model 
            defined in settings.AUTH_USER_MODEL, representing the members of the server.
    """
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="Server_owner")
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="Server_category")
    description = models.CharField(max_length=250, blank=True, null=True)
    member = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="Server_members")


class Channel(models.Model):
    """
    Represents a channel in a server.

    Attributes:
        name (CharField): The name of the channel.
        owner (ForeignKey): A reference to the user who owns the server. 
            This is a foreign key to the user model defined in settings.AUTH_USER_MODEL.
        topic (CharField): The topic or theme of the channel.
        server (ForeignKey): A reference to the server in which the channel is created in.

    Methods:
        save(): Overrides the default save method to convert the name to lowercase.
    """
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
