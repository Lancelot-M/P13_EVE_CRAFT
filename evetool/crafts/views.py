import json
from django.shortcuts import render
from crafts.forms import CraftForm
from crafts.services import Services
from django.http import QueryDict
# from crafts.services import Services

def home(request):
    """Tool home page."""
    if request.method == 'GET':
        form = CraftForm()
        return render(request, "crafts/research.html", {"form": form})
    elif request.method == "POST":
        f = CraftForm(request.POST)
        if f.is_valid():
            service = Services()
            data = service.make_list(f)
        return render(request, "crafts/research.html", {"form": f, "data": data})

def info(request):
    """Production detail page"""
    
    if request.method == 'POST':
        form = QueryDict(query_string=request.POST["form"], mutable=True)
        f = CraftForm(form)
        if f.is_valid():
            data = {
                "form": f,
                "item": request.POST["item"]
            }
            service = Services()
            data = service.show_info(data)
            return render(request, "crafts/info.html", {
                "form": f,
                "data": data
            })
    else:
        print("POUIC!")
        form = CraftForm()
        return render(request, "crafts/research.html", {"form": form})