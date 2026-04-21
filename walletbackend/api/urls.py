from django.urls import path, include

urlpatterns = [
    path('users/', include('users.urls'))
    # path('wallet/', include('wallet.urls')),
    # path('orders/', include('orders.urls')),
    # path('payment/', include('payment.urls')),
]