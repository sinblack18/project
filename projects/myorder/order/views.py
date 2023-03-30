from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .models import Order


# Create your views here.


def index(request):

    return render(request, 'order/index.html')


def order_from(request):

    if request.method == 'GET':
        return render(request, 'order/order_from.html')
    else:
        order_text = request.POST['order_text']
        price = request.POST['price']
        address = request.POST['address']

        Order.objects.create(
            order_text=order_text,
            price=price,
            address=address
        )
        return HttpResponseRedirect('/order/')


def search_all(request):

    order_list = Order.objects.all().order_by('-id')

    context = {
        'order_list': order_list
    }

    return render(request, 'order/search.html', context)


def update(request, id):

    print(id)

    order = Order.objects.get(id=id)

    if request.method == "GET":

        context = {'order': order}

        return render(request, 'order/order_update.html', context)

    else:
        order.order_text = request.POST['order_text']
        order.price = request.POST['price']
        order.address = request.POST['address']

        # 객체 안에 저장하기
        order.save()

        return HttpResponseRedirect('/order/')


def delete(request, id):

    print(id)
    # 해당 객체를 가져와서(get 가져올꺼니깐) 삭제
    Order.objects.get(id=id).delete()

    return HttpResponseRedirect('/order/')


def order_show(request, id):

    print(id)

    order = Order.objects.get(id=id)

    context = {
        'ordertext': order.order_text,
        'orderdate': order.order_date,
        'orderaddress': order.address,
        'orderprice': order.price,
        'orderid': id,
        'orderts': order.order_text.split(',')
    }

    return render(request, 'order/order_show.html', context)


def search_address(request):

    order_address = request.POST['search_address']
    condition = request.POST['condition']

    if condition == 'all':

        olist = Order.objects.filter(address__contains=order_address)
        context = {
            'order_list': olist
        }

        return render(request, 'order/search.html', context)

    else:
        olist = Order.objects.filter(address__startswith=order_address)
        context = {
            'order_list': olist
        }

        return render(request, 'order/search.html', context)
