from decimal import Decimal

from django.conf import settings

from main.models import Drug


class Cart(object):
    def __init__(self, request):
        """Initialization cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            """Saving empty cart in session"""
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def save(self):
        """Session is modified"""
        self.session.modified = True

    def add(self, drug, quantity=1, update_quantity=False):
        drug_id = str(drug.id)
        if drug_id not in self.cart:
            self.cart[drug_id] = {'quantity': 0, 'price': str(drug.price)}
        if update_quantity:
            self.cart[drug_id]['quantity'] = quantity
        else:
            self.cart[drug_id]['quantity'] += quantity
        self.save()

    def remove(self, drug):
        drug_id = str(drug.id)
        if drug_id in self.cart:
            del self.cart[drug_id]
            self.save()

    def __iter__(self):
        """Iterate products in cart"""
        drug_ids = self.cart.keys()
        drugs = Drug.objects.filter(id__in=drug_ids)

        cart = self.cart.copy()
        for drug in drugs:
            cart[str(drug.id)]['drug'] = drug
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def total_items(self):
        """Returns sum of items in cart"""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()



