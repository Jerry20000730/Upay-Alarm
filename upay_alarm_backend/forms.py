from django import forms


class loginForm(forms.Form):
    """
    form for login
    """
    email = forms.EmailField(label="学校邮箱", required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    password = forms.CharField(label="密码", required=True, widget=forms.PasswordInput(), min_length=6, error_messages={'invalid': '密码不得少于6位'})

class registerForm(forms.Form):
    """
    form for registration
    """
    email = forms.EmailField(label="学校邮箱", required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    password = forms.CharField(label="密码", required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})
    rePassword = forms.CharField(label="重新输入密码", required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})

class emailVeriForm(forms.Form):
    """
    form for email verification
    """
    email = forms.CharField(label="学校邮箱", required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    code = forms.CharField(label="验证码", required=True, error_messages={'invalid': '请提供正确的验证码'})

class locationSetupForm(forms.Form):
    """
    form for setting up the location
    """
    buildingCode = forms.CharField(label="楼号", required=True, error_messages={'invalid': '请填写正确的楼号'})
    floorCode = forms.CharField(label="层号", required=True, error_messages={'invalid': '请填写正确的层号'})
    roomCode = forms.CharField(label="房号", required=True, error_messages={'invalid': '请填写正确的房间号'})

class forgetPwdForm(forms.Form):
    """
    form for submitting the email for resetting the password
    """
    email = forms.EmailField(required=True, error_messages={'invalid': '请填写正确的邮箱地址'})

class ModifyPwdForm(forms.Form):
    """
    form for resetting the password
    """
    password1 = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})
    password2 = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})
