from django.views import View

from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages

from django.utils.decorators import method_decorator

from .models import Turf

from .decorators import admin_required

from django.contrib.admin.views.decorators import staff_member_required

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import TurfOwnerSignupForm,TurfOwnerLoginForm

from .models import TurfOwner,Turf,TurfBooking


class TurfOwnerSignupView(View):

    template_name = 'turf/owner-signup.html'

    def get(self, request):

        form = TurfOwnerSignupForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = TurfOwnerSignupForm(request.POST)

        if not form.is_valid():

            return render(request, self.template_name, {'form': form})

        owner_name = form.cleaned_data['owner_name']

        email      = form.cleaned_data['email']

        phone      = form.cleaned_data['phone']

        username   = form.cleaned_data['username'] 

        password   = form.cleaned_data['password']

        user = User.objects.create_user(

                                        username=username,
                                        
                                        email=email,
                                        
                                        password=password
                                        
                                        )

        TurfOwner.objects.create(

                                user=user,

                                owner_name=owner_name,

                                email=email,

                                phone=phone,

                                account_holder_name=form.cleaned_data['account_holder_name'],

                                account_number=form.cleaned_data['account_number'],

                                ifsc_code=form.cleaned_data['ifsc_code'],

                                pan_number=form.cleaned_data['pan_number']

                                )

        messages.success(request,'Turf owner account created successfully. Please login.')

        return redirect('owner-login')





class TurfOwnerLoginView(View):

    template_name = 'turf/owner-login.html'

    def get(self, request):

        form = TurfOwnerLoginForm()

        return render(request, self.template_name, {'form': form})

    def post(self, request):

        form = TurfOwnerLoginForm(request.POST)

        if not form.is_valid():

            return render(request, self.template_name, {'form': form})

        username = form.cleaned_data['username'].upper().replace(' ', '')

        password = form.cleaned_data['password']

        user = authenticate(

                            request,
                            
                            username=username,
                            
                            password=password
                            
                            )

        if user is None:

            messages.error(request, 'Invalid turf username or password')

            return render(request, self.template_name, {'form': form})

        login(request, user)

        return redirect('owner-dashboard')




class TurfOwnerDashboardView(LoginRequiredMixin, View):
    template_name = 'turf/owner-dashboard.html'

    def get(self, request):
        owner = request.user.turf_owner

        turfs = Turf.objects.filter(owner=owner)

        return render(request, self.template_name, {
            'owner': owner,
            'turfs': turfs
        })






class TurfRegisterView(LoginRequiredMixin, View):

    template_name = 'turf/turf-register.html'

    def get(self, request):
        owner = request.user.turf_owner

        turf = Turf.objects.filter(owner=owner, is_denied=False).first()
        if turf:
            messages.error(request, 'You already registered a turf.')
            return redirect('owner-dashboard')

        return render(request, self.template_name)

    def post(self, request):
        owner = request.user.turf_owner

        Turf.objects.create(
            owner=owner,
            turf_name=request.POST.get('turf_name'),
            turf_image=request.FILES.get('turf_image'),
            city=request.POST.get('city'),
            address=request.POST.get('address'),
            landmark=request.POST.get('landmark'),
            google_map_link=request.POST.get('google_map_link'),
            games=request.POST.get('games'),
            ground_type=request.POST.get('ground_type'),
            price_per_hour=request.POST.get('price_per_hour'),
        )

        messages.success(
            request,
            'Turf registration submitted successfully. Please wait for admin approval.'
        )
        return redirect('owner-dashboard')





class ToggleBookingStatusView(LoginRequiredMixin, View):

    def get(self, request):

        turf = get_object_or_404(Turf, owner=request.user.turf_owner)

        turf.is_booking_open = not turf.is_booking_open

        turf.save()

        return redirect('owner-dashboard')


