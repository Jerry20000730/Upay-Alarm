import re
import datetime
import requests

from django.contrib import auth
from django.http import JsonResponse
from django.views import View
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from .auth import CustomBackend
from .forms import loginForm, registerForm, emailVeriForm, locationSetupForm
from .models import UserProfile, EmailVeriRecord
from .utils.email_util import send_email


# check if the domain name is nottingham
def checkEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@][nottingham]+((.edu.cn)|(.ac.uk))'
    if (re.search(regex, email)):
        return True
    else:
        return False
    
# check whether the current user has set up
# the location of the dormitory
def checkLocationSetup(user):
    return user.buildingCode != None and user.floorCode != None and user.roomCode != None


"""
class LogoutView(view):
    The view class for log out

    if the current user has saved the session
    in the session database ('django_session'),
    delete the session id corresponds to the request
    in the database.

"""
class LogoutView(View):
    def get(self, request):
        auth.logout(request)
        request.session.clear()
        response = JsonResponse({
            "statusCode": 0,
            "errorCode": "",
            "message": "logout",
        })
        return response
    
    def post(self, request):
        return JsonResponse({
            "statusCode": -1,
            "errorCode": "NO_METHOD",
            "message": "NO SUCH METHOD EXISTED UNDER CURRENT URL"
        })

"""
class LoginView(view):
    The view class for log in

    Login requires two core steps:
        1. hand in the form containing a email and a password
        2. backend authenticate the password in the database
    (currently, the password is not encrypted, will improve later)
    TODO encrypt password when transmitting form in the HttpRequest

"""
class LoginView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": -1,
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
                # check whether user is active
                # (verification code in the email)
                if user.is_active:
                    user.backend = 'django.contrib.auth.backends.ModelBackend'
                    auth.login(request, user)
                    return JsonResponse({
                        "statusCode": 0,
                        "errorCode": "",
                        "message": "login success"
                    })
                else:
                    return JsonResponse({
                        "statusCode": -1,
                        "errorCode": "INACTIVE",
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
        

"""
class RegisterUserView(view):
    The view class for register user profile

    During the register, it is not compulsory to acquire
    the location of the user, but without location, the 
    electricial bill will not display

    Compulsory parameters in the form includes:
        1. email address
        2. password
        3. rePassword (second time password for confirmation)

"""
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
            if not checkEmail(email=email):
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "WRONG_EMAIL_DOMAIN",
                    "message": "please register using school's email address"
                })
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
            # return if the form submitted in the httprequest
            # is problematic
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "FORM_MISTAKE",
                "message": "form is not complete or contain wrong information"
            })

"""
class EmailVeriView(view):
    The view class for confirm email verification

    If the email fits the requirement, an verification email
    will be sent on our behalf for us to know if the user
    really owns the email address.

    Compulsory parameters in the form includes:
        1. email address
        2. password
        3. rePassword (second time password for confirmation)

"""
class EmailVeriView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": -1,
            "errorCode": "NO_METHOD",
            "message": "NO SUCH METHOD EXISTED UNDER CURRENT URL"
        })

    def post(self, request):
        form = emailVeriForm(request.POST)
        # judge if the form is valid
        if form.is_valid():
            email = form.cleaned_data['email']
            code = form.cleaned_data['code']
            if len(EmailVeriRecord.objects.filter(email=email)) != 0:
                email_record = EmailVeriRecord.objects.get(email=email)
                
                # if the valid code expired
                # will ask the user to register again
                if datetime.datetime.now() > email_record.expire_time:
                    return JsonResponse({
                        "statusCode": -1,
                        "errorCode": "VERI_CODE_EXPIRED",
                        "message": "The verification code is expired"
                    })
                
                # if the submitted code matches the code
                # in the database, then verification success
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
            # or there is just no such email registered
            else:
                return JsonResponse({
                    "statusCode": -1,
                    "errorCode": "EMAIL_NOT_IDENTICAL",
                    "message": "no such email exists"
                })
        # form is problematic
        else:
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "FORM_MISTAKE",
                "message": "form is not complete or contain wrong information"
            })

"""
class locationSetupView(view):
    The view class for setting up the location

    Compulsory parameters in the form includes:
        1. buildingCode: 层号
        2. floorCode: 楼号
        3. roomCode: 房号

"""
class locationSetupView(View):
    def get(self, request):
        return JsonResponse({
            "statusCode": -1,
            "errorCode": "NO_METHOD",
            "message": "NO SUCH METHOD EXISTED UNDER CURRENT URL"
        })

    def post(self, request):
        form = locationSetupForm(request.POST)
        if form.is_valid():
            buildingCode = form.cleaned_data['buildingCode']
            floorCode = form.cleaned_data['floorCode']
            roomCode = form.cleaned_data['roomCode']
            user = request.user
            user.buildingCode = buildingCode
            user.floorCode = floorCode
            user.roomCode = roomCode
            user.save()
            return JsonResponse({
                "statusCode": 0,
                "errorCode": "",
                "message": "location setup success"
            })
        else:
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "FORM_MISTAKE",
                "message": "form is not complete or contain wrong information"
            })


"""
Interface that query the surplus of the electricity bill
in current user's dorm room
"""
@login_required          
def query_surplus(request):
    if request.method == 'GET':
        user = request.user
        print(user.buildingCode)
        # check whether user has setup the location
        # of his/her dormitory
        if not checkLocationSetup(user):
            return JsonResponse({
                "statusCode": -1,
                "errorCode": "NO_LOCATION",
                "message": "user has not setup the location"
            })

        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.39(0x18002732) NetType/WIFI Language/zh_CN',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        url_query = "https://application.xiaofubao.com/app/electric/queryRoomSurplus"
        cookie = {
            'shiroJID': '27d1905c-5540-4323-bc60-c7f07ed532c1'
        }
        payload = {
            'areaId': '2307499265384382465',
            'buildingCode': user.buildingCode,
            'floorCode': user.floorCode,
            'roomCode': user.roomCode,
            'ymId': '2307499265384382465',
            'platform': 'WECHAT_H5'
        }

        resp = requests.post(url=url_query, headers=headers, cookies=cookie, data=payload)
        resp_json = resp.json()
        surplus = resp_json["data"]["surplus"]
        return JsonResponse({
            "statusCode": 0,
            "errorCode": "",
            "message": "surplus acquire success",
            "surplus": surplus
        })

