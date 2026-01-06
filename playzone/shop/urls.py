from django.urls import path

from . import views


urlpatterns = [

    path('product-list/',views.ProductListView.as_view(),name='product-list'),

    path('product-create/',views.ProductCreateView.as_view(),name='product-create'),

    path('product-detail/<str:uuid>/',views.ProductDetailView.as_view(),name='product-detail'),

    path('product-edit/<str:uuid>/',views.ProductEditView.as_view(),name='product-edit'),

    path('product-delete/<str:uuid>/',views.ProductDeleteView.as_view(),name='product-delete'),

    path('cart/', views.CartView.as_view(), name='cart'),

    path('add-to-cart/<str:uuid>/', views.AddToCartView.as_view(), name='add-to-cart'),

    path('update-cart/<str:uuid>/<str:action>/', views.UpdateCartView.as_view(), name='update-cart'),

    path('remove-cart/<str:uuid>/', views.RemoveFromCartView.as_view(), name='remove-cart'),



]
