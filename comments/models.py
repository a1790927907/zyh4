from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
class Manger(models.Manager):
    def get_queryset(self):
        return super(Manger,self).get_queryset().filter(isdelete=False)
# Create your models here.
class Comments(models.Model):
    commentmanager = Manger()
    content_type = models.ForeignKey(ContentType,on_delete=models.DO_NOTHING)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type','object_id')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_user')
    comment = models.TextField()
    uploadtime = models.DateTimeField(auto_now_add=True)
    isdelete = models.BooleanField(default=False)
    reply_user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='reply_user')
    parent = models.ForeignKey('self',null=True,on_delete=models.CASCADE,related_name='parent_comment')
    root = models.ForeignKey('self',null=True,related_name='root_comment',on_delete=models.CASCADE)
    cappreciatenum = models.IntegerField(default=0)
    cappreciateuser = models.TextField(default='{"user":[]}')
    class Meta(object):
        db_table = 'comments'
        ordering = ["uploadtime"]

    def __str__(self):
        return self.comment









