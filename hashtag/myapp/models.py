from django.db import models
from django.db.models import Model


class dataTable(models.Model):
    id = models.AutoField(primary_key=True)
    COMPUTERNAME = models.CharField(max_length=255)
    OS = models.CharField(max_length=255)
    USERDOMAIN = models.CharField(max_length=255)
    REMOTE_HOST = models.CharField(max_length=255)
    CONTENT_LENGTH = models.BigIntegerField()
    QUERY_STRING = models.TextField()
    HTTP_USER_AGENT = models.TextField()
    GENERATED_KEYWORDS = models.TextField()
    GENERATED_COUNTS = models.TextField(null=True, blank=True)
    CONTENT_LENGTH = models.IntegerField(null=True, blank=True)
    remote_addr = models.GenericIPAddressField(null=True, blank=True)
    KEYWORD = models.CharField(max_length=255)

    def __str__(self):
        return self.KEYWORD

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"
