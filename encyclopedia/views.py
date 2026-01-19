from django.shortcuts import render
from . import util
import markdown2
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
import random


class NewForm(forms.Form):
    title1 = forms.CharField()

# Return the index page
def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Get the contents of .md file
def get_data(request, title):

    # Get contents of .md file for searched title
    content = util.get_entry(title)

    # if page name typed in URL is not found
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


# To search a page
def search(request):

    # Get name of searched title
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

# Creates a new page
def create_new_page(request):
    title = ""
    content = ""
    results = ""
    if request.method == "POST":
        title = request.POST.get("page_name","").strip()
        content = request.POST.get("page_body", "")
        entries = util.list_entries()

        # Title for page cannot be empty
        if not title:
            return render(request, "encyclopedia/create.html", {
                "error": "Title cannot be empty"
            })
        
        results = [entry for entry in entries if entry.lower() == title.lower()]

        # If page already exists
        if results:
            return render(request, "encyclopedia/error_existingentry.html", {
                "title": title
            })
        
        # Save and display new page
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("title", args=[title]))

    return render(request, "encyclopedia/create.html", {
        "title":title,
        "results": results,
    })

def edit(request, title):
    if request.method == "GET":
        content = util.get_entry(title)

        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "Page not found"
            })

        return render(request, "encyclopedia/edit.html", {
            "title": title,
            "content": content
        })

    else:  # POST
        new_content = request.POST["content"]
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse("title", args=[title]))
    
def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return HttpResponseRedirect(reverse("title", args=[random_entry]))

    



