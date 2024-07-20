from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("task-create/", views.TaskCreateView.as_view(), name="task-create"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="task-update"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="task-delete"),
    path("<int:pk>/complete/", views.TaskCompleteView.as_view(), name="task-complete"),
    path("<int:pk>/to-do/", views.TaskToDoView.as_view(), name="task-to-do"),
    path("<int:pk>/in-progress/", views.TaskInProgressView.as_view(), name="task-in-progress"),

    path("comments/<int:pk>/update", views.CommentUpdateView.as_view(), name="comment-update"),
    path("comments/<int:pk>/delete/", views.CommentDeleteView.as_view(), name="comment-delete"),
]

app_name = "tasks"