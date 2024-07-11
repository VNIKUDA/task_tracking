from django import forms
from tasks.models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "status", "priority", "due_date"]
        widgets = {
            "due_date": forms.DateInput(attrs={'type':"date"})
        }

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class TaskFilterForm(forms.Form):
    STATUS_CHOICES = (
        ("", "All"),
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done")
    )

    PRIORITY_CHOICES = (
        ("", "All"),
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False, label="Статус")
    priority = forms.ChoiceField(choices=PRIORITY_CHOICES, required=False, label="Пріорітет")

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        self.fields["status"].widget.attrs.update({"class": "form-control"})
        self.fields["priority"].widget.attrs.update({"class": "form-control"})