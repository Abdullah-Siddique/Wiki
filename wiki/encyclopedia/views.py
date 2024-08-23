from django.shortcuts import render, get_object_or_404, redirect
from markdown2 import Markdown
from . import util
import random
markdowner = Markdown()

def index(request):
    entries = util.list_entries()
    return render(request, "encyclopedia/index.html", {
        "entries": entries
    })
def entry_page(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/not_found.html", {"title": title})
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdowner.convert(entry)
    })
def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()
    results = [entry for entry in entries if query.lower() in entry.lower()]
    if len(results) == 1 and results[0].lower() == query.lower():
        return redirect('entry_page', title=results[0])
    return render(request, "encyclopedia/search_results.html", {
        "query": query,
        "results": results
    })
def create_page(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/create.html", {
                "error": "Page with this title already exists."
            })
        util.save_entry(title, content)
        return redirect('entry_page', title=title)
    return render(request, "encyclopedia/create.html")

def edit_page(request, title):
    entry = util.get_entry(title)
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return redirect('entry_page', title=title)
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry
    })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry_page', title=random_entry)

