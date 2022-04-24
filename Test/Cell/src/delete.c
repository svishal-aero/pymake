#include <stdlib.h>
#include "../Cell.h"

void Cell__delete(Cell *self)
{
    if(self->nodes!=NULL)
    {
        for(int iNode=0; iNode<self->nNodes; iNode++)
            Node__delete(self->nodes + iNode);
        free(self->nodes);
    }
    if(self->faces!=NULL)
    {
        for(int iFace=0; iFace<self->nFaces; iFace++)
            Face__delete(self->faces + iFace);
        free(self->faces);
    }
    Cell__init(self);
}
