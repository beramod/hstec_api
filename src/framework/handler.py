
class Handler():
    parameters = []

    def SetParameters(self):
        pass

    def MakeParameter(self, parameter, required):
        return {
            'parameter' : parameter,
            'required' : required
        }

    def ValidParameters(self, context):
        self.SetParameters()

        for param in self.parameters:
            if param.get('required'):
                if not context.parameter.get(param.get('parameter')):
                    return False

        return True

    def handle(self, context, *args, **kwargs):
        pass