class OwnerProfileEditView(LoginRequiredMixin, View):
    template_name = 'turf/owner-profile-edit.html'

    def get(self, request):
        owner = request.user.turf_owner
        return render(request, self.template_name, {'owner': owner})

    def post(self, request):
        owner = request.user.turf_owner
        user = request.user

        user.username = request.POST.get('username')
        owner.email = request.POST.get('email')
        owner.phone = request.POST.get('phone')

        owner.account_holder_name = request.POST.get('account_holder_name')
        owner.account_number = request.POST.get('account_number')
        owner.ifsc_code = request.POST.get('ifsc_code')
        owner.pan_number = request.POST.get('pan_number')

        user.save()
        owner.save()

        messages.success(request, 'Profile updated successfully')
        return redirect('owner-dashboard')


class OwnerEditTurfView(LoginRequiredMixin, View):

    template_name = 'turf/owner-edit-turf.html'

    login_url = 'owner-login'

    def get(self, request, uuid):

        turf = get_object_or_404(

                                Turf,

                                uuid=uuid,

                                owner=request.user.turf_owner,

                                is_approved=True

                                )

        return render(request, self.template_name, {

                                                    'turf': turf,

                                                    })

    def post(self, request, uuid):

        turf = get_object_or_404(

                                Turf,

                                uuid=uuid,

                                owner=request.user.turf_owner,

                                is_approved=True

                                )

        turf.turf_name       = request.POST.get('turf_name')

        turf.city            = request.POST.get('city')

        turf.address         = request.POST.get('address')

        turf.landmark        = request.POST.get('landmark')

        turf.google_map_link = request.POST.get('google_map_link')

        turf.games           = request.POST.get('games')

        turf.ground_type     = request.POST.get('ground_type')

        turf.price_per_hour  = request.POST.get('price_per_hour')

        if request.FILES.get('turf_image'):

            turf.turf_image = request.FILES.get('turf_image')

        turf.save()

        messages.success(request, 'Turf details updated successfully')

        return redirect('owner-dashboard')




class OwnerDeleteTurfView(LoginRequiredMixin, View):

    login_url = 'owner-login'

    def get(self, request, uuid):

        turf = get_object_or_404 (
                                
                                Turf,

                                uuid=uuid,
                                
                                owner=request.user.turf_owner
                                
                                )

        turf.delete()

        messages.success(request, 'Turf deleted successfully')

        return redirect('owner-dashboard')



class TurfOwnerLogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('home')



class TurfApprovalDashboardView(LoginRequiredMixin, View):

    template_name = 'turf/turf-approvals.html'

    def get(self, request):

        if not request.user.is_superuser:

            return redirect('home')

        pending_turfs = Turf.objects.filter(
                                            is_approved=False,
                                            is_denied=False
                                            )


        approved_turfs = Turf.objects.filter(is_approved=True)

        return render(request, self.template_name, {

                                                    'pending_turfs': pending_turfs,
                                                    
                                                    'approved_turfs': approved_turfs
                                                    
                                                    })




class ApproveTurfView(LoginRequiredMixin, View):

    def get(self, request, uuid):

        if not request.user.is_superuser:

            return redirect('home')

        turf = get_object_or_404(Turf, uuid=uuid)

        turf.is_approved = True

        turf.save()

        messages.success(request, 'Turf approved successfully')

        return redirect('turf-approvals')




class DenyTurfView(LoginRequiredMixin, View):

    def post(self, request, uuid):
        if not request.user.is_superuser:
            return redirect('home')

        turf = get_object_or_404(Turf, uuid=uuid)

        turf.is_denied = True
        turf.is_approved = False
        turf.admin_delete_reason = request.POST.get('reason')
        turf.save()

        messages.error(request, 'Turf request denied')

        return redirect('turf-approvals')







class DeleteTurfView(LoginRequiredMixin, View):

    def post(self, request, uuid):
        if not request.user.is_superuser:
            return redirect('home')

        turf = get_object_or_404(Turf, uuid=uuid)

        reason = request.POST.get('reason')
        turf.admin_delete_reason = reason
        turf.save()

        turf.delete()

        messages.error(request, 'Approved turf deleted')

        return redirect('turf-approvals')









