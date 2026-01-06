from django.urls import path

from . import views

from django.contrib.auth.views import PasswordChangeView


urlpatterns = [

    
    
    path('owner/signup/',views.TurfOwnerSignupView.as_view(),name='owner-signup'),

    path('owner/login/',views.TurfOwnerLoginView.as_view(),name='owner-login'),

    path('owner/logout/',views.TurfOwnerLogoutView.as_view(),name='owner-logout'),

    path('owner/dashboard/',views.TurfOwnerDashboardView.as_view(), name='owner-dashboard'),

    path('owner/turf/register/',views.TurfRegisterView.as_view(), name='turf-register'),

    path('owner/turf/toggle-booking/',views.ToggleBookingStatusView.as_view(), name='toggle-booking'),

    path('owner/change-password/',PasswordChangeView.as_view(template_name='turf/change-password.html',success_url='/owner/dashboard/'),name='owner-change-password'),

    path('owner/profile/edit/',views.OwnerProfileEditView.as_view(), name='owner-profile-edit'),

    path('owner/turf/edit/<uuid:uuid>/',views.OwnerEditTurfView.as_view(), name='owner-edit-turf'),

    path('owner/turf/delete/<uuid:uuid>/',views.OwnerDeleteTurfView.as_view(), name='owner-delete-turf'),

    path('turf-approvals/',views.TurfApprovalDashboardView.as_view(),name='turf-approvals'),

    path('turf-approvals/approve/<uuid:uuid>/',views.ApproveTurfView.as_view(),name='approve-turf'),

    path('turf-approvals/deny/<uuid:uuid>/',views.DenyTurfView.as_view(),name='deny-turf'),

    path('turf-approvals/delete/<uuid:uuid>/',views.DeleteTurfView.as_view(),name='delete-turf'),

]
