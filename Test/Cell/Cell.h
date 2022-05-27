#pragma once

#include "../Face/Face.h"

#pragma pack(2)
typedef struct Cell
{
    int nFaces;
    Face *faces;
}
Cell;
#pragma pack()

void Cell__init(Cell *self);
void Cell__delete(Cell *self);
