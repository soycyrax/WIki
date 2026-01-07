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

    # Exact match → go to page
    for entry in entries:
        if entry.lower() == query.lower():
            return HttpResponseRedirect(reverse("title", args=[entry]))

    # Substring results
    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "query": query,
        "results": results
    })

def create_new_page(request):
    title = request.GET.get("page_name","").strip()
    entries = util.list_entries()

    results = [entry for entry in entries if entry.lower() == title.lower()]

    if results:
        return render(request, "encyclopedia/error_existingentry.html", {
            "title": title
        })

    return render(request, "encyclopedia/create.html", {
        "title":title,
        "results": results
    })
    


