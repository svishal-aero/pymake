#include <stdlib.h>
#include "../Cell.h"

void Cell__delete(Cell *self)
{
    if(self->faces!=NULL)
    {
        for(int iFace=0; iFace<self->nFaces; iFace++)
            Face__delete(self->faces + iFace);
        free(self->faces);
    }
    Cell__init(self);
}
