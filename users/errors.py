from django.http import HttpResponseRedirect
from django.urls import reverse_lazy

def error_403(request, exception=None):
    return HttpResponseRedirect(reverse_lazy("users:permission-denied"))