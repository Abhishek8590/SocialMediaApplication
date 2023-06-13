"""finsta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/',views.SignupView.as_view(),name="register"),
    path("",views.SignInView.as_view(),name="signin"),
    path("index/",views.IndexView.as_view(),name="index"),
    path("profile/<int:pk>/change/",views.ProfileEditView.as_view(),name="profile-edit"),
    path("logout/",views.signout_view,name="signout"),
    path("posts/<int:pk>/like/",views.add_like_view,name="addlike"),
    path("posts/<int:pk>/comment/",views.add_comment_view,name="addcomment"),
    path("comment/<int:pk>/remove/",views.delete_comment_view,name="removecomment"),
    path("profile/<int:pk>",views.ProfileDetailView.as_view(),name="profile-detail"),
    path("profile/all",views.ProfileListView.as_view(),name="profile-list"),
    path("profile/<int:pk>/coverpic/change",views.change_cover_pic_view,name="coverpic-change"),
    path("profile/all",views.ProfileListView.as_view(),name="profile-all"),
    path("profile/<int:pk>/follow/",views.follow_view,name="follow"),
    path("profile/<int:pk>/unfollow/",views.unfollow_view,name="unfollow")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
