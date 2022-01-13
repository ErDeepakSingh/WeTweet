from django.urls import path
from .views import CustomUserLogin,CustomUserSignup,\
    BlacklistTokenUpdateView,\
    login_request,\
    logout_request,\
    register_request,user_profile,\
    follow_user,\
    users_list,\
    FollowUserCreateView



app_name = 'users'

urlpatterns = [
    path("",login_request, name="user_login"),
    path('logout/',logout_request,name='user_logout'),
    path('register/', register_request,name="user_register"),
    path('profile/<int:user_id>/', user_profile,name="user_profile"),
    path('follow_user/', follow_user,name="follow_user"),
    path('users_list/', users_list,name="users_list"),
    path('follow_user_api/', FollowUserCreateView.as_view(),name="follow_user_api"),
    path('login_api/', CustomUserLogin.as_view(),name="login_api"),
    path('sign_up_api/', CustomUserSignup.as_view(), name="sign_up_api"),
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),name='logout_api')
]