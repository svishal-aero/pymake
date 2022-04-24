from .Scope import Scope

class CParser:

    def __init__(self, filename):
        sectionList   = self.__preprocess(filename)
        sectionList   = self.__removeNewlines(sectionList)
        tokenList     = self.__tokenize(sectionList)
        contents      = self.__extractContents(tokenList)
        self.contents = self.__addNewlines(contents)

    def __addNewlines(self, contents):
        newContents = []
        lastScopeKind = ''
        for iToken in range(len(contents)):
            token = contents[iToken]
            newContents.append(token)
            if isinstance(token, Scope):
                token.contents = self.__addNewlines(token.contents)
                if lastScopeKind=='()' and token.kind=='{}':
                    newContents.append('\n')
                lastScopeKind = token.kind
            else:
                lastScopeKind = ''
        return newContents

    def __extractContents(self, tokenList):
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
    
    def __tokenize(self, sections):
        tokenList = []
        for section in sections:
            sectionTokenList = []
            if section[0]!='"':
                for sep in '[]{}();,+-*/\n':
                    section = section.replace(sep, ' '+sep+' ')
                section = section.replace('\t', ' ')
                sectionTokenList = section.split(' ')
                while '' in sectionTokenList:
                    sectionTokenList.remove('')
            else:
                sectionTokenList.append(section)
            tokenList.extend(sectionTokenList)
        return tokenList

    def __removeNewlines(self, sections): 
        newSections   = []
        insideMacro   = False
        prevIsNewline = True
        for section in sections:
            newSection = ''
            if section[0]=='"':
                newSection = section
            else:
                for char in section:
                    newSection += char
                    if prevIsNewline:
                        if char=='#': insideMacro = True
                        elif char not in ' \t\n': prevIsNewline = False
                    if char=='\n':
                        prevIsNewline = True
                        if insideMacro: insideMacro = False
                        else: newSection = newSection[:-1]
            if len(newSection)>0: newSections.append(newSection)
        return newSections

    def __preprocess(self, filename):
        vars = {}
        vars['buffer'   ] = ''
        vars['inString' ] = False
        vars['inEscape' ] = False
        vars['inComment'] = None
        vars['sections' ] = []
        for char in open(filename,'r').read():
            vars['buffer'] += char
            if self.__removeContinuationCharacter(vars): continue
            if self.__processEscapeSequence(vars): continue
            if self.__processStringBeg(vars): continue
            if self.__processCommentBeg(vars): continue
            if self.__processStringEnd(vars): continue
            if self.__processCommentEnd(vars): continue
        vars['sections'].append(vars['buffer'])
        return vars['sections']

    def __removeContinuationCharacter(self, vars):
        if len(vars['buffer'])>1:
            char = vars['buffer'][-1]
            prev = vars['buffer'][-2]
            if prev=='\\' and char=='\n':
                vars['buffer'] = vars['buffer'][:-2]
                return True
        return False

    def __processEscapeSequence(self, vars):
        if len(vars['buffer'])>0:
            char = vars['buffer'][-1]
            if vars['inString']:
                if vars['inEscape']:
                    vars['inEscape'] = False
                    return True
                elif char=='\\':
                    vars['inEscape'] = True
                    return True
        return False

    def __processStringBeg(self, vars):
        if len(vars['buffer'])>0:
            char = vars['buffer'][-1]
            if not vars['inString'] and not vars['inComment'] and char=='"':
                vars['sections'].append(vars['buffer'][:-1])
                vars['buffer']   = '"'
                vars['inString'] = True
                return True
        return False

    def __processCommentBeg(self, vars):
        if len(vars['buffer'])>1:
            char = vars['buffer'][-1]
            prev = vars['buffer'][-2]
            if not vars['inString'] and not vars['inComment'] and prev=='/':
                if char=='/':
                    vars['sections'].append(vars['buffer'][:-2])
                    vars['buffer']    = ''
                    vars['inComment'] = 'INLINE'
                    return True
                elif char=='*':
                    vars['sections'].append(vars['buffer'][:-2])
                    vars['buffer']    = ''
                    vars['inComment'] = 'BLOCK'
                    return True
        return False

    def __processStringEnd(self, vars):
        if len(vars['buffer'])>0:
            char = vars['buffer'][-1]
            if vars['inString'] and not vars['inEscape'] and char=='"':
                vars['sections'].append(vars['buffer'])
                vars['buffer']   = ''
                vars['inString'] = False
                return True
        return False

    def __processCommentEnd(self, vars):
        if len(vars['buffer'])>1:
            char = vars['buffer'][-1]
            prev = vars['buffer'][-2]
            if vars['inComment'] is not None:
                if char=='\n' and vars['inComment']=='INLINE':
                    vars['buffer']    = '\n'
                    vars['inComment'] = None
                    return True
                if prev=='*' and char=='/' and vars['inComment']=='BLOCK':
                    vars['buffer']    = ''
                    vars['inComment'] = None
                    return True
        return False
