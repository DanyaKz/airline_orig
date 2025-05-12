from django.shortcuts import redirect, render, get_object_or_404
from .models import Flight, Airport, Passenger, Booking
from .forms import LoginForm , RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

# регистрация 
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            Passenger.objects.create(user=user)
            login(request, user)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'flights/register.html', {'form': form})

# логин
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "Неверный логин или пароль")
    else:
        form = LoginForm()
    return render(request, 'flights/login.html', {'form': form})

# логаут
def logout_view(request):
    logout(request)
    return redirect('/')

# главная страница
def index(request):
    flights = Flight.objects.all()
    airports = Airport.objects.all() 
    return render(request, "flights/index.html", {"flights": flights, "airports":airports})

# детализированно о рейсе (бронь и просмотр)
def flight_detail(request, flight_id):
    flight = get_object_or_404(Flight, pk=flight_id)
    return render(request, "flights/flight_detail.html", {"flight": flight})

@login_required
@require_http_methods(["POST"])
def create_booking_api(request):
    data = json.loads(request.body)
    flight_id = data.get('flight_id')

    try:
        flight = Flight.objects.get(id=flight_id)
    except Flight.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Рейс не найден."}, status=404)

    if flight.capacity == 0:
        return JsonResponse({"status": "error", "message": "Мест на рейсе больше нет."}, status=400)

    booking = Booking.objects.create(
        passenger=request.user,
        flight=flight
    )

    flight.capacity -= 1
    flight.save()

    return JsonResponse({
        "status": "success",
        "message": "Бронирование успешно создано!",
        "booking_code": booking.booking_code,
        "cap":flight.capacity
    }, status=201)


# информация аэропорта
def airport_detail(request, airport_id):
    airport = get_object_or_404(Airport, pk=airport_id)
    departures = Flight.objects.filter(origin=airport)
    arrivals = Flight.objects.filter(destination=airport)
    return render(request, "flights/airport_detail.html", {"airport": airport, "departures": departures, "arrivals": arrivals})


# профиль юзера
@login_required
def profile_view(request):
    return render(request, 'flights/profile.html')


# апи юзера
@login_required
@require_http_methods(["GET"])
def profile_api(request):
    passenger = get_object_or_404(Passenger, user=request.user)
    bookings = Booking.objects.filter(passenger=request.user)

    data = {
        "username":request.user.username,
        "first_name": request.user.first_name,
        "last_name": request.user.last_name,
        "passport_number": passenger.passport_number or "",
        "phone_number": passenger.phone_number or "",
        "bookings": [
            {
                "origin": booking.flight.origin.city,
                "destination": booking.flight.destination.city,
                "duration": booking.flight.duration,
                "booking_code": booking.booking_code
            }
            for booking in bookings
        ]
    }
    return JsonResponse(data)

# обновление профиля
@login_required
@require_http_methods(["PATCH"])
def profile_update_api(request):
    data = json.loads(request.body)

    request.user.first_name = data.get('first_name', request.user.first_name)
    request.user.last_name = data.get('last_name', request.user.last_name)
    request.user.save()

    passenger = get_object_or_404(Passenger, user=request.user)
    passenger.passport_number = data.get('passport_number', passenger.passport_number)
    passenger.phone_number = data.get('phone_number', passenger.phone_number)
    passenger.save()

    return JsonResponse({"status": "success", "message": "Профиль успешно обновлён!"})


def booking_details_api(request, booking_code):
    booking = get_object_or_404(Booking, booking_code=booking_code)
    data = {
        "origin": booking.flight.origin.city,
        "destination": booking.flight.destination.city,
        "duration": booking.flight.duration,
        "passenger_name": booking.passenger.first_name + " " + booking.passenger.last_name,
        "passenger_email": booking.passenger.email
    }
    return JsonResponse(data)


