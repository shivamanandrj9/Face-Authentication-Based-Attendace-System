from django.urls import path
from .import views
from django.contrib.auth import views as auth_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('',views.home,name="home"),
    # path('admin',admin.site.urls),
    path('register',views.register,name="register"),
    path('admin_main',views.admin_main,name="admin_main"),
    path('profile',views.profile,name="profile"),
    path('markatt',views.markattendance,name="markatt"),
    path('upload_comp',views.upload_comp,name="upload_comp"),
    path('upload_webcam_mod',views.upload_webcam_mod,name="upload_webcam_mod"),
    path('upload_webcam',views.upload_webcam,name="upload_webcam"),
    path('view',views.view,name="view"),
    path('login',auth_view.LoginView.as_view(template_name='userlogin/login.html'),name="login"),
    path('logout',auth_view.LogoutView.as_view(template_name='userlogin/logout.html'),name="logout"),
    path('change_password',views.change_passwd,name="change_password"),
    # path('password_change/done/',auth_view.PasswordChangeDoneView.as_view(template_name='userlogin/changed.html'), name='password_change_done'),
]
urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
