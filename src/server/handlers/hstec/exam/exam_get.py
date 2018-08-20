from src.framework.handler import Handler


class ExamGetHandler(Handler):
    def handle(self, context, *args, **kwargs):
        context.data = {
            'res' : 'TEST!'
        }