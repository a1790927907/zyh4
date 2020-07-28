from django.shortcuts import render,get_object_or_404
from blog.models import Blogtype,Blog
from django.http import JsonResponse
from django.conf import settings
from django.template.defaulttags import register
from django.core.paginator import Paginator
from comments.models import Comments
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from zyh4.forms import LoginForm
from django.http import QueryDict
import datetime
@register.filter
def getrange(val):
    return range(val)

@register.filter
def getrangequjian(val1,val2):
    return range(val1,val2)

@register.filter
def jianfa(val1,val2):
    return (val1-val2)

@register.filter
def next(lis1,index):
    return lis1[index+1]

@register.filter
def previous(lis1,index):
    return lis1[index-1]

@register.filter
def getlistval(lis,index):
    try:
        return lis[index]
    except:
        return ''

def markcount():
    marklistcount = 0
    @register.filter
    def digui(comments):
        nonlocal marklistcount
        for comment in comments:
            try:
                subcomment = comment.parent_comment.all()
                a = subcomment[0]
                marklistcount += len(subcomment)
                digui(subcomment)
            except:
                pass
        return marklistcount
@register.filter
def getmarkcount(queryset):
    bloginmark = ContentType.objects.get_for_model(queryset)
    comments = Comments.commentmanager.filter(content_type_id=bloginmark.id,object_id=queryset.id)
    return comments


# Create your views here.

def allblogs(request):
    params = {}
    page = request.GET.get("page","1")
    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")
    params["year"] = ""
    params["month"] = ""
    params["day"] = ""
    bloglistall = Blog.blogmanager.all()
    params['loginform'] = LoginForm()
    params['blogdate'] = Blog.blogmanager.dates('createtime','month',order='DESC')
    if year:
        bloglistall = bloglistall.filter(createtime__year=year)
        params["year"] = year
    if month:
        bloglistall = bloglistall.filter(createtime__month=month)
        params["month"] = month
    if day:
        bloglistall = bloglistall.filter(createtime__day=day)
        params['day'] = day
    paginator = Paginator(bloglistall,settings.PER_PAGE)
    bloglist = paginator.page(int(page)).object_list
    blogtype = Blogtype.typemanager.all()
    if len(bloglistall) > 10:
        allpage = paginator.num_pages
        params['allpage'] = allpage
    params["bloglist"] = bloglist
    params["blogtype"] = blogtype
    params['bloglistall'] = bloglistall
    params['page'] = int(page)
    params["pageshow"] = 5
    try:
        page_start = int(page) - 3
        page_end = int(page) + 2
        if page_start <= 0:
            page_start = 0
            page_end = 5
        if page_end > allpage:
            page_end = allpage
        params['pagerange'] = range(page_start,page_end)
    except:
        pass
    return render(request,'blog/allblogs.html',params)

def showblog(request):
    params = {}
    blogid = request.GET.get("id")
    blogtype = request.GET.get("type")
    if blogtype:
        params['blogtype'] = blogtype
        allblogtype = Blogtype.typemanager.get(blogtype1=blogtype).blog_set.all()
        idlist = [i.id for i in allblogtype]
        params["idlist"] = idlist
        params["index"] = idlist.index(int(blogid))
        params["previousblog"] = previous(list(allblogtype),idlist.index(int(blogid)))
        try:
            params["nextblog"] = next(allblogtype, idlist.index(int(blogid)))
        except:
            params["nextblog"] = allblogtype[0]
    else:
        allblogtype = Blog.blogmanager.all()
        idlist = [i.id for i in allblogtype]
        params["idlist"] = idlist
        params["index"] = idlist.index(int(blogid))
        params["previousblog"] = previous(list(allblogtype), idlist.index(int(blogid)))
        try:
            params["nextblog"] = next(allblogtype, idlist.index(int(blogid)))
        except:
            params["nextblog"] = allblogtype[0]
    blog = get_object_or_404(Blog,id=blogid)
    params["blog"] = blog
    blogincomment = ContentType.objects.get_for_model(blog)
    comments = Comments.commentmanager.filter(content_type_id = blogincomment.id ,object_id=int(blog.id),parent_id=None,root_id=None)
    commentscount = Comments.commentmanager.filter(content_type_id=blogincomment.id, object_id=int(blog.id))
    markcount()
    params['comments'] = comments.order_by('-uploadtime')
    params['commentscount'] = commentscount
    params['loginform'] = LoginForm()
    data = {}
    data['content_type'] = blogincomment.model
    data['object_id'] = blog.id
    params['commentform'] = CommentForm(initial=data)
    return render(request,'blog/showblog.html',params)

