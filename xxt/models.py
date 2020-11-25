from django.db import models

# Create your models here.
class Xxt(models.Model):
    xxt_full_url = models.CharField(max_length=500)
    xxt_course_url = models.CharField(max_length=500,default='')
    class Meta(object):
        db_table = "xxt"


