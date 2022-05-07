import os

def readLocalOptions(imports):
    options = {'D':[], 'I':[], 'L':[], 'CC':'gcc'}
    options['L'].extend(getImportFlags(imports))
    if os.path.exists('pyMakeOptions'):
        if os.path.isdir('pyMakeOptions'):
            os.chdir('pyMakeOptions')
            options['D'].extend(getDefFlags())
            options['I'].extend(getIncFlags())
            options['L'].extend(getLibFlags())
            options['CC'] = getCC()
            os.chdir('..')
    return options

def getCC():
    if os.path.exists('cc.txt'):
        return open('cc.txt','r').read().strip()
    else:
        return 'gcc'

def getDefFlags():
    flags = []
    if os.path.exists('def.txt'):
        paths = [line.strip() for line in open('def.txt', 'r').readlines()]
        for path in paths:
            path = os.path.abspath(path)
            flags.append('-D'+path)
    return flags

def getIncFlags():
    flags = []
    if os.path.exists('inc.txt'):
        paths = [line.strip() for line in open('inc.txt', 'r').readlines()]
        for path in paths:
            path = os.path.abspath(path)
            flags.append('-I'+path)
    return flags

def getLibFlags():
    flags = []
    if os.path.exists('lib.txt'):
        paths = [line.strip() for line in open('lib.txt', 'r').readlines()]
        for path in paths:
            path = os.path.abspath(path)
            filename = os.path.basename(path)
            assert len(filename)>6
            assert filename[:3]=='lib' and filename[-3:]=='.so'
            name = filename[3:-3]
            dirname = os.path.dirname(path)
            flags.append('-Wl,-rpath='+dirname+' -L'+dirname+' -l'+name)
    return flags

def getImportFlags(imports):
    flags = []
    for module in imports:
        path = module['path']
        name = os.path.basename(path)
        flags.append('-Wl,-rpath='+path+' -L'+path+' -l'+name)
    return flags
