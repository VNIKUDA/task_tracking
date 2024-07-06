from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks.forms import TaskForm
from tasks import models

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"
    paginate_by = 7


class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


class TaskCreateView(CreateView):
    model = models.Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm
    success_url = reverse_lazy("tasks:task-list")


class TaskUpdateView(UpdateView):
    model = models.Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        return reverse_lazy("tasks:task-detail", kwargs={"pk": pk})

class TaskDeleteView(DeleteView):
    model = models.Task
    template_name = "tasks/task_delete.html"
    success_url = reverse_lazy("tasks:task-list")