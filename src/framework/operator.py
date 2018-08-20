from django.views.generic import View
from src.framework.context import Context
from src.framework.interpreter import Interpreter
from src.framework.handler import Handler
from src.framework.router import urls


class Operator(View):
    def get(self, request, *args, **kwargs):
        context = Context(request)

        interpreter = Interpreter()

        interpreter.PreProcess(context, *args, **kwargs)
        interpreter.Process(context, *args, **kwargs)
        interpreter.PostProcess(context, *args, **kwargs)

        path = request.path

        if path.endswith('/'):
            path = path[:-1]

        method = request.method

        for url in urls:
            targetPath = url[0]
            targetMethod = url[1]
            targetHandlerClass = url[2]

            if path != targetPath or method != targetMethod:
                continue

            if issubclass(targetHandlerClass, Handler):
                handlerInstance = targetHandlerClass()

                try:
                    handlerInstance.handle(context, *args, **kwargs)
                except Exception as e:
                    context.data = {
                        'message': str(e),
                        'code': 400
                    }

        return context.render_to_response()

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)