from django.shortcuts import render,redirect
from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import CreateAPIView
from .serializers import TweetSerializer
from rest_framework.views import APIView
from users.response import Response as response
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
import requests
from .mixins import TweetMixins
from .models import Tweet
from users.models import FollowUser,User
from .forms import TweetCreationForm

BASE_URL='http://127.0.0.1:8000/'
def we_tweet_home(request):
    form=TweetCreationForm()
    if request.method=="POST":
        form=TweetCreationForm(request.POST,request.FILES)
        if form.is_valid():
            try:
                message = request.POST.get('message')
                ENDPOINT='api/tweets/create_api/'
                url =BASE_URL+ENDPOINT
                data ={
                    "message": message,
                    "user":request.user.id,
                }
                print('request.session',request.session.items())
                if 'active'+str(request.user) not in request.session:
                    messages.warning(request,'You are not logged in Please login to make a tweet !')
                    return render(request,template_name='home.html',context={"form":form},status=400)
                access_token=request.session.get('active'+str(request.user))['access']
                headers = {"Authorization": "Bearer "+access_token}
                resp=requests.post(url,data,headers=headers)
                status_code=resp.status_code
                if status_code==200 or status_code==201:
                        messages.success(request, 'Tweet Posted successfully')
                        return redirect("we_tweet_home")
                else:
                    messages.error(request,"Invalid username or password.")
                    return redirect('we_tweet_home')
            except Exception as e:
                print(e)
    ENDPOINT='api/tweets/tweet_list_api/'
    url=BASE_URL+ENDPOINT
    data ={
        "user_id":request.user.id,
    }
    if 'active'+str(request.user) not in request.session:
        messages.warning(request,'You are not logged in Please login to make a tweet !')
        return render(request,template_name='home.html',context={"form":form},status=400)
    access_token=request.session.get('active'+str(request.user))['access']
    headers = {"Authorization": "Bearer "+access_token,
               'accept': 'application/json'}
    resp=requests.post(url,data=data,headers=headers)
    tweets=resp.json()
    for tweet in tweets:
        username=User.objects.filter(id=tweet['user']).first().username
        tweet.update({'user':username,'timestamp':tweet['timestamp'][:10]})
    return render(request,template_name='home.html',context={"form":form,'tweets':tweets},status=200)



class CreateTweetAPIView(CreateAPIView):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/api/tweets/create/
    AUTHORIZATION BEARER TOKEN: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjM4ODE1ODY1LCJpYXQiOjE2Mzg4MTIyNjUsImp0aSI6IjYzOGFiMDY5OWFmZjQ4NmE4NzFmNmExMzI1MTc4NzlhIiwidXNlcl9pZCI6OH0.4Wjw27PvyLBUoAp2fFbx66us94BcI177PAhWgHFxj_g
    REQUEST PARAMETER: {
                            "message":"This is tweet Demo",
                            "user_id":7
                        }
    Response :{
                    "message": "This is tweet Demo",
                    "user": 7
                }
    '''
    serializer_class        = TweetSerializer
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        return serializer.save()

class TweetListByFollowingUser(APIView,TweetMixins):
    '''
    Method: POST
    URL: http://127.0.0.1:8000/user/logout/blacklist/
    REQUEST PARAMETER: {
                            "user_id":7
                        }
    Expected Response :[
                    {
                        "message": "मैं कुछ भी बर्दाश्त कर सकता हूँ, भ्रष्टाचार बर्दाश्त नहीं कर सकता!\r\n\r\nकिसी ने Ticket बेची है तो साबित करो। मैं उनका जहन्नुम तक पीछा करूंगा, उन्हें Jail भेजूंगा, छोडूंगा नहीं।",
                        "timestamp": "2022-01-13T08:50:39.811Z",
                        "user": 3
                    },
                    {
                        "message": "We are friends.\r\nYes it’s true!\r\nWe are excited for a happy new year.\r\nAnd hope you are happy too!",
                        "timestamp": "2022-01-11T01:45:30.308Z",
                        "user": 1
                    },
                    {
                        "message": "Took my first dose of the COVID-19 vaccine at AIIMS. \r\n\r\nRemarkable how our doctors and scientists have worked in quick time to strengthen the global fight against COVID-19. \r\n\r\nI appeal to all those who are eligible to take the vaccine. Together, let us make India COVID-19 free!",
                        "timestamp": "2022-01-11T01:30:04.418Z",
                        "user": 1
                    }
                ]
    '''
    serializer_class        = TweetSerializer
    authentication_classes  = [JWTAuthentication]
    permission_classes      = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            user_id = request.data["user_id"]
            if user_id:
                        followed_users=FollowUser.objects.filter(user_id=user_id)
                        user_list=[user.follow_user_id for user in followed_users]
                        tweet_queryset=Tweet.objects.filter(user_id__in=user_list)
                        json_data=self.serialize(tweet_queryset)
                        return self.render_to_http_response(json_data)
        except Exception as e:
            print(e)
