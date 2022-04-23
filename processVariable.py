def processVariable(tags):

    varname = ''
    varsize = []
    dynsize = []
    stasize = []

    while len(tags)>0:
        if isinstance(tags[0], str):
            if tags[0]=='*':
                dynsize.append(0)
                tags.pop(0)
            else:
                varname = tags[0]
                tags.pop(0)
        else:
            if tags[0].kind=='()':
                varname, varsize = processVariable(tags[0])
                tags.pop(0)
            elif tags[0].kind=='[]':
                stasize.append(int(tags[0].contents[0]))

    varsize.extend(stasize)
    varsize.extend(dynsize)

    return varname, varsize
