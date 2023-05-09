import stripe
from django.conf import settings

from journey_hub.constants import CURRENCY_MAPPING

stripe.api_key = settings.STRIPE_API_KEY


class StripeClient:
    def __init__(self):
        self.success_url = 'http://localhost:8000/'
        self.fail_url = 'http://localhost:8000/'

    def create_session(self, price: str, currency: str, product_name: str, user_email: str):
        session = stripe.checkout.Session.create(
            success_url=self.success_url,
            cancel_url=self.fail_url,
            payment_method_types=['card'],
            mode='payment',
            line_items=[{
                'price_data': {
                    'currency': CURRENCY_MAPPING.get(currency),
                    'unit_amount': int(price * 100),
                    'product_data': {
                        'name': product_name,
                    },
                },
                'quantity': 1,
            }],
            customer_email=user_email,
        )
        return session.id, session.url
