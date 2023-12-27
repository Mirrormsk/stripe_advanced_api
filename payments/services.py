import collections

import environ
import stripe
from stripe.checkout import Session

from items.models import Item
from payments.models import Order, Discount, Tax
from django.conf import settings

env = environ.Env(DEBUG=(bool, False))

stripe.api_key = settings.STRIPE_DEFAULT_SECRET_KEY
SUCCESS_URL = env("PAYMENT_SUCCESS_URL")


class StripeApiClient:
    """Stripe API Client class"""

    @staticmethod
    def get_stripe_api_key(currency):
        if currency == "USD":
            return settings.STRIPE_SECRET_KEY_USD
        elif currency == "EUR":
            return settings.STRIPE_SECRET_KEY_EUR
        else:
            return settings.STRIPE_DEFAULT_SECRET_KEY

    @staticmethod
    def get_stripe_public_key(currency):
        if currency == "USD":
            return settings.STRIPE_PUBLIC_KEY_USD
        elif currency == "EUR":
            return settings.STRIPE_PUBLIC_KEY_EUR
        else:
            return settings.STRIPE_DEFAULT_PUBLIC_KEY

    @classmethod
    def create_product(cls, item: Item) -> stripe.Product:
        product = stripe.Product.create(name=item.name, description=item.description)
        return product

    @classmethod
    def create_price(cls, item: Item) -> stripe.Price:
        product = cls.create_product(item)

        price = stripe.Price.create(
            unit_amount_decimal=str(item.price * 100),
            currency=item.currency,
            product=product.id,
        )
        return price

    @staticmethod
    def create_coupon(discount: Discount) -> stripe.Coupon:
        """Creates a Stripe coupon"""
        coupon = stripe.Coupon.create(
            amount_off=discount.amount_off if discount.amount_off else None,
            currency=discount.currency if discount.currency else None,
            percent_off=discount.percent_off if discount.percent_off else None,
        )
        return coupon

    @staticmethod
    def create_tax_rate(tax: Tax):
        """Creates a Stripe Tax object"""
        stripe_tax = stripe.TaxRate.create(
            display_name=tax.display_name,
            description=tax.description if tax.description else None,
            percentage=tax.percentage,
            inclusive=tax.inclusive,
            country=tax.country,
        )
        return stripe_tax

    @classmethod
    def get_line_items_from_order(cls, order: Order):
        tax_rates = [cls.create_tax_rate(tax).id for tax in order.tax_rates.all()]
        line_items = [
            {"price": cls.create_price(item).id, "quantity": 1, "tax_rates": tax_rates}
            for item in order.items.all()
        ]
        return line_items

    @classmethod
    def create_session(cls, order: Order) -> Session:
        """Creates a Stripe Session Object.
        Uses different api keys for EUR and USD currencies
        """
        currency = order.items.first().currency
        stripe.api_key = cls.get_stripe_api_key(currency)

        line_items = cls.get_line_items_from_order(order)
        coupons = [cls.create_coupon(discount).id for discount in order.discounts.all()]

        session = stripe.checkout.Session.create(
            line_items=line_items,
            mode="payment",
            success_url=SUCCESS_URL,
            discounts=[{"coupon": coupon} for coupon in coupons],
        )

        return session

    @classmethod
    def execute_payment(cls, payment_object: Order | Item) -> Session:

        if isinstance(payment_object, Item):
            order = Order.objects.create()
            order.items.add(payment_object)
            order.save()
            payment_object = order

        elif not isinstance(payment_object, Order):
            raise TypeError("Only Order and Item objects are supported")

        session = cls.create_session(payment_object)

        return session

    @staticmethod
    def retrieve_session(session_id: str) -> Session:
        session = stripe.checkout.Session.retrieve(session_id)
        return session

    # @staticmethod
    # def create_payment_intent(order: Order):
    #     intent = stripe.PaymentIntent.create(
    #         amount=int(order.total_price() * 100),  # сумма в центах
    #         currency='usd',
    #         description=f'Оплата заказа #{order.id}',
    #         payment_method=request.data.get('payment_method'),  # ID платежного метода, например, 'pm_card_visa'
    #         confirm=True,
    #         metadata={'order_id': order.id},
    #     )


class PaymentService:
    """Payment service"""

    def create_payment(self, order: Order) -> dict:
        ...
