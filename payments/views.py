from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from payments.models import Order
from payments.serializers import OrderSerializer
from payments.services import StripeApiClient


class OrderCreateAPIView(CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderPaymentView(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderPaymentAPIView(APIView):
    """View for payment using Stripe checkout session"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))
        session = StripeApiClient.execute_payment(order)
        return Response(
            {
                "order_id": order.id,
                "session_id": session.id,
                "checkout_url": session.url,
            },
            status=status.HTTP_200_OK,
        )


class OrderPaymentIntentAPIView(APIView):
    """View for payment using Stripe PaymentIntent"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))
        payment_intent = StripeApiClient.execute_payment_intent(order)
        return Response(
            {
                "order_id": order.id,
                "payment_intent": payment_intent.id,
                "client_secret": payment_intent.client_secret,
            },
            status=status.HTTP_200_OK,
        )