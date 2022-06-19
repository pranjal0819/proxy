import json

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def index(request):
    print('Welcome!!!')

    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url')
        headers = data.get('headers')
        method = data.get('method')
        timeout = int(data.get('timeout', 10))
        data = data.get('data')

        try:
            if method == 'GET':
                res = requests.get(url=url, headers=headers, timeout=timeout)
                return HttpResponse(res.content, status=res.status_code)
            elif method == 'POST':
                res = requests.post(url=url, headers=headers, timeout=timeout, data=data)
                return HttpResponse(res.content, status=res.status_code)

        except Exception as e:
            return HttpResponse(e, status=500)

    return HttpResponse("OK", status=200)
