from django.contrib import admin

# Register your models here.
from blog.models import Blogtype,Blog
class Add(admin.TabularInline):
    model = Blogtype
    extra = 1
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):

    list_display = ["title",'blogtype','bappreciatenum','createtime','updatetime']
    list_per_page = 10

@admin.register(Blogtype)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ['blogtype1']
    list_per_page = 10






