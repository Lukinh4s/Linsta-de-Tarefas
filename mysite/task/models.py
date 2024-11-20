from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):

    tittle = models.CharField(max_length=100)
    describe = models.TextField(blank=True)
    created = models.DateTimeField(null=True)
    date_completed = models.DateTimeField(null=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    
    def _str_(self):

        return self.tittle + ' - by: ' + self.user.username