from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CustomUserSerializer,UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from tweets.models import Tweet
from django.contrib.auth.decorators import login_required
from .serializers import FollowUserSerializer
from .response import Response as response
from .models import User,Profile,FollowUser
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import NewUserForm
import requests


BASE_URL='http://127.0.0.1:8000/'


from django.db.models import Q
def is_user_exists(email='',username=''):
    user=User.objects.filter(Q(email=email)|Q(username=username))
    if user:
        return True
    else:
        return False


def register_request(request):
    if request.method == "POST":
        # try:
            form = NewUserForm(request.POST)
            print(request.POST)
            if form:
                email=request.POST.get("email")
                username=request.POST.get("username")
                password1=request.POST.get("password1")
                password2=request.POST.get("password2")
                print(username,email,password2,password1)
                if is_user_exists(email=email,username=username):
                    return render(request=request, template_name="users/register.html", context={"register_form":form})
                ENDPOINT='users/sign_up_api/'
                url =BASE_URL+ENDPOINT
                data ={
                    "email":email,
                    "username":username,
                    "password": password1
                }
                resp=requests.post(url,data)
                print(resp.status_code)
                resp_json=resp.json()
                print([(key,val) for key,val in resp_json.items()])
                print(resp.json())
                if is_user_exists(email=email,username=username) or resp.status_code==200:
                    messages.success(request, resp_json.get('msg')+" with email id "+email)
                    return redirect("/users")
            messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="users/register.html", context={"register_form":form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        print("request.POST",request.POST)
        print('form',form.is_valid())
        if form.is_valid():
            email = request.POST.get('username')
            password = request.POST.get('password')
            ENDPOINT='users/login_api/'
            url =BASE_URL+ENDPOINT
            data ={
                "email":email,
                "password": password
            }
            if not is_user_exists(email=email):
                return render(request=request, template_name="users/login.html", context={"login_form":form})

            resp=requests.post(url,data)
            # print('resp',resp)
            status_code=resp.status_code
            # print('resp.status_code',resp.status_code)
            resp_json=resp.json()
            # print([(key,val) for key,val in resp_json.items()])
            # print(resp.json())
            resp=resp.json()
            # print(resp.get('msg'))
            # print(resp.get('data'))
            request.session["active"+email]=resp.get('data')
            # print('request.session',request.session["active"+email])
            # print('request.session',request.session.items())
            if status_code==200 and 'email' in resp.get('data'):
                user = authenticate(username=email, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, resp_json.get('msg')+" with email id "+email)
                    return redirect("we_tweet_home")
            else:
                # messages.error(request,"Invalid username or password.")
                return render(request=request, template_name="users/login.html", context={"login_form":form})
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="users/login.html", context={"login_form":form})



def logout_request(request):
    ENDPOINT='users/logout/blacklist/'
    url =BASE_URL+ENDPOINT
    user_session_data=request.session.get('active'+str(request.user))
    refresh_token=user_session_data.get('refresh')
    data ={
        "refresh_token":refresh_token
    }
    resp=requests.post(url,data)
    resp_json=resp.json()
    resp=resp.json()
    if resp_json.get('error')==0 or resp.status_code==200:
        logout(request)
        messages.success(request, resp_json.get('msg'))
        return redirect("/users")
    return redirect('/users')






