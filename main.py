import os, sys
from subprocess import call
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from CStruct import CStruct
from utils import *
sys.path.pop(0)

def make(finished=[]):
    cwd = os.getcwd()
    call('mkdir -p obj', shell=True)
    structName = os.path.basename(cwd)
    struct = CStruct(structName+'.h')
    struct.write()
    depLibsAll = []
    for module in struct.imports:
        if module['path'] not in finished:
            os.chdir(module['path'])
            finished, depLibs = make(finished=finished)
            depLibsAll.extend(depLibs)
            os.chdir(cwd)
    options = readLocalOptions(struct.imports)
    for lib in depLibsAll:
        if lib not in options['L']:
            options['L'].append(lib)
    with open('Makefile', 'w') as f:
        f.write('SRC := $(wildcard src/*.c)\n')
        f.write('OBJ := $(patsubst src/%.c,obj/%.o,$(SRC))')
        f.write('\n\n')
        f.write('CFLAGS :=')
        for flag in options['D']: f.write(' \\\n\t'+flag)
        for flag in options['I']: f.write(' \\\n\t'+flag)
        f.write('\n\n')
        f.write('LDFLAGS :=')
        for flag in options['L'][::-1]: f.write(' \\\n\t'+flag)
        f.write('\n\n')
        f.write('all: lib'+structName+'.so')
        f.write('\n\n')
        f.write('lib'+structName+'.so: $(OBJ)\n')
        f.write('\t'+options['CC']+' $(CFLAGS) -O3 -shared -fPIC -o $@ $^ $(LDFLAGS)')
        f.write('\n\n')
        f.write('obj/%.o: src/%.c '+structName+'.h\n')
        f.write('\t'+ options['CC'] + ' $(CFLAGS) ')
        f.write('-c -O3 -fPIC -o $@ $<')
    call('make -j > make.log 2>&1', shell=True)
    finished.append(cwd)
    print('pymake completed for %s' % cwd)
    return finished, options['L']

def clean():
    cwd = os.getcwd()
    structName = os.path.basename(cwd)
    call('rm -rf make.log __pycache__ obj '+structName+'.py lib'+structName+'.so Makefile', shell=True)
    print('pymake clean completed for %s' % cwd)

def rclean(finished=[]):
    cwd = os.getcwd()
    call('mkdir -p obj', shell=True)
    structName = os.path.basename(cwd)
    struct = CStruct(structName+'.h')
    struct.write()
    for module in struct.imports:
        if module['path'] not in finished:
            os.chdir(module['path'])
            finished = rclean(finished=finished)
            os.chdir(cwd)
    call('rm -rf make.log __pycache__ obj '+structName+'.py lib'+structName+'.so Makefile', shell=True)
    finished.append(cwd)
    print('pymake clean completed for %s' % cwd)
    return finished

if __name__=='__main__':
    if len(sys.argv)==1:        make()
    elif sys.argv[1]=='clean':  clean()
    elif sys.argv[1]=='rclean': rclean()
