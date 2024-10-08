from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
import datetime
from tasks.forms import TaskForm, TaskFilterForm, CommentForm
from tasks.mixins import UserIsOwnerMixin
from tasks import models

# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = "tasks"
    template_name = "tasks/task_list.html"
    paginate_by = 7


    def get(self, request, *args, **kwargs) -> HttpResponse:
        return super().get(request, *args, **kwargs)


    def get_queryset(self):
        queryset = super().get_queryset()

        # ЕТАП ФІЛЬТРАЦІЇ ЗАВДАНЬ
        status = self.request.GET.get("status", "")
        priority = self.request.GET.get("priority", "")
        from_date = self.request.GET.get("from_date", "")
        to_date = self.request.GET.get("to_date", "")

        # Застосувати фільтри по терміну
        if from_date:
            from_date = datetime.date.fromisoformat(from_date)
            queryset = queryset.filter(due_date__gte=from_date)
        if to_date:
            to_date = datetime.date.fromisoformat(to_date)
            queryset = queryset.filter(due_date__lte=to_date)

        # Застосувати фільтри по статусу і пріорітету
        if status:
            queryset = queryset.filter(status=status)
        if priority:
            queryset = queryset.filter(priority=priority)

        # ЕТАП СОРТУВАННЯ ЗАВДАНЬ
        sort = self.request.GET.get("sort", "")

        # Розвернути список завдань якщо сортування встановлено "oldest"
        if sort == "oldest":
            queryset = queryset.reverse()

        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = TaskFilterForm(self.request.GET)

        get_data = dict(self.request.GET.items())
        if "page" in get_data.keys():
            del get_data["page"]

        filters = ""
        for filter, value in get_data.items():
            filters += f"{filter}={value}&"
        context["filters"] = filters

        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = models.Task
    context_object_name = "task"
    template_name = "tasks/task_detail.html"


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        task = self.get_object()
        user = self.request.user

        comments = models.Comment.objects.filter(task=task).annotate(count=Count("likes")).order_by("-count", "-created_at")
        context["comments"] = comments

        context["liked_comments"] = []
        if user.is_authenticated:
            context["liked_comments"] = [comment for comment in comments if any(like in comment.likes.all() for like in user.like_comments.all())]
        
        context["form"] = CommentForm()

        return context
    

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST, request.FILES)
        task = self.get_object()

        if form.is_valid():
            form.instance.task = task
            form.instance.author = self.request.user

            form.save()

        return redirect(reverse_lazy("tasks:task-detail", kwargs={"pk": task.id}))


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = models.Task
    template_name = "tasks/task_form.html"
    form_class = TaskForm


    def form_valid(self, form):
        form.instance.author = self.request.user
        
        return super().form_valid(form)


    def get_success_url(self):
        return reverse_lazy("tasks:task-detail", kwargs={"pk": self.object.id})


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


    def form_valid(self, form):
        task = self.get_object()

        for comment in task.comments.all():
            comment.delete()

        return super().form_valid(form)


class TaskCompleteView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "done"
        task.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    

class TaskInProgressView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "in_progress"
        task.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    

class TaskToDoView(LoginRequiredMixin, UserIsOwnerMixin, View):
    def get(self, request, *args, **kwargs):
        task = self.get_object()

        task.status = "todo"
        task.save()

        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    

    def get_object(self):
        task_id = self.kwargs.get("pk")
        return get_object_or_404(models.Task, pk=task_id)
    

class CommentUpdateView(LoginRequiredMixin, UserIsOwnerMixin, UpdateView):
    model = models.Comment
    form_class = CommentForm
    template_name = "tasks/comment_update.html"
    context_object_name = "comment"


    def get_success_url(self):
        comment = self.get_object()
        task = comment.task

        return reverse_lazy("tasks:task-detail", kwargs={"pk": task.id}) + f"#{comment.pk}"
    

    def form_valid(self, form):
        comment = self.get_object()

        if form.instance.media.name != comment.media.name:
            comment.media.delete()

        return super().form_valid(form)


class CommentDeleteView(LoginRequiredMixin, UserIsOwnerMixin, DeleteView):
    model = models.Comment
    template_name = "tasks/comment_delete.html"
    context_object_name = "comment"


    def get_success_url(self):
        comment = self.get_object()
        task = comment.task

        return reverse_lazy("tasks:task-detail", kwargs={"pk": task.id})


class CommentLikeToggleView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        comment = self.get_object()

        like, created = models.Like.objects.get_or_create(comment=comment, author=request.user)
        if not created:
            like.delete()

        context = {
            "comment": comment,
            "is_liked": any(like in comment.likes.all() for like in self.request.user.like_comments.all())
        }

        return render(request, "tasks/comment_like.html", context=context)


    def get_object(self):
        comment_id = self.kwargs.get("pk")
        return get_object_or_404(models.Comment, pk=comment_id)

class CommentLikesView(View):
    def get(self, requset, *args, **kwargs):
        comment = self.get_object()

        response = ""
        if comment:
            response = f'{len(comment.likes.all())}'

        return HttpResponse(response)
    
    def get_object(self):
        comment_id = self.kwargs.get("pk")
        return get_object_or_404(models.Comment, pk=comment_id)