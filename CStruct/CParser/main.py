from .Scope import Scope

class CParser:

    def __init__(self, filename):
        self.__tempBuffer    = ''
        self.__prevChar      = ''
        self.__insideString  = False
        self.__insideEscape  = False
        self.__insideComment = None
        sectionList   = self.preprocess(filename)
        sectionList   = self.removeNewlines(sectionList)
        tokenList     = self.tokenize(sectionList)
        contents      = self.extractContents(tokenList)
        self.contents = self.addNewlines(contents)

    def addNewlines(self, contents):
        newContents = []
        lastScopeKind = ''
        for iToken in range(len(contents)):
            token = contents[iToken]
            newContents.append(token)
            if isinstance(token, Scope):
                token.contents = self.addNewlines(token.contents)
                if lastScopeKind=='()' and token.kind=='{}':
                    newContents.append('\n')
                lastScopeKind = token.kind
            else:
                lastScopeKind = ''
        return newContents

    def extractContents(self, tokenList):
        mainScope = Scope()
        scopeList = [mainScope]
        for token in tokenList:
            if token in '[{(':
                kind = ''
                if token in '[': kind = '[]'
                if token in '{': kind = '{}'
                if token in '(': kind = '()'
                newScope = Scope(kind=kind)
                scopeList[-1].contents.append(newScope)
                scopeList.append(newScope)
            elif token in ')}]':
                scopeList.pop()
            else:
                scopeList[-1].contents.append(token)
        return mainScope.contents
    
    def tokenize(self, sectionList):
        tokenList = []
        for section in sectionList:
            tempList = []
            if section[0]!='"':
                for c in '[]{}();,+-*/\n':
                    section = section.replace(c, ' '+c+' ')
                section = section.replace('\t', ' ')
                tempList = section.split(' ')
                while '' in tempList:
                    tempList.remove('')
            else:
                tempList.append(section)
            tokenList.extend(tempList)
        return tokenList

    def removeNewlines(self, sectionList): 
        newSectionList = []
        previousNewline = True
        insideMacro = False
        for section in sectionList:
            if section[0]=='"':
                newSection = section
            else:
                newSection = ''
                for char in section:
                    newSection += char
                    if char=='#' and previousNewline:
                        insideMacro = True
                    if char=='\n':
                        previousNewline = True
                        if insideMacro: insideMacro=False
                        else: newSection = newSection[:-1]
                    if char not in ' \t' and previousNewline:
                        previousNewline = False
            if len(newSection)>0: newSectionList.append(newSection)
        return newSectionList

    def preprocess(self, filename):
        sectionList = [] 
        for char in open(filename,'r').read():
            self.__tempBuffer += char
            if self.__prevChar=='\\' and char=='\n':
                self.__tempBuffer = self.__tempBuffer[:-2]
            else:
                if self.__insideString:
                    if self.__insideEscape:
                        self.__insideEscape = False
                    elif char=='\\':
                        self.__insideEscape = True
                    elif char=='"':
                        self.__insideString = False
                        sectionList.append(self.__tempBuffer)
                        self.__tempBuffer = ''
                elif self.__insideComment is not None:
                    if char=='\n' and self.__insideComment=='INLINE':
                        self.__insideComment = None
                        self.__tempBuffer = '\n'
                    if self.__prevChar=='*' and char=='/' and self.__insideComment=='BLOCK':
                        self.__insideComment = None
                        self.__tempBuffer = ''
                else:
                    if self.__prevChar=='/':
                        if char=='/':
                            self.__insideComment = 'INLINE'
                            sectionList.append(self.__tempBuffer[:-2])
                            self.__tempBuffer = ''
                        elif char=='*':
                            self.__insideComment = 'BLOCK'
                            sectionList.append(self.__tempBuffer[:-2])
                            self.__tempBuffer = ''
                    elif char=='"':
                        self.__insideString = True
                        sectionList.append(self.__tempBuffer[:-1])
                        self.__tempBuffer = '"'
            self.__prevChar = char
        sectionList.append(self.__tempBuffer)
        return sectionList
