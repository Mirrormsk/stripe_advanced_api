from django.urls import path
from payments import views
from payments.apps import PaymentsConfig

app_name = PaymentsConfig.name


urlpatterns = [
    path('', views.OrderListAPIView.as_view(), name='order_list'),
    path('create/', views.OrderCreateAPIView.as_view(), name='order_create'),
    path('<int:pk>/pay/', views.OrderPaymentAPIView.as_view(), name='order_pay'),
]