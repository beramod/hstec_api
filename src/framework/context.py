from django.http import HttpResponse
from django.http import QueryDict
import time
import json


class Context():
    def __init__(self, request):
        self.startTime = time.time()
        self.request = {
            'body': request.body,
            'method': request.method,
            'path': request.path,
            'encoding': request.encoding or 'utf-8'
        }

        parameter = QueryDict('', mutable=True)
        parameter.update(request.GET.copy())

        if request.body:
            try:
                parsed = json.loads(request.body.decode(self.request.get('encoding')))
                parameter.update(parsed)
            except Exception as e:
                pass

        self.parameter = parameter

        self.header = {}
        self.data = {}
        self.code = 200
        self.message = 'success'
        self.content_type = 'application/json'
        self.encoding = 'utf-8'

    def render_to_response(self):
        response = HttpResponse()
        response.status_code = self.code

        content = {
            'response' : self.data,
            'code' : self.code,
            'responseTime' : time.time() - self.startTime,
            'message' : self.message
        }

        response.content = json.dumps(content).encode(self.encoding)
        response['Content-Type'] = '{}; charset={}'.format(self.content_type, self.encoding)

        for key in self.header.keys():
            value = self.header.get(key)
            response[key] = value

        return response