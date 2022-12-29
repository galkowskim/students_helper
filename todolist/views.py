from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from .models import Task, Project


class ProjectCreate(LoginRequiredMixin, CreateView):
    model = Project
    fields = ['title', 'description']
    success_url = reverse_lazy('todolist:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user

        return super(ProjectCreate, self).form_valid(form)


class ProjectDetail(LoginRequiredMixin, DetailView):
    model = Project
    context_object_name = 'project'
    template_name = 'todolist/project.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectDetail, self).get_context_data(**kwargs)
        context['tasks'] = Task.objects.filter(project=self.object)
        context['projects'] = Project.objects.filter(user=self.request.user)
        return context


class ProjectUpdate(LoginRequiredMixin, UpdateView):
    model = Project
    fields = ['title', 'description']

    def get_success_url(self):
        return reverse_lazy('todolist:project', kwargs={'pk': self.object.pk})


class ProjectDelete(LoginRequiredMixin, DeleteView):
    model = Project
    context_object_name = "project"
    success_url = reverse_lazy('todolist:tasks')


class MainPageToDoList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user, project=None)
        context['projects'] = Project.objects.filter(user=self.request.user)
        context['count'] = context['tasks'].filter(status_of_completion=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__icontains=search_input)

        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'todolist/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'content', 'status_of_completion', 'project']
    success_url = reverse_lazy('todolist:tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def get_form(self, *args, **kwargs):
        form = super(TaskCreate, self).get_form(*args, **kwargs)
        form.fields['project'].queryset = Project.objects.filter(user=self.request.user)
        return form


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('todolist:tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy('todolist:tasks')
