from django import forms

from django.contrib.auth.models import User

from .models import TurfOwner,Turf,TurfBooking



class TurfOwnerSignupForm(forms.Form):

    owner_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))

    phone = forms.CharField(max_length=15,widget=forms.TextInput(attrs={'class': 'form-control'}))

    username = forms.CharField(max_length=50,help_text='Use TURF NAME in CAPITAL letters without spaces',widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    account_holder_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    account_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    ifsc_code = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    
    pan_number = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


    def clean_username(self):

        username = self.cleaned_data.get('username').upper().replace(' ', '')

        if User.objects.filter(username=username).exists():

            raise forms.ValidationError('This turf username already exists')

        return username

    def clean(self):

        cleaned_data = super().clean()

        password = cleaned_data.get('password')

        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:

            raise forms.ValidationError('Passwords do not match')

        return cleaned_data



class TurfOwnerLoginForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))



class TurfRegisterForm(forms.ModelForm):

    class Meta:

        model = Turf

        fields = [

            'turf_name',

            'turf_image',

            'city',

            'address',

            'landmark',

            'google_map_link',

            'games',

            'ground_type',

            'price_per_hour'

        ]

        widgets = {

            'turf_name': forms.TextInput(attrs={'class': 'form-control'}),

            'city': forms.TextInput(attrs={'class': 'form-control'}),

            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

            'landmark': forms.TextInput(attrs={'class': 'form-control'}),

            'google_map_link': forms.URLInput(attrs={'class': 'form-control'}),

            'games': forms.TextInput(attrs={

                                            'class': 'form-control',

                                            'placeholder': 'Football, Cricket, Badminton'

                                        }

            ),

            'ground_type': forms.Select(attrs={'class': 'form-control'}),

            'price_per_hour': forms.NumberInput(attrs={'class': 'form-control'}),

        }



class TurfBookingForm(forms.ModelForm):

    class Meta:

        model = TurfBooking

        fields = [

            'customer_name',

            'customer_phone',

            'booking_date',

            'start_time',

            'end_time'
        ]

        widgets = {

            'customer_name': forms.TextInput(attrs={'class': 'form-control'}),

            'customer_phone': forms.TextInput(attrs={'class': 'form-control'}),

            'booking_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),

            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),

        }
