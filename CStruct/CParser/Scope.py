class Scope:

    def __init__(self, kind=''):

        self.kind = kind
        self.contents = []

    def __str__(self):
        return ' '.join(self.combineContents())

    def combineContents(self):

        contents = []

        if len(self.kind)==2:
            contents.append(self.kind[0])

        for token in self.contents:

            if isinstance(token, str):
                contents.append(token)
            else:
                contents.extend(token.combineContents())

        if len(self.kind)==2:
            contents.append(self.kind[1])

        return contents
