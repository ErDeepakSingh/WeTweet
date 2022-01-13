from django.urls import path
from .views import CreateTweetAPIView,TweetListByFollowingUser
app_name = 'tweets'

urlpatterns = [
    # path('', CreateTweetAPIView.as_view(), name="tweets"),
    path('create_api/', CreateTweetAPIView.as_view(), name="tweets_api"),
    path('tweet_list_api/', TweetListByFollowingUser.as_view(),name="tweet_list_api"),

]