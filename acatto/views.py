# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response

from django.utils.translation import gettext_lazy as _

from .models import Product, Offer


def products(request):
    products = Product.objects.all()
    offers = Offer.objects.all()
    return render_to_response('products.html', {'products': products, 'offers': offers})


def product(request, product_id):
    product = Product.objects.get(pk=int(product_id))
    return render_to_response('product.html', {'product': product})
