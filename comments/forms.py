from django import forms
from ckeditor.widgets import CKEditorWidget

from django.contrib.contenttypes.models import ContentType
from comments.models import Comments
class CommentForm(forms.Form):
    commentcontent = forms.CharField(widget=CKEditorWidget(config_name='ckeditorconfig'))
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)

    def clean(self):
        try:
            commentcontent = self.cleaned_data['commentcontent']
        except:
            raise forms.ValidationError('评论长度不得小于6个字符')
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        if len(commentcontent) < 14:
            raise forms.ValidationError('评论长度不得小于6个字符')
        try:
            blogclass = ContentType.objects.get(model=content_type).model_class()
            blog = blogclass.blogmanager.get(id=int(object_id))
        except:
            raise forms.ValidationError('评论的博客不存在')
        content_object = blog
        self.cleaned_data['content_object'] = content_object
        return self.cleaned_data

























