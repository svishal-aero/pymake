class Scope:
    '''Stores contents within brackets, braces or parentheses'''

    def __init__(self, kind=''):
        self.kind     = kind    # Can take values of '', '()', '{}', '[]'
        self.contents = []      # Contains strings or child Scope objects

    def __str__(self):
        '''Returns a string representation of the contents (recursively)'''
        return ' '.join(self.combineContents())

    def combineContents(self):
        '''Creates a list of strings from the contents (recursively)'''
        combinedContents = []
        # Store the opening bracket
        if len(self.kind)==2: combinedContents.append(self.kind[0])
        for token in self.contents:
            # A token can be a string or another Scope object
            if isinstance(token, str): combinedContents.append(token)
            else: combinedContents.extend(token.combineContents())
        # Store the closing bracket
        if len(self.kind)==2: combinedContents.append(self.kind[1])
        return combinedContents
