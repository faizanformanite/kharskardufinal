from django.shortcuts import render
from .models import Room, Booking, Images,GalleryImage
# Create your views here.
# import messages
# login required decorator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
@login_required
def saveroom(id,request):
    room = Room.objects.get(id=id)
    room.title=request.POST.get('title')
    room.description=request.POST.get('desc')
    room.price=request.POST.get('price')
    room.room_type=request.POST.get('room_type')
    for img in request.FILES.getlist('imageFile'):
        image = Images.objects.create(image=img)
        room.images.add(image)
    room.save()

def createRoom(request):
    title = request.POST.get('title')
    description = request.POST.get('desc')
    price = request.POST.get('price')
    room_type = request.POST.get('room_type')
    room = Room.objects.create(title=title, description=description, price=price, room_type=room_type)
    print(request.FILES.get('imageFile'))
    for img in request.FILES.getlist('imageFile'):
        print(img)
        image = Images.objects.create(image=img)
        room.images.add(image)

    print(request.FILES)
    room.save()

def createbooking(data):
    room=Room.objects.get(id=data['room_id'])
    check_in = datetime.datetime.strptime(data['checkin_date'], '%Y-%m-%d').date()
    check_out = datetime.datetime.strptime(data['checkout_date'], '%Y-%m-%d').date()
    # check if the room is booked for that date
    existing_booking = Booking.objects.filter(
        room=room,
        check_in__lt=check_out,
        check_out__gt=check_in
    ).first()
    if existing_booking:
        return False  # or handle the error as needed
    booking=Booking.objects.create(
        name=data['guest_name'],
        phone=data['phone'],
        email=data['email'],
        check_in=check_in,
        check_out=check_out,

        room=room,
        booked_by='Admin'

    )
    return booking

from django.utils import timezone
@login_required
def home(request):

    today = timezone.localdate()
    bookings = Booking.objects.all().order_by('-booked_on')

    booking_data = []
    for booking in bookings:
        
            
        if booking.status == 'Pending':
            status='Pending'
            action='pending'
            color='green'

        elif booking.check_in == today:
            status = "Expected Check-in Today"
            action = "Check In"
            color = "blue"
        elif booking.check_out == today:
            status = "Expected Check-out Today"
            action = "Check Out"
            color = "yellow"
        elif booking.check_in > today:
            status = "Upcoming"
            action = "N/A"
            color = "gray"
        elif booking.check_out < today:
            status = "Completed"
            action = "N/A"
            color = "green"
        else:
            status = "Active"
            action = "N/A"
            color = "orange"

        booking_data.append({
            "id": booking.id,
            "name": booking.name,
            "room": booking.room.title if booking.room else "N/A",
            "check_in": booking.check_in,
            "check_out": booking.check_out,
            "status": status,
            "action": action,
            'checkedin':booking.checkedin(),
            'checkedout':booking.checkedout(),
            'refNumber': f"KHAR-{booking.id:05d}",
            'room_no': booking.room.room_no if booking.room else "N/A",

            "color": color,
        })
    return render(request, 'adminportal/home.html',{
        'bookings':booking_data,
        'selected':'bookings',
        'today':today
    })
import datetime
@login_required
def rooms(request):
    rooms = Room.objects.all()

    if request.method == 'POST':
        
        if request.POST.get('add') == 'add':
            createRoom(request)

            messages.success(request, 'Room created successfully.',)
            return render(request, 'adminportal/rooms.html', {'rooms': rooms})
        elif request.POST.get('edit') == 'edit':
            saveroom(request.POST.get('room_id'),request)
            messages.success(request, 'Room updated successfully.',)
            return render(request, 'adminportal/rooms.html', {'rooms': rooms})
    room_groups={}
    for room in rooms:
        if room.title not in room_groups:
            room_groups[room.title] = room  # take the first available room for this title

    # Take only the first two groups (two titles)
    selected_rooms = list(room_groups.values())[:2]
    actual_rooms=[]
    for room in rooms:
        today = datetime.date.today()

        # Check for today's booking (where today is between check_in and check_out)
        today_booking = Booking.objects.filter(
            room=room,
            check_in__lte=today,
            check_out__gte=today
        ).first()

        # If no booking today, check for the next upcoming booking (after today)
        next_booking = None
        if not today_booking:
            next_booking = Booking.objects.filter(
                room=room,
                check_in__gt=today
            ).order_by('check_in').first()

        if today_booking:
            booking_status = 'Booked Today'
            guest_name = today_booking.name
            checkout_date = today_booking.check_out
        elif next_booking:
            booking_status = f'Next Booking'
            guest_name = next_booking.name
            checkin=next_booking.check_in
            checkout_date = next_booking.check_out
        else:
            booking_status = 'Available'
            guest_name = ''
            checkout_date = ''
        willcheckout=False
        if today_booking and today_booking.check_out == today:
            willcheckout = True
        actual_rooms.append({
            'id': room.id,
            'title': room.title,
            'description': room.description,
            'price': room.price,
            'room_type': room.room_type,
            'room_no': room.room_no,
            'status': booking_status,
            'guest_name': guest_name,
            'checkout_date': checkout_date,
            'willcheckout': willcheckout,
            'checkin': checkin if next_booking else '',
            'checkedin': today_booking.checkedin() if today_booking else False,
            'checkedout': today_booking.checkedout() if today_booking else False,
            'floor': room.floor() if room.floor() else '1st Floor'
        })

            

    return render(request, 'adminportal/rooms.html', {'roomshow': selected_rooms,'selected':'rooms','rooms':actual_rooms})
