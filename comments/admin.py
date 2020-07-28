from django.contrib import admin
from comments.models import Comments
# Register your models here.
@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['content_type','object_id','user','uploadtime']








