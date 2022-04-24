#pragma once
#pragma pack(1)

#include "../Node/Node.h"

typedef struct Face
{
    int nNodes;
    Node *nodes;
}
Face;

void Face__init(Face *self);
void Face__delete(Face *self);
