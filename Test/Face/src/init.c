#include <stdlib.h>
#include "../Face.h"

void Face__init(Face *self)
{
    self->nNodes = 0;
    self->nodes = NULL;
}
