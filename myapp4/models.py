from django.db import models

class Manager(models.Manager):
    def get_queryset(self):
        return super(Manager,self).get_queryset().filter(isdelete=False)
    def createarticle(self,title1,author1,content1,isdelete1=False):
        art = self.model()
        art.title = title1
        art.author = author1
        art.content = content1
        art.isdelete = isdelete1
        return art
# Create your models here.
class Article(models.Model):
    articleman = Manager()
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=20,blank=True)
    content = models.TextField()
    createtime = models.DateTimeField(auto_now_add=True)
    isdelete  = models.BooleanField(default=False)
    class Meta(object):
        db_table = "article"
        ordering = ["id"]









