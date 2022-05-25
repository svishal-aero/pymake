#pragma once
#pragma pack(1)

#include "../Face/Face.h"

typedef struct Cell
{
    int nFaces;
    Face *faces;
}
Cell;

void Cell__init(Cell *self);
void Cell__delete(Cell *self);
