import os
from subprocess import call

home = os.environ['HOME']
thisDir = os.path.dirname(os.path.abspath(__file__))

def addToRcFile():
    rcFile = input('Enter the path for the shell rc [default: ~/.bashrc]: ')
    if rcFile=='': rcFile = os.path.join(home, '.bashrc')
    oldContents = open(rcFile, 'r').readlines()
    newContents = []
    editMode = True
    for line in oldContents:
        if line=='# >>> pymake block >>>\n':
            editMode = False
        if editMode:
            newContents.append(line)
        if line=='# <<< pymake block <<<\n':
            editMode = True
    newContents.append(
        '# >>> pymake block >>>\n'
        'export PATH="'+thisDir+':$PATH"\n'
        '# <<< pymake block <<<\n'
    )
    open(rcFile, 'w').write(''.join(newContents))

if __name__=='__main__':
    addToRcFile()
    open('pymake','w').write('#!/bin/bash\npython '+thisDir+'/main.py $@\n')
    call('chmod +x ./pymake', shell=True)
