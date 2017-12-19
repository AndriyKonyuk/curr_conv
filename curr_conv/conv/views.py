from django.shortcuts import render
from django.http import HttpResponse
import requests, json, time
from curr_conv.cel import get_api_data

def main_page(request):
    form = request.GET
    data = get_api_data(request)
    response_data = {}
    if request.method == 'GET':
        response_data['from'] = form.get('from')
        response_data['to'] = form.get('to')
        response_data['price'] = data['ticker']['price']

    resp = json.dumps(response_data)

    dic = {'data': data, 'form': form, 'resp':resp}
    return render(request, 'curr_conv/index.html', dic)

