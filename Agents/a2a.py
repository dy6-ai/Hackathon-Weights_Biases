class Agent:
    def __init__(self, name, tools):
        self.name = name
        self.tools = tools
        self.url = None

class Tool:
    def __init__(self, fn, description):
        self.fn = fn
        self.description = description 