from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
class Manager(models.Manager):
    def get_queryset(self):
        return super(Manager,self).get_queryset().filter(blogisdelete=False)
    def createarticle(self,title1,author1,content1,blogtype1,isdelete1=False):
        blog = self.model()
        blog.title = title1
        blog.author = author1
        blog.content = content1
        blog.blogtype = blogtype1
        blog.isdelete = isdelete1
        return blog
class TypeManager(models.Manager):
    def get_queryset(self):
        return super(TypeManager,self).get_queryset().filter(typeisdelete=False)
class Blogtype(models.Model):
    typemanager = TypeManager()
    blogtype1 = models.CharField(max_length=15)
    typeisdelete = models.BooleanField(default=False)
    class Meta(object):
        db_table = "blogtype"
        ordering = ["id"]
    def __str__(self):
        return self.blogtype1

class Blog(models.Model):
    blogmanager = Manager()
    title = models.CharField(max_length=30)
    content = RichTextUploadingField()
    author = models.ForeignKey(User,related_name='author_user')
    createtime = models.DateTimeField(auto_now_add=True)
    updatetime = models.DateTimeField(auto_now=True)
    blogtype = models.ForeignKey(Blogtype)
    blogisdelete = models.BooleanField(default=False)
    bappreciatenum = models.IntegerField(default=0)
    bappreciateuser = models.TextField(default='{"user":[]}')
    class Meta(object):
        db_table = "blog"
        ordering = ["id"]



