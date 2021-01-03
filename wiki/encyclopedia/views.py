from django.shortcuts import render, redirect
from markdown2 import Markdown
from . import util
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random


md = Markdown()

# Global entries variable for consistent updating of entries
all_entry = util.list_entries()
    
class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea, label="Content")
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": all_entry
    })

def title(request, name):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            form.cleaned_data.get("title")
            titles = form.cleaned_data["title"]
            contents = form.cleaned_data["content"]
            util.save_entry(titles, contents)
        return render(request, "encyclopedia/pages.html", {
            "page": md.convert(util.get_entry(name)),
            "name": name
        })
    if util.get_entry(name) == None:
        return render(request, "encyclopedia/error.html")
    else:
        return render(request, "encyclopedia/pages.html", {
        "page": md.convert(util.get_entry(name)),
        "name": name
    })
        
def search(request):
    query = request.GET['q']
    entry = all_entry
    list_results = []
    if query in entry:
        return title(request, query)
    for i in entry:
        if query in i:
            list_results.append(i)
    return render(request, "encyclopedia/search.html", {
        "results": list_results
    })
        
def new(request):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["title"] in all_entry:
                return render(request, "encyclopedia/error.html")
            else:
                form.cleaned_data.get("title")
                titles = form.cleaned_data["title"]
                contents = form.cleaned_data["content"]
                util.save_entry(titles, contents)
                all_entry.append(titles)
                return title(request, titles)
        else:
            return render(request, "encyclopedia/new.html",{
                "form": form
            })
    return render(request, "encyclopedia/new.html", {
        "form": NewForm()
    })
    
def edit(request, name):
    contentPage = util.get_entry(name)
    return render(request, "encyclopedia/edit.html", {
        "form": NewForm(initial={'title': name, 'content':util.get_entry(name)}),
        "name": name
    })
    
def randomPage(request):
    randPages = random.choice(all_entry)
    return title(request, randPages)
    
