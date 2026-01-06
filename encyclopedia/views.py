from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse


class NewForm(forms.Form):
    title1 = forms.CharField()


def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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



def search(request):
    query = request.GET.get("q", "").strip()
    entries = util.list_entries()

    # 1️⃣ Exact match → go to page
    for entry in entries:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse("title", args=[entry]))

    # 2️⃣ Substring results
    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })
    


