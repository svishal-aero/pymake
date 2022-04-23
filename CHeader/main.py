from .Scope import Scope

class CHeader:

    def __init__(self, filename):

        self.__tempBuffer    = ''
        self.__prevChar      = ''
        self.__insideString  = False
        self.__insideEscape  = False
        self.__insideComment = None

        sectionList   = self.preprocess(filename)
        sectionList   = self.removeNewlines(sectionList)
        tokenList     = self.tokenize(sectionList)
        self.contents = self.extractContents(tokenList)

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

            if section[0]!="":

                for c in '[]{}()*;,\n':
                    section = section.replace(c, ' '+c+' ')
                section = section.replace('\t', ' ')

                tempList = section.split(' ')

                while '' in tempList:
                    tempList.remove('')

            else:
                tempList = [section]

            tokenList.extend(tempList)

        return tokenList

    def removeNewlines(self, sectionList): 

        newSectionList = []

        for section in sectionList:

            if section[0]!='"':

                sectionLines = [line.strip() for line in section.split('\n')]

                for iLine in range(len(sectionLines)):
                    if len(sectionLines[iLine])>0:
                        if sectionLines[iLine][0]=='#':
                            sectionLines[iLine] += '\n'

                newSection = ' '.join(sectionLines)

            else:
                newSection = section

            newSectionList.append(newSection)

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
                            self.tempBuffer = ''

                        elif char=='*':
                            self.__insideComment = 'BLOCK'
                            sectionList.append(self.__tempBuffer[:-2])
                            self.tempBuffer = ''

                    elif char=='"':
                        self.__insideString = True
                        sectionList.append(self.__tempBuffer[:-1])
                        self.tempBuffer = '"'

            self.__prevChar = char

        sectionList.append(self.__tempBuffer)

        return sectionList
