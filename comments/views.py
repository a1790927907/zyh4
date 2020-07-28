from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from comments.models import Comments
from comments.forms import CommentForm
# Create your views here.
def comment(request):
    if request.method == 'POST':
        comment = Comments()
        commentform = CommentForm(request.POST)
        if not request.user.is_authenticated():
            return JsonResponse({'status':'error'})
        if commentform.is_valid():
            comment.content_object = commentform.cleaned_data['content_object']
            comment.comment = commentform.cleaned_data['commentcontent']
            comment.user = request.user
            comment.save()
            data = {}
            data['user'] = request.user.username
            data['comment'] = commentform.cleaned_data['commentcontent']
            data['uploadtime'] = comment.uploadtime.strftime('%Y-%m-%d %H:%M:%S')
            data['id'] = comment.id
            data['appreciatenum'] = comment.cappreciatenum
            return JsonResponse(data)
        else:
            return JsonResponse({'status':'error'})

def mark(request):
    if request.method == 'POST':
        comment = Comments()
        commentform = CommentForm(request.POST)
        if request.user.is_authenticated():
            if commentform.is_valid():
                comment.content_object = commentform.cleaned_data['content_object']
                comment.user = request.user
                comment.comment = commentform.cleaned_data['commentcontent']
                reply_user = Comments.commentmanager.get(id=int(request.POST.get('urltar')))
                parent_user = Comments.commentmanager.get(id=int(request.POST.get('parent')))
                comment.reply_user = reply_user.user
                comment.parent = parent_user
                comment.save()
                data = {}
                data['user'] = request.user.username
                data['reply_user'] = reply_user.user.username
                data['comment'] = comment.comment
                data['huifuuser'] = comment.user.username
                data['parent'] = parent_user.id
                data['huifuurltar'] = comment.id
                data['urltar'] = request.POST.get('urltar')
                data['commentid'] = comment.id
                data['uploadtime'] = comment.uploadtime.strftime('%Y-%m-%d %H:%M:%S')
                data['appreciatenum'] = comment.cappreciatenum
                return JsonResponse(data)
        else:
            return JsonResponse({'status':'error'})
    else:
        return JsonResponse({'status':'wrong','errormsg':'请刷新重试'})

def removemark(request):
    if request.method == 'POST':
        commentid  =  request.POST.get('id')
    else:
        commentid  =  request.GET.get('id')
    comment = Comments.commentmanager.get(id=int(commentid))
    if (request.user.username == comment.user.username) and request.user.is_authenticated():
        comment.isdelete = True
        comment.save()
        data = {}
        data['status'] = 'success'
        data['removeid'] = comment.id
        return JsonResponse(data)
    else:
        return JsonResponse({"status": 'error'})

import json
from django.template.defaulttags import register
@register.filter
def chas_appreciate(comment,request):
    jsondata = json.loads(comment.cappreciateuser)
    if request.user.username in jsondata['user']:
        return True
    else:
        return False

def has_appreciate(blog,request):
    jsondata = json.loads(blog.bappreciateuser)
    if request.user.username in jsondata['user']:
        return True
    else:
        return False

def appreciate(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            commentid = request.POST.get('blogid')
            status = request.POST.get('status','appreciate')
            try:
                comment = Comments.commentmanager.get(id = commentid)
            except:
                return JsonResponse({'status':'error','errormsg':'无对应数据'})
            if status == 'appreciate':
                user_has_appreciate = json.loads(comment.cappreciateuser)
                if request.user.username not in user_has_appreciate['user']:
                    user_has_appreciate['user'].append(request.user.username)
                    user_json_string = json.dumps(user_has_appreciate)
                    comment.cappreciateuser = user_json_string
                    comment.cappreciatenum += 1
                    comment.save()
                    return JsonResponse({'status': 'success','operate':'appreciate','num':comment.cappreciatenum})
                else:
                    return JsonResponse({'status':'error','errormsg':'不能重复点赞'})
            elif status == 'cancel':
                user_has_appreciate = json.loads(comment.cappreciateuser)
                if request.user.username in user_has_appreciate['user']:
                    user_has_appreciate['user'].remove(request.user.username)
                    user_json_string = json.dumps(user_has_appreciate)
                    comment.cappreciateuser = user_json_string
                    comment.cappreciatenum -= 1
                    comment.save()
                    return JsonResponse({'status': 'success','operate':'cancel','num':comment.cappreciatenum})
                else:
                    return JsonResponse({'status': 'error', 'errormsg': '您暂未点赞过'})
            else:
                return JsonResponse({'status': 'error', 'errormsg': '参数错误'})
        else:
            return JsonResponse({'status': 'error', 'errormsg': '请求方式错误'})
    else:
        return JsonResponse({'status': 'error', 'errormsg': '您未登录'})


















