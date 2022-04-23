#include <stdio.h>

typedef struct Meow
{
    double x;
    double y;
    char* name;
}
Meow;

void Meow__init(Meow *self);
void Meow__delete(Meow *self);
