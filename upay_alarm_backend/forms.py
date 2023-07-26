from django import forms


class loginForm(forms.Form):
    """
    form for login
    """
    email = forms.EmailField(label="学校邮箱", required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    password = forms.CharField(required=True, widget=forms.PasswordInput(), min_length=6, error_messages={'invalid': '密码不得少于6位'})

class registerForm(forms.Form):
    """
    form for registration
    """
    email = forms.EmailField(required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    password = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})
    rePassword = forms.CharField(required=True, min_length=6, error_messages={'invalid': '密码不得少于6位'})

class emailVeriForm(forms.Form):
    """
    form for email verification
    """
    email = forms.CharField(required=True, error_messages={'invalid': '请填写正确的邮箱地址'})
    code = forms.CharField(required=True, error_messages={'invalid': '请提供正确的验证码'})


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
