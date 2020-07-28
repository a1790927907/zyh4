from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',widget=forms.TextInput(attrs={'class':"form-control",'placeholder':'请输入账号'}))
    password = forms.CharField(label='密码',widget=forms.PasswordInput(attrs={'class':"form-control",'placeholder':'请输入密码'}))

    #验证表单正确性，重写clean方法，若不出错，则is_valid函数返回True，否则返回False
    def clean(self):
        #cleaned_data用于获取表单填写的数据
        #此方法会在视图中自动调用，视图只要调用了，它就调用了
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = auth.authenticate(username=username,password=password)
        if user:
            #如果验证成功，user不为None，那么直接给cleaned_data字典添加一个键值对返回给视图
            #这样form表单对象的cleaned_data属性里面就有user了
            self.cleaned_data['user'] = user
            return self.cleaned_data
        else:
            #这个ValidationError类会连带着form表单+错误信息一起返回给浏览器，就相当于重新加载一遍页面，然后多出来个错误信息
            #因为是个错误信息，所以要用raise抛出
            raise forms.ValidationError("用户名或密码错误")


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=20,min_length=6,error_messages={'required':'不能为空',"invalid":'请检查是否输入正确'},label='用户名',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'请输入用户名'}))
    password = forms.CharField(min_length=6,error_messages={'required':'长度在6-20个字符之间',"invalid":'请检查是否输入正确'},label='密码',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'请输入密码'}))
    password_again = forms.CharField(min_length=6, error_messages={'required':'长度在6-20个字符之间',"invalid":'请检查是否输入正确'}, label='再次输入密码',widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '请再次输入密码'}))
    email = forms.EmailField(label='邮箱',widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'输入邮箱'}))
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("当前用户已存在")
        else:
            return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("当前邮箱已存在")
        else:
            return email

    def clean(self):
        password = self.cleaned_data['password']
        password_again = self.cleaned_data['password_again']
        if password != password_again:
            raise forms.ValidationError("两次输入密码不一致")
        else:
            return self.cleaned_data


















