#pragma once

#include "../Node/Node.h"

#pragma pack(1)
typedef struct Face
{
    int nNodes;
    Node *nodes;
}
Face;
#pragma pack()

void Face__init(Face *self);
void Face__delete(Face *self);
