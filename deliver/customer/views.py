from typing import Any
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.core.mail import send_mail
from customer.models import *

class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/index.html')


class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'customer/about.html')


class Order(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(
        category__name__contains='Appetizer')
        entres = MenuItem.objects.filter(category__name__contains='Entre')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')

        # pass into context
        context = {
            'appetizers': appetizers,
            'entres': entres,
            'desserts': desserts,
            'drinks': drinks,
        }

        # render the template
        return render(request, 'customer/order.html', context)

    def post(self, request, *args, **kwargs):
        name=request.POSt.get('name')
        email=request.POSt.get('email')
        street=request.POSt.get('street')
        city=request.POSt.get('city')
        state=request.POSt.get('state')
        zip_code=request.POSt.get('zip_code')

        order_items = {
            'items': []
        }

        items = request.POST.getlist('items[]')

        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }

            order_items['items'].append(item_data)

            price = 0
            item_ids = []

        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])

        order = OrderModel.objects.create(
            price=price,
            name=name,
            email=email,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,

            )
        order.items.add(*item_ids)
        #afer everthing is done, send conformation email to the user
        body='''thank you for order! youy food being is made and will be deliverd soon
              Your total:{price}
              thank you agian for your order!'''
        
        send_mail(
            'Thank for Your Order!',
            body,
            'example@exaple.com',
            [email],
            fail_silently=False        
        )


        context = {
            'items': order_items['items'],
            'price': price
        }

        return render(request, 'customer/order_confirmation.html', context)
    