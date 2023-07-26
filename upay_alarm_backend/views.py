from django.contrib import auth
from django.http import JsonResponse
from django.views import View

from .auth import CustomBackend
from .forms import loginForm, registerForm, emailVeriForm
from .models import UserProfile, EmailVeriRecord
from django.contrib.auth.hashers import make_password

from .utils.email_util import send_email


# Create your views here.

class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        request.session.clear()
        response = JsonResponse({
            "statusCode": 0,
            "errorCode": "",
            "message": "logout",
        })
        response.delete_cookie()
        return response


class LoginView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": 0,
            "errorCode": "",
            "message": "login",
        })

    def post(self, request):
        # validate the form
        form = loginForm(request.POST)
        if form.is_valid():
            # compare password
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            authentication = CustomBackend()
            user = authentication.authenticate(request, username=email, password=pwd)
            if user is not None:
                if user.is_active:
                    user.backend = 'django.contrib.auth.backend.ModelBackend'
                    auth.login(request, user)
                    print(auth.login(request, user))
                else:
                    return JsonResponse({
                        "statusCode": -1,
                        "errorCode": 'INACTIVE',
                        "message": "user is inactive"
                    })
            else:
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "WRONG_CREDENTIAL",
                    "message": "wrong email or password"
                })
        else:
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "FORM_MISTAKE",
                "message": "form is not complete or contain wrong information"
            })


class RegisterUserView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": -1,
            "errorCode": "NO_METHOD",
            "message": "NO SUCH METHOD EXISTED UNDER CURRENT URL"
        })

    def post(self, request):
        form = registerForm(request.POST)
        # judge if the form is valid
        if form.is_valid():
            # judge whether the password is identical
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['password']
            repwd = form.cleaned_data['rePassword']

            """
            two steps of authentication here:
                1. whether the password is identical
                2. whether the email has already been registered
            """

            # 1. not identical
            if pwd != repwd:
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "PWD_NOT_IDENTICAL",
                    "message": "the password is not identical"
                })

            # 2. exist
            if UserProfile.objects.filter(email=email):
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "EXIST_USER",
                    "message": "the email has already been registered"
                })

            """
            register the user here
            """
            # initiate a form
            user = UserProfile(email=email, password=make_password(pwd))
            # save the username as email
            user.username = email
            # set the active status as false (before clicking on the email)
            user.is_active = False
            # save the user
            user.save()

            """
            send verification email
            """
            if send_email(desc_email=email, send_type='register'):
                # return verification email sending success
                return JsonResponse({
                    "statusCode": 0,
                    "errorCode": "",
                    "message": "The registration is success, please proceed to email verification"
                })
            else:
                # return verification email sending failed
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "VERI_EMAIL_FAILED",
                    "message": "verification email sending wrong, please retry the registration"
                })
        else:
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "FORM_MISTAKE",
                "message": "form is not complete or contain wrong information"
            })


class EmailVeriView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": -1,
            "errorCode": "NO_METHOD",
            "message": "NO SUCH METHOD EXISTED UNDER CURRENT URL"
        })

    def post(self, request):
        form = emailVeriForm(request)
        # judge if the form is valid
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            if len(EmailVeriRecord.objects.filter(email=email)) != 0:
                email_record = EmailVeriRecord.objects.get(email=email)
                if email_record.code == code:
                    user = UserProfile.objects.get(email=email)
                    user.is_active = True
                    user.save()
                    return JsonResponse({
                        "statusCode": 0,
                        "errorCode": "",
                        "message": "user activate success"
                    })
                else:
                    return JsonResponse({
                        "statusCode": -1,
                        "errorCode": "VERI_CODE_NOT_IDENTICAL",
                        "message": "user activate success"
                    })
            else:
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "EMAIL_NOT_IDENTICAL",
                    "message": "no such email exists"
                })
