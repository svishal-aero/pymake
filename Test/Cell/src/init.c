#include <stdlib.h>
#include "../Cell.h"

void Cell__init(Cell *self)
{
    self->nNodes = 0;
    self->nodes = NULL;
    self->nFaces = 0;
    self->faces = NULL;
}
