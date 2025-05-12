from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path("flights/<int:flight_id>/", views.flight_detail, name="flight_detail"),
    path("airport_detail/<int:airport_id>/", views.airport_detail, name="airport_detail"),
    path('profile/', views.profile_view, name='profile'),

# RESTfull 
    path('profile/api/', views.profile_api, name='profile_api'),
    path('profile/api/update/', views.profile_update_api, name='profile_upd'),
    path('profile/api/bookings/<str:booking_code>/', views.booking_details_api, name='booking_details_api'),
    path('api/bookings/create/', views.create_booking_api, name='create_booking_api'),
]
