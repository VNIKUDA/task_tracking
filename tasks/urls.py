from django.urls import path
from tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task-list"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task-detail"),
    path("task-create/", views.TaskCreateView.as_view(), name="task-create"),
    path("task-update/<int:pk>/", views.TaskUpdateView.as_view(), name="task-update"),
    path("task-delete/<int:pk>/", views.TaskDeleteView.as_view(), name="task-delete")
]

app_name = "tasks"