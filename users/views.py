from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView, CreateView
from course.models import Course, Module, User, Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from course.forms import UserEditForm
from django.views.generic.base import View, TemplateResponseMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
# Create your views here.

class CourseListView(ListView):
    model = Course
    template_name = "users_temp/home_page.html"

class CourseDetailView(LoginRequiredMixin,DetailView):
    model = Course
    template_name = "users_temp/module_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        course = self.get_object()
        context['modules'] = course.modules.all()
        return context

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "users_temp/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.get_object()
        context['user'] = user

class UpdateUserProfileView(TemplateResponseMixin,View):
    template_name = 'users_temp/profile_edit.html'

    def get(self, request, *args, **kwargs):
        form = UserEditForm(instance=request.user)
        return self.render_to_response({'form': form})

    def post(self, request, *args, **kwargs):
        form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(f'/{request.user.id}/profile')
        else:
            return self.render_to_response({'form': form})

class PermissionView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'users_temp/permission_form.html'
    success_url = reverse_lazy('users:home')
    success_message = 'Message has been sent'

    model = Permission
    fields = ['permission']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_message(self, cleaned_data):
        # print(cleaned_data)
        return "Message has been sent"

def course_search(request):
    query = None
    results = []

    if 'query' in request.GET:
        query = request.GET['query']

        search_vector = SearchVector('title', 'overview')
        search_query =SearchQuery(query)
        results = Course.objects.annotate(
            search = search_vector,
            rank = SearchRank(search_vector, search_query)
        ).filter(search=search_query).order_by('-rank')

        return render(request,
                      'users_temp/search.html',
                      {'query': query,
                       'results': results})