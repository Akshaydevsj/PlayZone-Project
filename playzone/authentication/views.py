from django.shortcuts import render, redirect

from django.views import View

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from django.core.mail import send_mail

from .models import Profile, Address

import random

from django.shortcuts import get_object_or_404

import time



class SignupView(View):

    template = 'authentication/signup.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        first_name = request.POST.get('first_name', '').strip()

        last_name  = request.POST.get('last_name', '').strip()

        email      = request.POST.get('email', '').strip().lower()

        phone      = request.POST.get('phone', '').strip()

        password   = request.POST.get('password')

        confirm    = request.POST.get('confirm_password')

        if not password or not confirm:

            messages.error(request, 'Password fields are required')

            return redirect('signup')

        if password != confirm:

            messages.error(request, 'Passwords do not match')

            return redirect('signup')

        if User.objects.filter(username=email).exists():

            messages.error(request, 'Email already registered')

            return redirect('signup')

        user = User.objects.create_user(

                                        username=email,

                                        email=email,

                                        password=password

                                    )

        user.first_name = first_name

        user.last_name  = last_name

        user.save()

        Profile.objects.create(

                                user=user,

                                phone=phone

                            )

        messages.success(request, 'Account created successfully')

        return redirect('login')
    



class LoginView(View):

    template = 'authentication/login.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        email    = request.POST.get('email', '').strip().lower()

        password = request.POST.get('password')

        user = authenticate(

                            request,

                            username=email,

                            password=password

                        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(request, 'Invalid email or password')

        return redirect('login')




class LogoutView(View):

    def get(self, request):

        logout(request)

        return redirect('home')




class ForgotPasswordView(View):

    template = 'authentication/forgot-password.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        email = request.POST.get('email', '').strip().lower()

        try:

            User.objects.get(username=email)

        except User.DoesNotExist:

            messages.error(request, 'Email not registered')

            return redirect('forgot-password')

        self.send_otp(request, email)

        messages.success(request, 'OTP has been sent to your email')

        return redirect('reset-password')

    def send_otp(self, request, email):

        otp = random.randint(100000, 999999)

        request.session['reset_email'] = email

        request.session['reset_otp'] = otp

        request.session['otp_time'] = time.time()  

        send_mail(

                    subject='PlayZone – Password Reset Verification Code',

                    message=f"""

                    Hello,

                    We received a request to reset your PlayZone account password.

                    Your One-Time Password (OTP) is:

                    {otp}

                    This OTP is valid for **2 minutes only**.

                    If you did not request this, please ignore this email.

                    —
                    Team PlayZone
                    Play Strong. Live Active.
                    """,
                                from_email='PlayZone Support <noreply@playzone.com>',

                                recipient_list=[email],

                                fail_silently=False,

                            )




class ResetPasswordView(View):

    template = 'authentication/reset-password.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        otp_input = request.POST.get('otp')

        password  = request.POST.get('password')

        confirm   = request.POST.get('confirm_password')

        if password != confirm:

            messages.error(request, 'Passwords do not match')

            return redirect('reset-password')

        saved_otp  = request.session.get('reset_otp')

        otp_time   = request.session.get('otp_time')

        email      = request.session.get('reset_email')

        if not otp_time or (time.time() - otp_time) > 120:

            messages.error(request, 'OTP expired. Please resend OTP.')

            return redirect('reset-password')

        if int(otp_input) != saved_otp:

            messages.error(request, 'Invalid OTP')

            return redirect('reset-password')
        
        user = User.objects.get(username=email)

        user.set_password(password)

        user.save()

        request.session.flush()

        messages.success(request, 'Password reset successful')

        return redirect('login')




class ResendOTPView(View):

    def get(self, request):

        email = request.session.get('reset_email')

        if not email:

            messages.error(request, 'Session expired. Try again.')

            return redirect('forgot-password')

        otp = random.randint(100000, 999999)

        request.session['reset_otp'] = otp

        request.session['otp_time'] = time.time()

        send_mail(

                    subject='PlayZone – New OTP',

                    message=f"""
                                
                    Hello,

                    We received a resend OTP request to reset your PlayZone account password.

                    Your One-Time Password (OTP) is:

                    {otp}

                    This OTP is valid for **2 minutes only**.

                    If you did not request this, please ignore this email.

                    —
                    Team PlayZone
                    Play Strong. Live Active.
                    """,

                    from_email='PlayZone Support <noreply@playzone.com>',
                                
                    recipient_list=[email],
                                
                    )

        messages.success(request, 'New OTP sent')

        return redirect('reset-password')




class ChangePasswordView(LoginRequiredMixin, View):

    template = 'authentication/change-password.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        old = request.POST.get('old_password')

        new = request.POST.get('new_password')

        if not request.user.check_password(old):

            messages.error(request, 'Current password is incorrect')

            return redirect('change-password')

        request.user.set_password(new)

        request.user.save()

        login(request, request.user)

        messages.success(request, 'Password updated')

        return redirect('account')




class AccountView(LoginRequiredMixin, View):

    template = 'authentication/account.html'

    def get(self, request):

        profile = request.user.profile

        addresses = request.user.addresses.all()

        return render(

                        request,

                        self.template,

                        {

                            'profile': profile,

                            'addresses': addresses

                        }

        )





class EditProfileView(LoginRequiredMixin, View):

    template = 'authentication/edit-profile.html'

    def get(self, request):

        profile = request.user.profile

        return render(

                        request,

                        self.template,

                        {'profile': profile}
                    )

    def post(self, request):

        user = request.user

        profile = user.profile

        user.first_name = request.POST.get('first_name')

        user.last_name  = request.POST.get('last_name')

        user.email      = request.POST.get('email')

        profile.phone   = request.POST.get('phone')

        user.save()

        profile.save()

        messages.success(request, 'Profile updated successfully')

        return redirect('account')
    



class AddAddressView(LoginRequiredMixin, View):

    template = 'authentication/add-address.html'

    def get(self, request):

        return render(request, self.template)

    def post(self, request):

        Address.objects.create(

                                user      = request.user,

                                full_name = request.POST.get('full_name'),

                                phone     = request.POST.get('phone'),

                                house     = request.POST.get('house'),

                                street    = request.POST.get('street'),

                                city      = request.POST.get('city'),

                                state     = request.POST.get('state'),

                                pincode   = request.POST.get('pincode'),


                            )

        messages.success(request, 'Address added successfully')

        return redirect('account')




class EditAddressView(LoginRequiredMixin, View):

    template = 'authentication/edit-address.html'


    def get(self, request, id):

        address = get_object_or_404(

                                        Address,

                                        id=id,

                                        user=request.user

                                    )

        return render(

                        request,

                        self.template,

                        {'address': address}


                    )

    def post(self, request, id):

        address = get_object_or_404(

                                        Address,

                                        id=id,

                                        user=request.user

                                    )

        address.full_name = request.POST.get('full_name')

        address.phone     = request.POST.get('phone')

        address.house     = request.POST.get('house')

        address.street    = request.POST.get('street')

        address.city      = request.POST.get('city')

        address.state     = request.POST.get('state')

        address.pincode   = request.POST.get('pincode')

        address.save()

        messages.success(request, 'Address updated successfully')

        return redirect('account')
