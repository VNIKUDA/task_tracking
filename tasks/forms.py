from django import forms
from tasks.models import Task, Comment

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

    date_input = forms.DateInput({"type": "date"})

    from_date = forms.DateField(required=False, label="Термін з", widget=date_input)
    to_date = forms.DateField(required=False, label="Термін по", widget=date_input)

    def __init__(self, *args, **kwargs):
        super(TaskFilterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"