def showtypedetail(request):
    blogtype1 = Blogtype.typemanager.all()
    fenlei = request.GET.get("type")
    page = int(request.GET.get('page','1'))
    params = {}
    params["type"] = fenlei
    params['loginform'] = LoginForm()
    blog_type = Blogtype.typemanager.get(blogtype1=fenlei)
    # blog_type = Blogtype.typemanager.filter(blogtype1=fenlei)[0]
    year = request.GET.get("year")
    month = request.GET.get("month")
    day = request.GET.get("day")
    params["year"] = ""
    params["month"] = ""
    params["day"] = ""
    blogtype2 = blog_type.blog_set.all()
    params['blogdate'] = blogtype2.dates('createtime','month',order='DESC')
    if year:
        blogtype2 = blogtype2.filter(createtime__year=year)
        params["year"] = year
    if month:
        blogtype2 = blogtype2.filter(createtime__month=month)
        params["month"] = month
    if day:
        blogtype2 = blogtype2.filter(createtime__day=day)
        params['day'] = day
    paginator = Paginator(blogtype2,settings.PER_PAGE)
    blogtype = paginator.page(page).object_list
    if len(blogtype2)>10:
        allpage = paginator.num_pages
        params['allpage'] = allpage
    params['blogtype'] = blogtype
    params['blogtype1'] = blogtype1
    params['blogtype2'] = blogtype2
    params['page'] = page
    params["pageshow"] = 5
    try:
        page_start = int(page) - 3
        page_end = int(page) + 2
        if page_start <= 0:
            page_start = 0
            page_end = 5
        if page_end > allpage:
            page_end = allpage
        params['pagerange'] = range(page_start, page_end)
    except:
        pass
    return render(request,'blog/showtypedetail.html',params)

import json

@register.filter
def has_appreciate(blog,request):
    jsondata = json.loads(blog.bappreciateuser)
    if request.user.username in jsondata['user']:
        return True
    else:
        return False

@register.filter
def chas_appreciate(comment,request):
    jsondata = json.loads(comment.cappreciateuser)
    if request.user.username in jsondata['user']:
        return True
    else:
        return False

def appreciate(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            blogid = request.POST.get('blogid')
            status = request.POST.get('status','appreciate')
            try:
                blog = Blog.blogmanager.get(id = blogid)
            except:
                return JsonResponse({'status':'error','errormsg':'无对应数据'})
            if status == 'appreciate':
                user_has_appreciate = json.loads(blog.bappreciateuser)
                if request.user.username not in user_has_appreciate['user']:
                    user_has_appreciate['user'].append(request.user.username)
                    user_json_string = json.dumps(user_has_appreciate)
                    blog.bappreciateuser = user_json_string
                    blog.bappreciatenum += 1
                    blog.save()
                    return JsonResponse({'status': 'success','operate':'appreciate','num':blog.bappreciatenum})
                else:
                    return JsonResponse({'status':'error','errormsg':'不能重复点赞'})
            elif status == 'cancel':
                user_has_appreciate = json.loads(blog.bappreciateuser)
                if request.user.username in user_has_appreciate['user']:
                    user_has_appreciate['user'].remove(request.user.username)
                    user_json_string = json.dumps(user_has_appreciate)
                    blog.bappreciateuser = user_json_string
                    blog.bappreciatenum -= 1
                    blog.save()
                    return JsonResponse({'status': 'success','operate':'cancel','num':blog.bappreciatenum})
                else:
                    return JsonResponse({'status': 'error', 'errormsg': '您暂未点赞过'})
            else:
                return JsonResponse({'status': 'error', 'errormsg': '参数错误'})
        else:
            return JsonResponse({'status': 'error', 'errormsg': '请求方式错误'})




























