from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

# Create your views here.
from .models import Item, Order


def index(request):

    return render(request, 'shoppingmall/index.html')


def iteminfo(request):

    if 'searchWord' in request.GET:

        search_word = request.GET['searchWord']

        result = Item.objects.filter(
            id__contains=search_word).order_by('-id')

    else:

        result = Item.objects.all().order_by('-id')

    context = {
        'item': result
    }

    return render(request, 'shoppingmall/iteminfo.html', context)


def itemadd(request):

    if request.method == 'GET':

        return render(request, 'shoppingmall/itemadd.html')

    else:

        item_name = request.POST['item_name']

        item_count = request.POST['item_count']

        Item.objects.create(
            item_name=item_name,
            item_count=item_count
        )

        return HttpResponseRedirect('/iteminfo/')


def itemupdate(request, id):

    item = Item.objects.get(id=id)

    if request.method == 'GET':

        context = {'item': item}

        return render(request, 'shoppingmall/itemupdate.html', context)

    else:

        item.item_count = request.POST['item_count']

        item.save()

        return HttpResponseRedirect('/iteminfo/')


def itemdelete(request, id):
    Item.objects.get(id=id).delete()

    return HttpResponseRedirect('/iteminfo/')


def orderinfo(request):

    if 'searchWord' in request.GET:

        search_word = request.GET['searchWord']

        # order = Order.objects.filter(item_code__contains=search_word)
        # order = Order.objects.all().order_by('-id')
        order = Order.objects.filter(
            item_code__item_name__contains=search_word).order_by('-id')

    else:
        order = Order.objects.all().order_by('-id')

    context = {'order': order}

    return render(request, 'shoppingmall/orderinfo.html', context)


def orderadd(request):

    if request.method == 'GET':

        return render(request, 'shoppingmall/orderadd.html')

    else:

        item_id = request.POST['item_id']

        quantity = request.POST['quantity']

        Order.objects.create(
            item_code_id=item_id,
            quantity=quantity
        )

        return HttpResponseRedirect('/orderinfo/')


def orderupdate(request, id):

    order = Order.objects.get(id=id)

    if request.method == 'GET':

        context = {'order': order}

        return render(request, 'shoppingmall/orderupdate.html', context)

    else:

        order.quantity = request.POST['quantity']

        order.save()

        return HttpResponseRedirect('/orderinfo/')


def orderdelete(request, id):

    order = Order.objects.get(id=id).delete()

    return HttpResponseRedirect('/orderinfo/')
