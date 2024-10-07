from django.db import models

# Create your models here.


class Note(models.Model):
    url = models.CharField(max_length=500)
    content = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now=True)
    num_of_views = models.IntegerField(default=0)

