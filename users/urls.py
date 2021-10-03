"""onlinedars URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [
    path('', views.CourseListView.as_view(), name='home'),
    path('<pk>/<slug>/module/', views.CourseDetailView.as_view(), name='course_detail'),
    path('<pk>/profile/', views.UserDetailView.as_view(), name='user_profile'),
    path('<pk>/profile_edit', views.UpdateUserProfileView.as_view(), name='profile_edit'),
    path('permission/', views.PermissionView.as_view(), name = 'permission'),
    path('search/', views.course_search, name='post_search'),
]
