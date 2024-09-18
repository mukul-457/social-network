from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import ImageCreateForm
from django.contrib import messages
from .models import Image
# Create your views here.


def image_create(request):
    if request.method == "POST":
        save_form = ImageCreateForm(request.POST)
        if save_form.is_valid:
            image = save_form.save(commit=False)
            image.user = request.user
            image.save()
            messages.success(request, "Image added successfully")
        return redirect(image.get_absolute_url())
    else:
        save_form = ImageCreateForm(request.GET)
        return render(request, "images/image/create.html",{"section": "images", "form":save_form})


def image_details(request, id, slug ):
    image  = get_object_or_404(Image, id=id ,slug =slug)
    return render(request, "images/image/details.html" , {'section': 'images','image':image})


@login_required
@require_POST
def image_like(request):
    iid = request.POST.get("id")
    action = request.POST.get("action")
    if iid and action :
        try:
            image  = Image.objects.get(id= iid)
            if action == "like":
                image.liked_by_users.add(request.user)
            else:
                image.liked_by_users.remove(request.user)
            return JsonResponse({"status": "ok"})
        except Image.DoesNotExist:
            pass
        return JsonResponse({"status": "error"})
    


