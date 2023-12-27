from django.conf import settings
from django.views.generic import DetailView
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response

from items.models import Item
from items.serializers import ItemSerializer
from payments.services import StripeApiClient


class ItemDetailView(DetailView):
    model = Item

    def get_context_data(self, **kwargs):
        item = self.get_object()
        context_data = super().get_context_data(**kwargs)
        context_data["STRIPE_PUBLIC_KEY"] = StripeApiClient.get_stripe_public_key(item.currency)
        return context_data


class ItemBuyView(RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def get(self, request, *args, **kwargs):
        item = self.get_object()
        session = StripeApiClient.execute_payment(item)
        return Response(
            {"item_id": item.id, "session_id": session.id}, status=status.HTTP_200_OK
        )
