#include <math.h>
#include "../Node.h"

double Node__getDistanceFromNode(Node *self, Node *other)
{
    double dist2 = 0.0;
    for(int i=0; i<3; i++)
    {
        double diff = self->x[i] - other->x[i];
        dist2 += diff * diff;
    }
    return sqrt(dist2);
}
