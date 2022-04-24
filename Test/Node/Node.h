#pragma once
#pragma pack(1)

typedef struct Node
{
    double x[3];
}
Node;

void Node__init(Node *self);
void Node__delete(Node *self);
double Node__getDistanceFromNode(Node *self, Node *other);
