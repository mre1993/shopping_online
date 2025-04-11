from .cart import Cart
from shop.models import Category

def cart(request):
    return {
        'cart': Cart(request),
        'categories': Category.objects.filter(is_sub=False), 
    }
