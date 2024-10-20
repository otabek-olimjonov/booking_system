from django.urls import path
from .views import (
    book_parking_spot,
    make_available,
    payment,
    toggle_door,
    get_parking_spots_status,
)

urlpatterns = [
    path('book/<int:spot_number>/', book_parking_spot, name='book_parking_spot'),
    path('available/<int:spot_number>/', make_available, name='make_available'),  # New path for making available
    path('toggle_door/<int:spot_number>/', toggle_door, name='toggle_door'),      # New path for toggling door
    path('status/', get_parking_spots_status, name='get_parking_spots_status'),
    path('payment/', payment, name='payment'),
]
