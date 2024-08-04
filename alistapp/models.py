from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class checklist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    checklist_name = models.CharField(max_length=1000)
    status = models.BooleanField(default=False)

    def _str_(self):
        return self.checklist_name