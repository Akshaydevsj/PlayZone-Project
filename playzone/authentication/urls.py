from django.urls import path

from . import views

urlpatterns = [

    path('signup/',views.SignupView.as_view(),name='signup'),

    path('login/',views.LoginView.as_view(),name='login'),

    path('logout/',views.LogoutView.as_view(),name='logout'),

    path('account/',views.AccountView.as_view(),name='account'),

    path('forgot-password/',views.ForgotPasswordView.as_view(),name='forgot-password'),

    path('reset-password/',views.ResetPasswordView.as_view(), name='reset-password'),

    path('resend-otp/',views.ResendOTPView.as_view(), name='resend-otp'),

    path('change-password/',views.ChangePasswordView.as_view(),name='change-password'),

    path('edit-profile/',views.EditProfileView.as_view(), name='edit-profile'),

    path('add-address/',views.AddAddressView.as_view(), name='add-address'),

    path('edit-address/<int:id>/',views.EditAddressView.as_view(), name='edit-address'),

]
