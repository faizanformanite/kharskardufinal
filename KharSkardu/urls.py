"""
URL configuration for KharSkardu project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('kharadmin/', include('adminportal.urls')),
    path('', views.home, name='home'),
    path('booking/', views.booking, name='booking'),
    path('explore/', views.explore, name='explore'),
    # createbooking_app
    path('createbooking_app/', views.createbooking_app, name='createbooking_app'),
    # login
    path('login/', views.login_view, name='login'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('confirmbooking/<int:booking_id>/', views.confirm_booking, name='confirm_booking'),
    path('declinebooking/<int:booking_id>/', views.decline_booking, name='decline_booking'),
    # blogview
    path('blogview/<int:id>/', views.blogs, name='blogview'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
