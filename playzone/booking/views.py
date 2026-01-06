from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from turf.models import Turf
from .models import TurfBooking
from datetime import datetime, timedelta, time

class TurfBookingListView(View):

    template_name = 'booking/turf-list.html'

    def get(self, request):

        turfs = Turf.objects.filter(is_approved=True, active_status=True)

        return render(request, self.template_name, {
            'turfs': turfs
        })


class TurfBookingDetailView(View):

    template_name = 'booking/turf-detail.html'

    def get(self, request, uuid):

        turf = get_object_or_404(Turf, uuid=uuid, is_approved=True)

        return render(request, self.template_name, {
            'turf': turf
        })


class CreateTurfBookingView(LoginRequiredMixin, View):

    login_url = 'login'

    def post(self, request, uuid):

        turf = get_object_or_404(Turf, uuid=uuid, is_approved=True)

        booking_date = request.POST.get('booking_date')
        start_time   = request.POST.get('start_time')
        end_time     = request.POST.get('end_time')

        start = datetime.strptime(start_time, '%H:%M').time()
        end   = datetime.strptime(end_time, '%H:%M').time()

        start_dt = datetime.combine(datetime.today(), start)
        end_dt   = datetime.combine(datetime.today(), end)

        total_hours = int((end_dt - start_dt).seconds / 3600)

        if total_hours < 1 or total_hours > 12:
            messages.error(request, 'Booking must be between 1 and 12 hours')
            return redirect('turf-booking-detail', uuid=uuid)

        # ================== TIME CONFLICT CHECK ==================
        conflict = TurfBooking.objects.filter(
            turf=turf,
            booking_date=booking_date,
            start_time__lt=end,
            end_time__gt=start
        ).exists()

        if conflict:
            messages.error(
                request,
                'Selected time slot is already booked. Please choose another time.'
            )
            return redirect('turf-booking-detail', uuid=uuid)

        # ================== PRICE CALCULATION ==================
        base_amount = 0
        light_charge = 0
        current_time = start

        for _ in range(total_hours):

            if time(18, 0) <= current_time or current_time < time(6, 0):
                light_charge += turf.light_extra_charge

            base_amount += turf.price_per_hour
            current_time = (datetime.combine(datetime.today(), current_time)
                            + timedelta(hours=1)).time()

        total_amount = base_amount + light_charge

        TurfBooking.objects.create(
            turf=turf,
            user=request.user,
            booking_date=booking_date,
            start_time=start,
            end_time=end,
            total_hours=total_hours,
            base_amount=base_amount,
            light_charge=light_charge,
            total_amount=total_amount
        )

        messages.success(request, 'Booking confirmed successfully')
        return redirect('turf-booking-detail', uuid=uuid)
