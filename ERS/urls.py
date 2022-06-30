from django.urls import path
from . import views

urlpatterns=[
        path('', views.home, name='home'),
        path('Home', views.login_in, name='Home'),
        path('Main_home', views.Main_home, name='Main_home'),
        path('home_series', views.home_series, name='home_series'),
        path('HTP', views.HTP, name='HTP'),
        path('home_parallel', views.home_parallel, name='home_parallel'),
        path("register",views.register, name="register"),
        path("forgot_password",views.forgot_password, name="forgot_password"),
        path("send_otp",views.send_otp,name="send otp"),
        path("sampleotp",views.sampleotp,name="sampleotp"),
        path("password_trial",views.password_trial,name="password_trial"),
        path("reset_password",views.reset_password,name="reset_password"),
        path("demo1",views.demo1,name="demo1"),
        path("admin_main",views.admin_main,name="admin_main"),
        path("Register_request",views.Register_request,name="Register_request"),
        path("Reset_pwd_request",views.Reset_pwd_request,name="Reset_pwd_request"),
        path("upload_data",views.upload_data,name="upload_data"),
        path("calculate",views.calculate,name="calculate"),
        path("send_data",views.send_data,name="send data"),
        path("reset_password",views.reset_password,name="reset_password"),
        path("admin_login",views.admin_login,name="admin_login"),
        path("logout",views.logout_out,name="logout"),

]