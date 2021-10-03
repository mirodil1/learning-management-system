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
from .forms import UserLoginForm
app_name = 'course'

urlpatterns = [
    # auth
    path('account/register', views.register, name='register'),
    # path('account/login', auth_views.LoginView.as_view(template_name="registration/login.html",
    #                                                    authentication_form=UserLoginForm), name='login'),
    path('account/login', views.login_request, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    #course
    path('create-course/', views.CourseCreateView.as_view(), name='create'),
    path('my-course/', views.CourseListView.as_view(), name='my_courses'),
    path('<pk>/my-course/edit', views.CourseUpdateView.as_view(), name='course_edit'),
    path('<pk>/my-course/delete', views.CourseDeleteView.as_view(), name='course_delete'),
    path('<pk>/module/', views.CourseModuleUpdateView.as_view(), name='course_module'),
]
