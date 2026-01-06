from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewForm(forms.Form):
    title1 = forms.CharField()

def index(request):
    title1 = None
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title1 = form.cleaned_data["title1"]
            return HttpResponseRedirect(reverse("title", args=[title1]))
        else:
            return render(request, "encyclopedia/index.html", {"form": form})

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewForm(),
        "title1": title1
    })

def get_data(request, title):

    # Get entry for searched title
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })
    
    # Convert Markdown to HTML
    html_content = markdown2.markdown(content)

    return render(request, "encyclopedia/title.html", {
        "title": title.capitalize(),
        "content": html_content,
    })

def search(request, title2):
    if request.method == "POST":
        form = NewForm(request.POST)
        if form.is_valid():
            title2 = form.cleaned_data["title1"]
            return HttpResponseRedirect(reverse("title", args=[title2]))
        else:
            return render(request, "encyclopedia/index.html", {"form": form})
        
    return render(request, "encyclopedia/search.html", {
        "entries2":util.list_entries(),
        "form": NewForm(),
        "title2": title2
    })
    


