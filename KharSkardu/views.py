from django.shortcuts import render
from adminportal.models import Room, Booking, Images, GalleryImage,Post
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def emailmanager(context):
    

    
    subject = 'Your Booking Confirmation - Khar Traditional Hotel'
    from_email = 'fkprogrammer12@gmail.com'
    to = ['fkprogrammer12@gmail.com']
    context

    html_content = render_to_string('email/booking_confirmation.html', context)
    text_content = 'Thank you for your booking!'  # fallback plain text

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    msg.send()

# Create your views here.
def tags():
    tag= [ "Skardu hotels",
    "Hotel Skardu",
    "Skardu accommodation",
    "Skardu traditional hotel",
    "Khar Hotel Skardu",
    "Khar Traditional Building",
    "Traditional hotel Pakistan",
    "Heritage hotel Skardu",
    "Cultural stay Skardu",
    "Authentic Skardu experience",
    "Best hotels Skardu",
    "Hotels in Skardu",
    "Luxury hotels Skardu",
    "Budget hotels Skardu",
    "Skardu guesthouses",
    "Skardu resorts",
    "Stay in Skardu",
    "Skardu tourism",
    "Visit Skardu",
    "Travel Skardu",
    "Northern Areas Pakistan hotels",
    "Gilgit Baltistan hotels",
    "Mountain view hotel Skardu",
    "Indus River view Skardu hotel",
    "Skardu Fort nearby hotel",
    "Shangrila Resort Skardu proximity",
    "K2 base camp trek accommodation",
    "Satpara Lake hotels",
    "Deosai Plains accommodation",
    "Traditional architecture hotel",
    "Wooden hotel Skardu",
    "Stone building hotel",
    "Historic hotel Skardu",
    "Local experience hotel Skardu",
    "Family hotel Skardu",
    "Couple friendly Skardu hotel",
    "Solo travel Skardu accommodation",
    "Adventure tourism Skardu",
    "Trekking hotels Skardu",
    "Skardu valley hotels"]
    print(tag)
    return tag
def home(request):
    rooms=Room.objects.all()
    gallery=GalleryImage.objects.all()
    room_list = []
    blogs=Post.objects.all()
    


    for room in rooms:
        
        # Get sorted images
        images = room.images.all().order_by('image_number')

        # Build dictionary for each room
        room_data = {
            'id': room.id,
            'title': room.title,
            'room_type': room.room_type,
            'price': float(room.price),
            'is_available': room.is_available,
            'description': room.description,
            'images': [img.image.url for img in images]  # list of image URLs
        }
        room_list.append(room_data)
    actualist=[]
    room_groups = {}
    for room in room_list:
        if room['title'] not in room_groups:
            room_groups[room['title']] = room  # take the first available room for this title

    # Take only the first two groups (two titles)
    selected_rooms = list(room_groups.values())[:2]
        
    

    return render(request, 'app/home.html',{
        'rooms':selected_rooms,
        'gallery':gallery,
        'tags':tags(),
        'blogs':blogs,
    })
from django.db.models import Q

def booking(request):
    if request.method == 'GET':
        try:
            checkin = request.GET.get('checkin')
            checkout = request.GET.get('checkout')
        except:
            messages.error(request,'Please Fill  a correct Date')
        available_rooms = Room.objects.all()  # Default to all rooms
        from datetime import datetime
        check_in = datetime.strptime(checkin, "%Y-%m-%d").date()
        check_out = datetime.strptime(checkout, "%Y-%m-%d").date()

        # Rooms that have overlapping bookings
        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).values_list("room_id", flat=True)

        # Exclude booked rooms
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        not_checkedoutrooms=Room.objects.filter()
        rooms=[
            {
                'id': room.id,
                'title': room.title,
                'description': room.description,
                'price': room.price,
                'room_type': room.room_type,
                'image_url': room.images.first().image.url if room.images.exists() else None
            } for room in available_rooms
        ]
        room_groups = {}
    for room in rooms:
        if room['title'] not in room_groups:
            room_groups[room['title']] = room

    selected_rooms = list(room_groups.values())[:2]

    return render(request, 'app/booking.html', {
        'available_rooms': selected_rooms,
        'checkin': check_in,
        'checkout': check_out
    })
def explore(request):
    return render(request, 'app/explore.html')
# createbooking_app
from datetime import datetime
from django.shortcuts import redirect
from django.urls import reverse
from datetime import timedelta

