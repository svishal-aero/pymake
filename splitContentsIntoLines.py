def splitContentsIntoLines(contents):

    lines = []
    tempLine = []

    for token in contents:

        if isinstance(token, str):

            if token in ';\n':
                lines.append(tempLine)
                tempLine = []

            else:
                tempLine.append(token)

        else:
            tempLine.append(token)

    lines.append(tempLine)

    return lines
