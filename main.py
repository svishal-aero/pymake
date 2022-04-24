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
    for module in struct.imports:
        if module['path'] not in finished:
            os.chdir(module['path'])
            finished = make(finished=finished)
            os.chdir(cwd)
    options = readLocalOptions(struct.imports)
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
        f.write('\t'+options['CC']+' -O3 -shared -fPIC -o $@ $^ $(LDFLAGS)')
        f.write('\n\n')
        f.write('obj/%.o: src/%.c '+structName+'.h\n')
        f.write('\t'+ options['CC'] + ' $(CFLAGS) ')
        f.write('-c -O3 -fPIC -o $@ $<')
        f.write('\n\n')
        f.write('clean:\n')
        f.write('\trm -rf __pycache__ obj ' + \
                structName+'.py lib'+structName+'.so Makefile\n')
    call('make -j', shell=True)
    finished.append(cwd)
    return finished

def clean():
    cwd = os.getcwd()
    structName = os.path.basename(cwd)
    call('rm -rf __pycache__ obj '+structName+'.py lib'+structName+'.so Makefile', shell=True)

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
    call('make clean', shell=True)
    finished.append(cwd)
    return finished

if __name__=='__main__':
    if len(sys.argv)==1:
        finished = make()
        print('Recursive make order:')
        for entry in finished:
            print('    %s' % entry)
    elif sys.argv[1]=='clean':
        clean()
    elif sys.argv[1]=='rclean':
        finished = rclean()
        print('Recursive make clean order:')
        for entry in finished:
            print('    %s' % entry)
