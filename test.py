from CHeader import CHeader
from CHeader.Scope import Scope

header = CHeader('test.h')
mainScope = Scope()
mainScope.contents = header.contents
print(mainScope.combineContents())
