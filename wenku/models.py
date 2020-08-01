from django.db import models


class WenkuManager(models.Manager):
    def get_queryset(self):
        return super(WenkuManager, self).get_queryset().filter(isdelete=False)

# Create your models here.
class Wenku(models.Model):
    wkmanager = WenkuManager()
    title = models.CharField(max_length=100)
    content = models.BinaryField()
    isdelete = models.BooleanField(default=False)
    def __str__(self):
        return f'<Wenku:{self.title}>'

