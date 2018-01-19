# from django.shortcuts import render

# Create your views here.

from django.shortcuts import render_to_response

from django.utils.translation import gettext_lazy as _

from .models import Product, ProductLoc, Offer


def products(request):
    products = Product.objects.all()
    offers = Offer.objects.all()
    return render_to_response('products.html', {'products': products, 'offers': offers})


def product(request, product_id):
    import django
    # product = Product.objects.get(pk=int(product_id))
    product = ProductLoc.objects.filter(product=int(product_id)).filter(lang__startswith='cs_CZ')[0]
    return render_to_response('product.html', {'product': product, 'ver': django.__version__})
