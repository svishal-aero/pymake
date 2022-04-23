nameDict = {
    'char'  : 'C.c_char',
    'int'   : 'C.c_int',
    'float' : 'C.c_float',
    'double': 'C.c_double',
    'long'  : 'C.c_long',
    'ulong' : 'C.c_ulong',
}

def getCtypesName(vartype, varsize):

    if len(varsize)>0:

        if varsize[-1]==0 and vartype=='void':
            varsize = varsize[:-1]
            vartype = 'C.c_void_p'

        elif varsize[-1]==0 and vartype=='char':
            varsize = varsize[:-1]
            vartype = 'C.c_char_p'

        elif vartype in nameDict.keys():
            vartype = nameDict[vartype]

    elif vartype in nameDict.keys():
        vartype = nameDict[vartype]
        
    while len(varsize)>0:

        if varsize[-1]==0:
            vartype = 'C.POINTER('+vartype+')'

        else:
            vartype = '('+vartype+')*'+str(varsize[-1])

        varsize = varsize[:-1]
    
    return vartype
