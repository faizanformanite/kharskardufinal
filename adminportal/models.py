from django.db import models

# Create your models here.
class Images(models.Model):
    image = models.ImageField(upload_to='room_images/')
    image_number=models.IntegerField(default=0)
    
    def __str__(self):
        return self.image.url
class GalleryImage(models.Model):
    title = models.CharField(max_length=100, default="Image Title")
    image = models.ImageField(upload_to='gallery_images/')

class Room(models.Model):
    title = models.CharField(max_length=100, default="Room Title")
    room_type = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    images = models.ManyToManyField('Images', blank=True)
    description = models.TextField()
    room_no = models.CharField(max_length=10, default="101",)

    

    def __str__(self):
        return f'Room {self.title} - {self.room_type} ({self.room_no})'
    def floor(self):
        try:
            floor_number = int(self.room_no) // 100
            if floor_number == 1:
                return "1st Floor"
            elif floor_number == 2:
                return "2nd Floor"
            elif floor_number == 3:
                return "3rd Floor"
            else:
                return f"{floor_number}th Floor"
        except ValueError:
            return None

    

    

class Booking(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True,null=True)
    phone = models.CharField(max_length=15)
    check_in = models.DateField()
    check_out = models.DateField()
    room = models.ForeignKey(Room, on_delete=models.SET_DEFAULT, blank=True, default=None)
    booked_on = models.DateTimeField(auto_now_add=True)
    booked_by = models.CharField(max_length=100, default="Admin")
    status = models.CharField(max_length=100, default="confirmed",null=True,blank=True)
    
    
    def checkedin(self):
        if self.status  == 'Checked In':
            return True
        return False
    def checkedout(self):
        if self.status == 'Checked Out':
            return True
        return False
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Post(models.Model):
    title = models.CharField(max_length=200)
    
    # Use RichTextField instead of a standard TextField
    content = RichTextField(blank=True, null=True)
    # ImageField requires Pillow to be installed
    featured_image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
