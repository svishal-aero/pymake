#include "../Node.h"

void Node__init(Node *self)
{
    for(int i=0; i<3; i++)
        self->x[i] = 0.0;
}
