from django.shortcuts import render
import json
from curr_conv.cel import get_api_data
from django.http import JsonResponse
from conv.forms import AddAuthor
from conv.models import Author


def main_page(request):
    form = request.GET
    data = get_api_data(request)

    dic = {'data': data, 'form': form}
    return render(request, 'curr_conv/index.html', dic)


def return_json(request):
    response_data = {}
    form = request.GET
    data = get_api_data(request)
    if request.method == 'GET':
        response_data["from"] = form.get('form-from')
        response_data["to"] = form.get('form-to')
        response_data["price"] = data['ticker']['price']
        response_data["count"] = form.get('form-count')
        if form.get('form-count'):
            response_data["result"] = float(form.get('form-count')) * float(data['ticker']['price'])

    return JsonResponse(response_data)


def db_page(request):
    r = request.POST
    print(r)
    res, mess = {}, {}
    if request.method == 'POST':
        form = AddAuthor(r)
        if form.is_valid():
            if r.get('doing') == 'Add':
                if not (Author.objects.filter(first_name=r.get('first_name')) or Author.objects.filter(
                        last_name=r.get('last_name'))):
                    q = Author(first_name=r.get('first_name'),
                               last_name=r.get('last_name'),
                               email=r.get('email'))
                    q.save()
                    mess = {'good': "Data add successful!"}
                else:
                    mess = {'warning': "Data warning!"}
            elif r.get('doing') == 'Del':
                try:
                    q = Author.objects.get(first_name=r.get('first_name'),
                               last_name=r.get('last_name'),
                               email=r.get('email'))
                    q.delete()
                    mess = {'good': "Data delete successful!"}
                except Author.DoesNotExist as e:
                    print(e)
                    mess = {'warning': "Data not exists or something goes wrong!"}
            res['mess'] = mess


    else:
        form = AddAuthor()

    us = tuple(Author.objects.values('id'))
    us_i = ()
    for i in us:
        us_i += ((i['id'], i['id']),)
    print(us_i)

    res['AddAuthor'] = form
    res['DB'] = Author.objects.all()
    return render(request, 'curr_conv/db_model.html', res)
