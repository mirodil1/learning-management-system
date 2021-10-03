from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateResponseMixin, View
from .models import Course, Module
from .forms import CourseCreateForm, ModuleFormSet
from django.urls import reverse_lazy
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.
User = get_user_model()

class OwnerMixin(object):
    def get_queryset(self):
        qs =super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(object):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class CourseOwnerMixin(OwnerMixin):
    model = Course
    form_class = CourseCreateForm
    success_url = reverse_lazy('course:my_courses')

class CourseOwnerEditMixin(CourseOwnerMixin, OwnerEditMixin):
    template_name ='courses/course_manage/create-course.html'

class CourseCreateView(CourseOwnerEditMixin,CreateView, PermissionRequiredMixin):
    template_name = 'courses/course_manage/create-course.html'
    permission_required = 'course.add_course'

class CourseListView(CourseOwnerMixin, ListView, PermissionRequiredMixin):
    template_name = 'courses/course_manage/my_courses.html'
    permission_required = 'course.view_course'

class CourseUpdateView(CourseOwnerEditMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'courses/course_manage/create-course.html'
    permission_required = 'course.change_course'

class CourseDeleteView(CourseOwnerMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'courses/course_manage/delete_course.html'
    permission_required = 'course.delete_course'

class CourseModuleUpdateView(TemplateResponseMixin, View):
    template_name = 'courses/module/formset.html'
    course =None

    def dispatch(self, request, pk):
        self.course = get_object_or_404(Course,
                                        id=pk,
                                        owner=request.user)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        formset = ModuleFormSet(instance=self.course)
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

    def post(self, request, *args, **kwargs):
        formset = ModuleFormSet(request.POST, request.FILES, instance=self.course)
        if formset.is_valid():
            for form in formset:
                formset.save()
            return redirect('course:my_courses')
        return self.render_to_response({'course': self.course,
                                        'formset': formset})

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        first_name = request.POST['first_name']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2 and len(password) > 5:
            user = User.objects.create_user(first_name=first_name,
                                            email=email,
                                            password=password)
            user.save()
            messages.success(request, 'Successfully created')
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, "Please, fill in all forms correctly")
            return render(request, "registration/register.html")

    return render(request, "registration/register.html")

def login_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Logged in as {request.user.first_name}")
            return redirect('/')
        else:
            messages.error(request, 'Wrong password or email')
            return render(request, 'registration/login.html')

    else:
        return render(request, 'registration/login.html')
