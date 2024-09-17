from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    url  = models.URLField(max_length=2000)
    description = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name="saved_images",on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    liked_by_users = models.ManyToManyField(User, related_name="liked_images",blank=True)
    class Meta:
        indexes = [
            models.Index(fields= ["-created"])
        ]
        ordering = ["-created"]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("images:detail", args=[self.id,self.slug])
    
