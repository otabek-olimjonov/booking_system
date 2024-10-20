from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from parking.tasks import cancel_booking, close_door_after_delay
from .models import ParkingSpot, Payment
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='/users/login/')  # Use your actual login URL here
def home(request):
    parking_spots = ParkingSpot.objects.all() 
    user_payments = Payment.objects.filter(user=request.user)
    total_balance = sum(payment.amount for payment in user_payments)
    return render(request, 'parking/parking.html', {'user': request.user, 'parking_spots': parking_spots, "balance": f'${total_balance}'})

@login_required(login_url='/users/login/')
def get_parking_spots_status(request):
    spots = ParkingSpot.objects.all()
    data = [
        {
            'number': spot.number,
            'status': spot.status,
            'booked_by': spot.booked_by.username if spot.booked_by else None,  # Username of the person who booked
            'in_use_by': spot.booked_by.username if spot.status == 'in_use' else None,  # Username of person using it
            'door': spot.door
        }
        for spot in spots
    ]
    return JsonResponse({'parking_spots': data})

@login_required(login_url='/users/login/')
@csrf_exempt
def book_parking_spot(request, spot_number):
    if request.method == 'POST':
        try:
            # Check if the user already has a booked spot
            existing_booking = ParkingSpot.objects.filter(booked_by=request.user,  status__in=['booked', 'in_use']).exists()

            if existing_booking:
                return JsonResponse({'status': 'error', 'message': 'You have already booked a parking spot.'})

            parking_spot = ParkingSpot.objects.get(number=spot_number)
            if parking_spot.status == 'free':
                parking_spot.status = 'booked'
                parking_spot.booked_by = request.user  # Set the user who booked
                Payment.objects.create(amount=-5, user=request.user)
                parking_spot.save()

                # Schedule the cancel_booking task to run after 20 minutes
                cancel_booking.apply_async((spot_number,), countdown=10)  # 1200 seconds = 20 minutes

                return JsonResponse({'status': 'success', 'message': 'Parking spot booked!'})
            return JsonResponse({'status': 'error', 'message': 'Spot is not available.'})
        except ParkingSpot.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Spot does not exist.'})

@login_required(login_url='/users/login/')  # Protecting the available view
@csrf_exempt
def make_available(request, spot_number):
    if request.method == 'POST':
        try:
            parking_spot = ParkingSpot.objects.get(number=spot_number)
            # Check if the user is the one who booked the spot
            if parking_spot.booked_by == request.user and (parking_spot.status == 'in_use' or parking_spot.status == 'booked'):
                parking_spot.status = 'free'
                parking_spot.door = False  # Close the door when available
                Payment.objects.create(amount=5, user=parking_spot.booked_by)
                parking_spot.booked_by = None  # Clear who booked it
                parking_spot.save()
                return JsonResponse({'status': 'success', 'message': 'Parking spot is now available!'})
            return JsonResponse({'status': 'error', 'message': 'Spot is not in use or not booked by you.'})
        except ParkingSpot.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Spot does not exist.'})

@login_required(login_url='/users/login/')  # Protecting the toggle door view
@csrf_exempt
def toggle_door(request, spot_number):
    if request.method == 'POST':
        try:
            parking_spot = ParkingSpot.objects.get(number=spot_number)

            # Check if the user is the one who booked the spot
            if parking_spot.booked_by == request.user:
                # Toggle door status
                if not parking_spot.door:  # Door is currently closed
                    parking_spot.door = True  # Open the door
                    if parking_spot.status == 'booked':
                        parking_spot.status = 'in_use'  # Mark as in use when door opens

                    elif parking_spot.status == 'in_use':
                        parking_spot.status = 'free'  # Mark as available when door is opened
                        parking_spot.booked_by = None  # Clear who booked it

                    # Schedule the door to close automatically after 20 seconds
                    close_door_after_delay.apply_async((spot_number,), countdown=5)

                parking_spot.save()

                return JsonResponse({'status': 'success', 'door_open': parking_spot.door, 'current_status': parking_spot.status})
            return JsonResponse({'status': 'error', 'message': 'You cannot toggle the door for this spot.'})
        except ParkingSpot.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Spot does not exist.'})


@csrf_exempt
@login_required(login_url='/users/login/')
def payment(request):
    if request.method == 'GET':
        # Render the payment HTML page
        user_payments = Payment.objects.filter(user=request.user)
        total_balance = sum(payment.amount for payment in user_payments)
        context = {
            "balance": f'${total_balance}'
        }
        return render(request, 'parking/payment.html', context)

    elif request.method == 'POST':
        action = request.POST.get('action')
        amount = int(request.POST.get('amount', 0))

        if action == 'deposit':
            # Handle deposit
            Payment.objects.create(amount=amount, user=request.user)
            new_balance = sum(payment.amount for payment in Payment.objects.filter(user=request.user))
            return JsonResponse({"message": "Deposit successful", "new_balance": new_balance})

        elif action == 'pay':
            # Handle payment
            total_balance = sum(payment.amount for payment in Payment.objects.filter(user=request.user))
            if total_balance >= amount:
                Payment.objects.create(amount=-amount, user=request.user)
                new_balance = total_balance - amount
                return JsonResponse({"message": "Payment successful", "new_balance": new_balance})
            else:
                return JsonResponse({"error": "Insufficient funds"}, status=400)

    # If the request method is not GET or POST
    return JsonResponse({"error": "Invalid request method"}, status=405)
