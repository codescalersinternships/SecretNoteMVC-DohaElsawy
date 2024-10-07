from django.db import models

# Create your models here.


class Note(models.Model):
    url = models.CharField()
    content = models.CharField()
    is_read = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True)
    num_of_views = models.IntegerField(default=0)

