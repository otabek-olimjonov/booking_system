# tasks.py
from celery import shared_task
from .models import ParkingSpot, Payment

@shared_task
def cancel_booking(spot_number):
    try:
        parking_spot = ParkingSpot.objects.get(number=spot_number)
        if parking_spot.status == 'booked':
            parking_spot.status = 'free'
            Payment.objects.create(amount=5, user=parking_spot.booked_by)
            parking_spot.booked_by = None  # Clear the booking
            parking_spot.save()
            
            print(f'Booking for spot {spot_number} has been canceled due to timeout.')
    except ParkingSpot.DoesNotExist:
        print(f'Spot {spot_number} does not exist.')


@shared_task
def close_door_after_delay(spot_number):
    try:
        parking_spot = ParkingSpot.objects.get(number=spot_number)
        if parking_spot.door:  # If the door is still open, close it
            parking_spot.door = False
            parking_spot.save()
            print(f'Door for spot {spot_number} has been automatically closed after delay.')
    except ParkingSpot.DoesNotExist:
        print(f'Spot {spot_number} does not exist.')