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
    open(rcFile, 'w').write(''.join(newContents))

if __name__=='__main__':
    addToRcFile()
    call('rm ./pymake', shell=True)
