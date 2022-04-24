#ifndef Cell_h
#define Cell_h

#include "../Node/Node.h"
#include "../Face/Face.h"

typedef struct Cell
{
    int nNodes, nFaces;
    Node *nodes; Face *faces;
}
Cell;

void Cell__init(Cell *self);
void Cell__delete(Cell *self);

#endif
