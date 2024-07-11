from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from tasks.forms import TaskForm, TaskFilterForm
from tasks.mixins import UserIsOwnerMixin
from tasks import models

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()

        status = self.request.GET.get("status", "")
        priority = self.request.GET.get("priority", "")

        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)

        return context


class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")

    def form_valid(self, form):
        form.instance.creator = self.request.user
        
        return super().form_valid(form)
    

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Task
    template_name = "tasks/task_update_form.html"
    form_class = TaskForm

    def get_success_url(self) -> str:
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.id})


class TaskDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks:task-list")


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "done"
        task.save()

        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))
    
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    
class TaskInProgressView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "in_progress"
        task.save()

        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))
    
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    
class TaskToDoView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "todo"
        task.save()

        return HttpResponseRedirect(reverse_lazy("tasks:task-list"))
    
    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)