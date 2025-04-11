from cart.cart import Cart
from .forms import ShippingForm
from .models import ShippingAddress, Order, OrderItem
from django.contrib import messages
import requests
import json
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
import requests
import json
from .models import Order
from django.contrib import messages
from shop.models import Product, Profile
from django.contrib.auth.models import User


def payment_success(request):
    return render(request, 'payment/payment_success.html', {})

def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    total = cart.get_total()
    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'total':total, 'shipping_form':shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {'cart_products':cart_products, 'quantities':quantities, 'total':total, 'shipping_form':shipping_form})


def confirm_order(request):
    if request.method == "POST":
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()

    
        user_shipping = {
            'shipping_fullname': request.POST.get('shipping_fullname', ''),
            'shipping_email': request.POST.get('shipping_email', ''),
            'shipping_address1': request.POST.get('shipping_address1', ''),
            'shipping_address2': request.POST.get('shipping_address2', ''),
            'shipping_city': request.POST.get('shipping_city', ''),
            'shipping_state': request.POST.get('shipping_state', ''),
            'shipping_zipcode': request.POST.get('shipping_zipcode', ''),
            'shipping_country': request.POST.get('shipping_country', ''),
        }

        if not user_shipping['shipping_fullname'] or not user_shipping['shipping_email']:
            messages.error(request, 'نام و ایمیل الزامی است.')
            return redirect('checkout')

        request.session['user_shipping'] = user_shipping

        if request.user.is_authenticated:
            user = request.user
            order, created = Order.objects.get_or_create(
                user=user,
                defaults={
                    "full_name": user_shipping['shipping_fullname'],
                    "email": user_shipping['shipping_email'],
                    "shipping_address": f"{user_shipping['shipping_address1']}\n"
                                        f"{user_shipping['shipping_address2']}\n"
                                        f"{user_shipping['shipping_city']}\n"
                                        f"{user_shipping['shipping_state']}\n"
                                        f"{user_shipping['shipping_zipcode']}\n"
                                        f"{user_shipping['shipping_country']}",
                    "amount_paid": total,
                }
            )
        else:
            order = Order(
                full_name=user_shipping['shipping_fullname'],
                email=user_shipping['shipping_email'],
                shipping_address=f"{user_shipping['shipping_address1']}\n"
                                 f"{user_shipping['shipping_address2']}\n"
                                 f"{user_shipping['shipping_city']}\n"
                                 f"{user_shipping['shipping_state']}\n"
                                 f"{user_shipping['shipping_zipcode']}\n"
                                 f"{user_shipping['shipping_country']}",
                amount_paid=total
            )
            order.save()

        return render(request, 'payment/confirm_order.html', {
            'cart_products': cart_products,
            'quantities': quantities,
            'total': total,
            'shipping_info': user_shipping,
            'order': order, 
        })
    else:
        messages.error(request, 'دسترسی به این صفحه امکان‌پذیر نمی‌باشد')
        return redirect('home')


def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods()
        quantities = cart.get_quants()
        total = cart.get_total()
        user_shipping = request.session.get('user_shipping')
        full_name = user_shipping['shipping_fullname']
        email = user_shipping['shipping_email']
        full_address = f"{user_shipping['shipping_address1']}\n{user_shipping['shipping_address2']}\n{user_shipping['shipping_city']}\n{user_shipping['shipping_state']}\n{user_shipping['shipping_zipcode']}\n{user_shipping['shipping_country']}"
        if request.user.is_authenticated:
            user = request.user
            new_order = Order(
                user = user,
                full_name = full_name,
                email=email,
                shipping_address = full_address,
                amount_paid = total
            )
            new_order.save()
            odr = get_object_or_404(Order, id=new_order.pk)
            for product in cart_products:
                prod = get_object_or_404(Product, id=product.id)
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for k, v in quantities.items():
                    if int(k) == product.id:
                        new_item = OrderItem(
                            order = odr,
                            product = prod,
                            price = price,
                            quantity = v,
                            user = user
                        )
                        new_item.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]


            messages.success(request,'سفارش ثبت شد')
            return redirect('home')
        else:
            new_order = Order(
                full_name = full_name,
                email=email,
                shipping_address = full_address,
                amount_paid = total
            )
            new_order.save()
            odr = get_object_or_404(Order, id=new_order.pk)
            for product in cart_products:
                prod = get_object_or_404(Product, id=product.id)
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price
                for k, v in quantities.items():
                    if int(k) == product.id:
                        new_item = OrderItem(
                            order = odr,
                            product = prod,
                            price = price,
                            quantity = v,
                        )
                        new_item.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]
            cu = Profile.objects.filter(user__id = request.user.id)
            cu.update(old_cart="")        

            messages.success(request,'سفارش ثبت شد')
            return redirect('home')
    else:
        messages.success(request,'دسترسی به این صفحه امکان  پذیز نمیباشد')
        return redirect('home')




MERCHANT = os.getenv('ZARINPAL_MERCHANT_ID', 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX')
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"
CallbackURL = 'http://127.0.0.1:8000/orders/verify/'


class OrderPayView(LoginRequiredMixin, View):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id, user=request.user)
        request.session['order_pay'] = {'order_id': order.id}

        req_data = {
            "merchant_id": MERCHANT,
            "amount": order.get_total_price(),
            "callback_url": CallbackURL,
            "description": description,
            "metadata": {"mobile": request.user.profile.phone_number, "email": request.user.email}
        }
        req_header = {"accept": "application/json", "content-type": "application/json"}
        response = requests.post(ZP_API_REQUEST, data=json.dumps(req_data), headers=req_header)
        result = response.json()

        if result.get('data') and not result['errors']:
            authority = result['data']['authority']
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            error = result['errors']
            return HttpResponse(f"Error code: {error['code']}, Message: {error['message']}")


class OrderVerifyView(LoginRequiredMixin, View):
    def get(self, request):
        order_id = request.session.get('order_pay', {}).get('order_id')
        if not order_id:
            messages.error(request, "No order found in session.")
            return redirect('home')

        order = get_object_or_404(Order, id=order_id, user=request.user)
        t_status = request.GET.get('Status')
        t_authority = request.GET.get('Authority')

        if t_status == 'OK':
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority
            }
            req_header = {"accept": "application/json", "content-type": "application/json"}
            response = requests.post(ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            result = response.json()

            if result.get('data') and not result['errors']:
                t_status = result['data']['code']
                if t_status == 100:
                    order.paid = True
                    order.save()
                    return HttpResponse('Transaction success. RefID: ' + str(result['data']['ref_id']))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted: ' + str(result['data']['message']))
                else:
                    return HttpResponse('Transaction failed. Status: ' + str(result['data']['message']))
            else:
                error = result['errors']
                return HttpResponse(f"Error code: {error['code']}, Message: {error['message']}")
        else:
            return HttpResponse('Transaction failed or canceled by user.')