def is_room_available_by_night(room, check_in_date, check_out_date):
    """
    Checks if a room is available by ensuring no requested 'nights' are already booked.

    Args:
        room (Room): The room instance to check.
        check_in_date (date): The desired check-in date (first night).
        check_out_date (date): The desired check-out date (the morning after the last night).

    Returns:
        bool: True if all requested nights are available, False otherwise.
    """
    # An existing booking is a conflict if its occupied nights overlap with the requested nights.
    # The 'nights' for an existing booking are from its check_in date up to the day before its check_out date.
    # The most efficient way to query for this is to find any booking that:
    # 1. Starts before the new booking's last night ends (i.e., before the new check_out date).
    # 2. Ends after the new booking's first night begins (i.e., after the new check_in date).
    conflicting_bookings = Booking.objects.filter(
        room=room,
        check_in__lt=check_out_date,
        check_out__gt=check_in_date
    )
    print(conflicting_bookings)

    # If this query finds ANY booking, it means there's a night conflict.
    # The function should return True if no conflicts are found.
    return  conflicting_bookings.exists()
def createbooking_app(request):
    if request.method == 'POST':
        try:
            room_id = request.POST.get('room_id')
            check_in_date = request.POST.get('check_in_date')
            check_out_date = request.POST.get('check_out_date')
            full_name = request.POST.get('full_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone_number')
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()

            room = Room.objects.get(id=room_id)
        except Room.DoesNotExist:
            return render(request, 'app/booking.html', {
                'error_message': 'Room not found.'
            })


        # Correct and simplified availability check
        

        if is_room_available_by_night(room, check_in, check_out):
            # This logic will now correctly handle back-to-back bookings.
            # If it still triggers, it means there's a different, genuinely overlapping booking.
           
            return render(request, 'app/booking.html', {
                'error_message': 'Sorry, this room is already booked for the selected dates.'
            })
       
        booking=Booking.objects.create(
            room=room,
            check_in=check_in,
            check_out=check_out,
            name=full_name,
            email=email,
            phone=phone,
            status="Pending",
            booked_by="Website User"
        )
        price=0
        number_of_nights = (booking.check_out - booking.check_in).days
        price=number_of_nights*room.price
        try:
            emailto=emailmanager({
                'guest':booking.name,
                'guest_no':phone,
                'checkin':check_in,
                'checkout':check_out,
                'confirmlink': request.build_absolute_uri(f'/confirmbooking/{booking.id}/'),
                'declinelink': request.build_absolute_uri(f'/declinebooking/{booking.id}/'),

            })
        except:
            pass


        
        request.session['booking_details'] = {
            "refNumber": f"KHAR-{booking.id:05d}",
            "guestName": booking.name,
            "checkinDate": str(booking.check_in),
            "checkoutDate": str(booking.check_out),
            "roomName": room.title,
            "totalAmount": f"{price} PKR",
            "hotelName": "Khar Skardu Hotel",
            "hotelAddress": "Skardu, Pakistan",
            "hotelContact": "+92 339 1119555"
        }

        # ✅ Redirect to success page
        return redirect(reverse('booking_success'))
    return redirect('home')
def booking_success(request):
    details = request.session.get('booking_details')
    if not details:
        return redirect('createbooking_app')  # if accessed directly

    # Optional: clear session after showing success
    del request.session['booking_details']
    return render(request, 'app/booking_success.html', {'details': details})
# login

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
def login_view(request):
    # redirect if already logged in
    if request.user.is_authenticated:
        return redirect('admin-home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin-home')  # Redirect to a success page.
        else:
            error_message = "Invalid username or password."
            return render(request, 'app/login.html', {'error_message': error_message})
    return render(request, 'app/login.html')
# import messsage
from django.contrib import messages
def confirm_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "Confirmed"
        booking.save()
        messages.success(request, "Booking has been confirmed.")

        return redirect('admin-home')
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('admin-home')
        
def decline_booking(request, booking_id):
    try:
        booking = Booking.objects.get(id=booking_id)
        booking.status = "Declined"
        booking.save()
        booking.delete()
        messages.success(request, "Booking has been declined.")
        return redirect('admin-home')
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('admin-home') 
def blogs(request,id):
    post=Post.objects.get(id=id)
    tagss=post.tags.split(',')
    return render(request, 'app/blogview.html',{
        'post':post,
        'tags':tagss,
    })