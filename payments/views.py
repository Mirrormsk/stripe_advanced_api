from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
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


class OrderListAPIView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderPaymentAPIView(APIView):
    """View for payment using Stripe checkout session"""

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "order_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "session_id": openapi.Schema(type=openapi.TYPE_STRING),
                    "checkout_url": openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=["order_id", "payment_intent", "client_secret"],
            ),
            404: "Not Found",
        },
    )
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

    @swagger_auto_schema(
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "order_id": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "payment_intent_id": openapi.Schema(type=openapi.TYPE_STRING),
                    "client_secret": openapi.Schema(type=openapi.TYPE_STRING),
                },
                required=["order_id", "payment_intent", "client_secret"],
            ),
            404: "Not Found",
        },
    )
    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=kwargs.get("pk"))
        payment_intent = StripeApiClient.execute_payment_intent(order)
        return Response(
            {
                "order_id": order.id,
                "payment_intent_id": payment_intent.id,
                "client_secret": payment_intent.client_secret,
            },
            status=status.HTTP_200_OK,
        )
