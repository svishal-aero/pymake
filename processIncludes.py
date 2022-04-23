import os

def processIncludes(lines):

    output = ''

    for line in lines:

        if line[0]=='#include':
            
            if line[1][0]=='"':
                filename = os.path.abspath(line[1][1:-1])
                dirname  = os.path.dirname(filename)
                modname  = os.path.basename(dirname)
                output += 'sys.path.insert(0, "%s")\n' % (dirname)
                output += 'from %s import %s\n' % (modname, modname)
                output += 'sys.path.pop(0)\n\n'

    if output!='':
        output = 'import sys\n\n' + output

    return output
