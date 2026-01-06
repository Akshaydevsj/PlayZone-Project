from django.urls import path
from . import views

urlpatterns = [

    path('turfs/',views.TurfBookingListView.as_view(), name='turf-list'),

    path('turf/<uuid:uuid>/',views.TurfBookingDetailView.as_view(), name='turf-detail'),

    path('turf/<uuid:uuid>/book/',views.CreateTurfBookingView.as_view(), name='create-turf-booking'),

]
