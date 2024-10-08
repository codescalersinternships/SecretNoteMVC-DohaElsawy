import uuid
from django.db import models

# Create your models here.


class Note(models.Model):
    key = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    url_key = models.CharField(max_length=500)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True)    

