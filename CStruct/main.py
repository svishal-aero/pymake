import os
from .utils import *

class CStruct:

    def __init__(self, filename):
        self.name      = ''
        self.pack      = None
        self.imports   = []
        self.vars      = []
        self.functions = []
        self.__processHeader(filename)

    def write(self):
        open(self.name+'.py','w').write(self.__writePythonFile())

    def __processHeader(self, filename):
        statements = getStatementsFromHeader(filename)
        assert statements[0][0]=='#pragma' and statements[0][1]=='once',\
               'First line must be "#pragma once"'
        assert statements[1][0]=='#pragma' and statements[1][1]=='pack' and\
               statements[1][2].kind=='()' and statements[1][2].contents[0]=='1',\
               'Second line must be "#pragma pack(1)"'
        for statement in statements:
            if containsPackStatement(statement):
                self.pack = int(statement[-1].contents[0])
            if containsModuleImport(statement):
                self.__processImport(statement[1][1:-1])
            if containsStructDefinition(statement):
                self.name = statement[-1]
                structContents = statement[3].contents
                self.__processStructContents(structContents)
            if containsFunctionDeclaration(statement):
                assert self.name!='', 'Function defined before struct'
                self.__processFunction(statement)
        assert self.name!='',\
            'No struct found in file, please refer '\
            'to the format mentioned in the manual'

    def __processImport(self, filepath):
        dirname = os.path.dirname(os.path.abspath(filepath))
        modname = os.path.basename(dirname)
        self.imports.append( {'name':modname, 'path':dirname} )

    def __processStructContents(self, contents):
        statement = []
        for iToken in range(len(contents)):
            token = contents[iToken]
            statement.append(token)
            if str(token)==';':
                self.__processStructStatement(statement)
                statement = []

    def __processStructStatement(self, statement):
        vartype = statement[0]
        varname = []
        for iToken in range(1, len(statement)):
            token = statement[iToken]
            if str(token) in ',;':
                newVar = getVar(vartype, varname)
                self.vars.append(newVar)
                varname = []
            else: varname.append(token)

    def __processFunction(self, statement):
        fn = {'type': statement[0]}
        fnName, fnSize = processVariable(statement[1:-1])
        fn['name'] = fnName[len(self.name)+2:]
        fn['size'] = fnSize
        assert fnName[:len(self.name)+2]==self.name+'__',\
            'Error: Function name does not start with "'+self.name+'__"'
        args = statement[-1].contents
        fn['args'] = processFunctionArgs(args, self.name)
        self.functions.append(fn)

    def __writePythonFile(self):
        output  = 'import ctypes as C\n\n'
        output += self.__writeImports()
        output += 'lib = C.CDLL("%s")\n\n' %\
                  os.path.join(os.getcwd(), 'lib'+self.name+'.so')
        output += self.__writeStruct()
        return output

    def __writeImports(self):
        output = ''
        for module in self.imports:
            output += 'sys.path.insert(0, "%s")\n' % (module['path'])
            output += 'from %s import %s\n' % (module['name'], module['name'])
            output += 'sys.path.pop(0)\n\n'
        if output!='':
            output = 'import sys\n\n' + output
        return output

    def __writeStruct(self):
        output  = 'class %s(C.Structure):\n\n' % self.name
        if self.pack is not None: output  = '    _pack_ = %d\n' % (self.pack)
        output += self.__writeStructFields()
        for fn in self.functions:
            output += self.__writeFunctionDeclaration(fn)
        for fn in self.functions:
            output += self.__writeFunctionDefinition(fn)
        return output

    def __writeStructFields(self):
        output = '    _fields_ = [\n'
        for var in self.vars:
            varType = getCtypesName(self.name, var['type'], var['size'])
            output += '        ("%s", %s),\n' % (var['name'], varType)
        output += '    ]\n\n'
        return output

    def __writeFunctionDeclaration(self, fn):
        fnType  = getCtypesName(self.name, fn['type'], fn['size'])
        output  = '    _%s = lib.%s__%s\n' % (fn['name'], self.name, fn['name'])
        output += '    _%s.restype = %s\n' % (fn['name'], fnType)
        output += '    _%s.argtypes = [\n' % (fn['name'])
        for arg in fn['args']:
            argType = getCtypesName(self.name, arg['type'], arg['size'])
            output += '        %s,\n' % (argType)
        output += '    ]\n\n'
        return output

    def __writeFunctionDefinition(self, fn):
        if fn['name']=='init':
            output = '    def __init__(\n'
        else:
            output = '    def %s(\n' % (fn['name'])
        for arg in fn['args']:
            output += '        %s,\n' % (arg['name'])
        output += '    ):\n'
        output += '        return self._%s(\n' % (fn['name'])
        for arg in fn['args']:
            if getCtypesName(self.name, arg['type'], arg['size'])=='C.c_void_p':
                output += '            C.addressof(%s),\n' % (arg['name'])
            else:
                output += '            %s,\n' % (arg['name'])
        output += '        )\n\n'
        return output