class CustomUserSignup(APIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/users/sign_up_api/
    REQUEST PARAMETER: {
                        "email":"saurav@gmail.com",
                        "username":"saurav",
                        "password": "pass@123"
                        }
    Response :{
                    "error": 0,
                    "code": 1,
                    "data": {
                        "email": "saurav@gmail.com",
                        "username": "saurav"
                    },
                    "msg": "Your account has been created successfully"
                }
    '''

    permission_classes = [AllowAny]
    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(response.parsejson(_("Your account has been created successfully"), json,  status=status.HTTP_201_CREATED))

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class CustomUserLogin(APIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/api/user/
    REQUEST PARAMETER: {
                        "email":"deepak@gmail.com",
                        "password": "pass@123"
                        }
    Expected Response :{
                            "error": 0,
                            "code": 1,
                            "data": {
                                "id": 1,
                                "email": "deepak@gmail.com",
                                "username": "deepak",
                                "last_login": "2022-01-13T18:58:16.730429Z",
                                "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY0MjcwNTA5NiwiaWF0IjoxNjQyMTAwMjk2LCJqdGkiOiJiNWQ5NzhhYTI4YTU0ZDIwOGE3YzNkZDgxMmNiMDY3ZCIsInVzZXJfaWQiOjF9.myjknctVrVk7AoFf9tOsWxCGFqpRa6JAQf9vzGnNw8c",
                                "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjQyMTg2Njk2LCJpYXQiOjE2NDIxMDAyOTYsImp0aSI6IjQyMDUxMTRlMmZiOTQyYmJiYmM1YjNiOWMwMDIxMTIxIiwidXNlcl9pZCI6MX0.lfmDYzf-_Jou4Fe0o3G6SuT46WcZ5OpVJnldg_bPb_E"
                            },
                            "msg": "User Login successfull"
                        }
    '''

    def post(self, request):
        print(request.data)
        if "email" in request.data and request.data['email'] != "":
            email = request.data.get('email')
            try:
                userObj = User.objects.get(Q(email__iexact=email) | Q(username__iexact=email))
            except Exception as e:
                print("Exception",e)
                return Response(response.parsejson(_("Email/Username does not exist"), "", status=404))
        else:
            return Response(response.parsejson(_("Email/Username is required"), {}, status=404))

        if "password" in request.data and request.data['password'] != "":
            password = request.data.get('password')
        else:
            return Response(response.parsejson(_("password is required"), {}, status=404))

        if (not userObj.check_password(password)):
            return Response(response.parsejson(_("Email/Username or password do not match"), "",status=status.HTTP_404_NOT_FOUND))

        if userObj.is_active == False:
            return Response(response.parsejson(_("Your account is inactive state, Please contact to administrator"), {}, status=404))

        userObj.last_login = timezone.now()
        userObj.save(update_fields=['last_login'])

        serialized_user = UserSerializer(userObj).data
        __resultlist = dict(UserSerializer(userObj).data.items())

        refresh = RefreshToken.for_user(userObj)
        __resultlist['refresh'] = str(refresh)
        __resultlist['access'] = str(refresh.access_token)
        return Response(response.parsejson(_("User Login successfull"),__resultlist, status=201))


class BlacklistTokenUpdateView(APIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/users/logout/blacklist/
    REQUEST PARAMETER: {
                        "refresh_token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTYzOTQ1MDU2NywiaWF0IjoxNjM4ODQ1NzY3LCJqdGkiOiJmNjhlM2Y4NzgxMTc0YmZlODhmM2VhN2YzY2ExMDJjYSIsInVzZXJfaWQiOjEwfQ.DRWr_bZB68XJnHZ7jeIICiYh18IbOmwSuRaLy9TWMqs"
                        }
    Expected Response :{
                    "error": 0,
                    "code": 0,
                    "data": {},
                    "msg": "You have been logged out successfully"
                        }
    '''
    permission_classes = [AllowAny]
    authentication_classes = ()

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(response.parsejson(_("You have been logged out successfully"), {},status=status.HTTP_205_RESET_CONTENT))
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@login_required(login_url='/users/')
def user_profile(request,user_id=0):
    print(request.user.id)
    user_data=User.objects.filter(id=user_id).first()
    if request.user.id and user_id:
        follow_check=FollowUser.objects.filter(user_id=request.user.id,follow_user_id=user_id)
    profile_data=Profile.objects.filter(user_id=user_id).first()
    return render(request,template_name='users/profile.html',context={'user_data':user_data,'profile_data':profile_data,'follow_check':follow_check})

@login_required(login_url='/users/')
def users_list(request):
    users=User.objects.filter(~Q(id=request.user.id))
    return render(request,template_name='users/users_list.html',context={'users':users})


def follow_user(request):
    if request.method=='POST':
        follow_user_id=request.POST.get('follow')
        if follow_user_id:
            print('request.user.id',request.user.id,'follow',follow_user_id)
            ENDPOINT='users/follow_user_api/'
            url =BASE_URL+ENDPOINT
            data ={
                "user":request.user.id,
                "follow_user":follow_user_id
            }
            if 'active'+str(request.user) not in request.session:
                messages.warning(request,'You are not logged in Please login to make a tweet !')
                return redirect('/users/users_list/')
            access_token=request.session.get('active'+str(request.user))['access']
            headers = {"Authorization": "Bearer "+access_token}
            resp=requests.post(url,data,headers=headers)
            status_code=resp.status_code
            resp_json=resp.json()
            if resp_json.get('error')==0 or status_code==200:
                messages.success(request,'Profile Followed Successfully')
            return redirect('/users/users_list/')


class FollowUserCreateView(CreateAPIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/api/tweets/create/
    AUTHORIZATION BEARER TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4ODE1ODY1LCJpYXQiOjE2Mzg4MTIyNjUsImp0aSI6IjYzOGFiMDY5OWFmZjQ4NmE4NzFmNmExMzI1MTc4NzlhIiwidXNlcl9pZCI6OH0.4Wjw27PvyLBUoAp2fFbx66us94BcI177PAhWgHFxj_g
    REQUEST PARAMETER: {"name":"Bajaj Pulsar 150",}
    Response :
    '''
    serializer_class        = FollowUserSerializer
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()
