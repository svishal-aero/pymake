import os
from .CParser import CParser
from .CParser.Scope import Scope as CScope

def containsPackStatement(statement):
    if statement[0]=='#pragma':
        if statement[1]=='pack':
            return True
    return False

def containsModuleImport(statement):
    if statement[0]=='#include':
        if statement[1][0]=='"':
            return True
    return False

def containsStructDefinition(statement):
    if statement[0]=='typedef' and statement[1]=='struct':
        assert isinstance(statement[2],str),\
                'Error: Unnamed struct'
        if isinstance(statement[3],CScope):
            assert statement[2]==statement[-1],\
                    'Error: Struct name must match alias'
            assert statement[2]==os.path.basename(os.getcwd()),\
                    'Error: Directory name must match struct name'
            return True
    return False

def containsFunctionDeclaration(statement):
    if isinstance(statement[-1],CScope):
        if statement[0] not in ['static','inline'] and\
           statement[0][0]!='#':
            return True
    return False

def getStatementsFromHeader(filename):
    header = CParser(filename)
    statements = []
    tempStatement = []
    for token in header.contents:
        if str(token) in ';\n':
            statements.append(tempStatement)
            tempStatement = []
        else:
            tempStatement.append(token)
    if len(tempStatement)>0:
        statements.append(tempStatement)
    return statements

def getCtypesName(classname, vartype, varsize):        
    nameDict = {
        'int'   : 'C.c_int'   , 'float' : 'C.c_float',
        'double': 'C.c_double', 'long'  : 'C.c_long' ,
        'ulong' : 'C.c_ulong' , 'char'  : 'C.c_char' ,
    }
    if len(varsize)==0:
        if vartype=='void':
            vartype = 'None'
        elif vartype in nameDict:
            vartype = nameDict[vartype] 
    else:
        if varsize[-1]==0 and vartype in ['void', classname]:
            varsize = varsize[:-1]
            vartype = 'C.c_void_p'
        elif varsize[-1]==0 and vartype=='char':
            varsize = varsize[:-1]
            vartype = 'C.c_char_p'
        elif vartype in nameDict:
            vartype = nameDict[vartype]
        while len(varsize)>0:
            if varsize[-1]==0: vartype = 'C.POINTER('+vartype+')'
            else: vartype = '('+vartype+')*'+str(varsize[-1])
            varsize = varsize[:-1]
    return vartype

def processVariable(tags):
    varname     = ''
    varsize     = []
    dynamicSize = []
    staticSize  = []
    while len(tags)>0:
        if isinstance(tags[0], str):
            if tags[0]=='*':
                dynamicSize.append(0)
                tags.pop(0)
            else:
                varname = tags[0]
                tags.pop(0)
        else:
            if tags[0].kind=='()':
                varname, varsize = processVariable(tags[0].contents)
                tags.pop(0)
            elif tags[0].kind=='[]':
                staticSize.append(int(tags[0].contents[0]))
                tags.pop(0)
    varsize.extend(staticSize)
    varsize.extend(dynamicSize)
    return varname, varsize

def getVar(vartype, varname):
    varname, varsize = processVariable(varname)
    return {'type': vartype, 'name': varname, 'size': varsize}

def processFunctionArgs(args, classname):
    argVars = []
    argtype = ''
    argname = []
    for iToken in range(len(args)):
        token = args[iToken]
        if argtype=='':
            argtype = token
        elif str(token)==',':
            argVars.append(getVar(argtype, argname))
            argtype = ''
            argname = []
        else: argname.append(token)
    if argtype!='':
        argVars.append(getVar(argtype, argname))
    assert len(argVars)>0,\
        'Error: Argument list must contain atleast one argument '\
        'where first argument must be "'+classname+' *self"'
    assert argVars[0]['type']==classname and\
           argVars[0]['size']==[0] and\
           argVars[0]['name']=='self',\
        'Error: First argument must be "'+classname+' *self"'
    return argVars