@login_required
def gallery(request):
    if request.method == "POST":
        image=GalleryImage.objects.create(title=request.POST.get('title'),image=request.FILES.get('image'))
    galleryImages=GalleryImage.objects.all()

    return render(request, 'adminportal/gallery.html',{
        'gallery':galleryImages,
        'selected':'gallery'
    })

from django.http import JsonResponse
from django.db.models import Q
import json
def checkAvailability(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        check_in = data['checkin']
        check_out = data['checkout']
        
        available_rooms = Room.objects.all()
        from datetime import datetime
        check_in = datetime.strptime(check_in, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out, "%Y-%m-%d").date()

        # Rooms that have overlapping bookings
        booked_rooms = Booking.objects.filter(
            Q(check_in__lt=check_out) & Q(check_out__gt=check_in)
        ).values_list("room_id", flat=True)

        # Exclude booked rooms
        available_rooms = Room.objects.exclude(id__in=booked_rooms)
        
            

        rooms=[
            {
                'id': room.id,
                'title': room.title,
                'description': room.description,
                'price': room.price,
                'room_type': room.room_type,
                'room_no':room.room_no,
                'image_url': room.images.first().image.url if room.images.exists() else None
            } for room in available_rooms
        ]
        return JsonResponse({'rooms': rooms,'status': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)
import json
def book(request):
    if request.method == 'POST':
        data=json.loads(request.body)
        booking=createbooking(data)
        if not booking:
            return JsonResponse({'error': 'Room is already booked for the selected dates.'}, status=400)
        messages.success(request, f'Booking for {booking.name} has been created successfully.',)

        return JsonResponse({'success': 'success'}, status=200)
    return JsonResponse({'error': 'Invalid request method.'}, status=400)


# reverse and redirect
from django.urls import reverse
from django.shortcuts import redirect


def add_booking_admin_room_wise(request):
    if request.method == 'POST':
        room=Room.objects.get(room_no=request.POST.get('room_no'))
        
        # double check if the room is booked for that date

        check_in = datetime.datetime.strptime(request.POST.get('checkin_date'), '%Y-%m-%d').date()
        check_out = datetime.datetime.strptime(request.POST.get('checkout_date'), '%Y-%m-%d').date()
        overlapping_bookings = Booking.objects.filter(
            room=room,
            check_in__lt=check_out,
            check_out__gt=check_in
        )
        if overlapping_bookings.exists():
            messages.error(request, f'Room {room.room_no} is already booked for the selected dates.',)
            return redirect(reverse('admin-rooms'))
        booking=Booking.objects.create(
            name=request.POST.get('guest_name'),
            phone=request.POST.get('guest_number'),
            check_in=check_in ,
            check_out=check_out,
            room=room,
            booked_by='Admin'
        )
        
        details = {
        "refNumber": f"KHAR-{booking.id:05d}",
        "guestName": booking.name,
       "checkinDate": booking.check_in.strftime('%Y-%m-%d'),
            "checkoutDate": booking.check_out.strftime('%Y-%m-%d'),
        "roomName": room.title,
        "totalAmount": f"{room.price} PKR",
        "hotelName": "Khar Skardu Hotel",
        "hotelAddress": "Skardu, Pakistan",
        "hotelContact": "+92 339 1119555"
        }
        request.session['admin_booking_details'] = details
        messages.success(request, f'Booking for {booking.name} has been created successfully.',)

        # ✅ Redirect to success page (prevents form resubmission)
        return redirect(reverse('admin_booking_success'))
        
    return rooms(request)
def admin_booking_success(request):
    details = request.session.get('admin_booking_details')
    if not details:
        return redirect('admin-rooms')  # redirect if accessed directly

    # Optional: clear session after use
    del request.session['admin_booking_details']
    return render(request, 'adminportal/booking_confirmation.html', {'details': details})
def checkin(request,id):
    booking=Booking.objects.get(id=id)
    booking.status='Checked In'
    booking.save()
    messages.success(request, f'Guest {booking.name} has been checked in successfully.',)
    return JsonResponse({'success': 'success'}, status=200)

def checkout(request,id):
    booking=Booking.objects.get(id=id)
    booking.status='Checked Out'
    booking.save()
    messages.success(request, f'Guest {booking.name} has been checked out successfully.',)
    return JsonResponse({'success': 'success'}, status=200)
def download_ticket(request, id):
    booking = Booking.objects.get(id=id)
    room = booking.room
    days=(booking.check_out - booking.check_in).days
    if days==0:
        days=1
        total_amount = room.price * days if room else 0
    else:
        total_amount = room.price * days if room else 0

    details = {
        "refNumber": f"KHAR-{booking.id:05d}",
        "guestName": booking.name,
        "checkinDate": booking.check_in,
        "checkoutDate": booking.check_out,
        "roomName": room.title if room else "N/A",
        "totalAmount": f"{total_amount} PKR" if room else "N/A",
        "hotelName": "Khar Skardu Hotel",
        "hotelAddress": "Skardu, Pakistan",
        "hotelContact": "+92 339 1119555"
    }
    
    return JsonResponse({'success': 'success', 'details': details}, status=200)