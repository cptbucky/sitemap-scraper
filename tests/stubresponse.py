class StubResponse:
    def __init__(self, content):
        self.content = content

    def read(self):
        return self.content
