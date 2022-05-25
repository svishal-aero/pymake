#include <stdlib.h>
#include "../Cell.h"

void Cell__init(Cell *self)
{
    self->nFaces = 0;
    self->faces = NULL;
}
