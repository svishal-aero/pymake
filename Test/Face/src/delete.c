#include <stdlib.h>
#include "../Face.h"

void Face__delete(Face *self)
{
    if(self->nodes!=NULL)
    {
        for(int iNode=0; iNode<self->nNodes; iNode++)
            Node__delete(self->nodes);
        free(self->nodes);
    }
    Face__init(self);
}
