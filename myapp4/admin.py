from django.contrib import admin
from myapp4.models import Article
# Register your models here.
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['pk','title','author','content','createtime','isdelete']





