from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Template, Context


def index(request):     
                   
    return render(request, "index.html", {})



