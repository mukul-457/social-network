from django.shortcuts import render, redirect, get_object_or_404
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