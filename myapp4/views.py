from django.shortcuts import render

from myapp4.models import Article
# Create your views here.
def index(request):
    artlist = Article.articleman.all()
    return render(request,'myapp4/index.html',{"articlelist":artlist})

def showarticle(request,id):
    art = Article.articleman.get(pk=id)
    return render(request,'myapp4/showarticle.html',{"art":art})



