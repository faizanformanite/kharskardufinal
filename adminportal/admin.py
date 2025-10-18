from django.contrib import admin
from .models import Room, Booking, Images,GalleryImage,Post
# Register your models here.
admin.site.register(Room)
admin.site.register(Booking)
admin.site.register(Images)
admin.site.register(GalleryImage)
admin.site.register(Post)