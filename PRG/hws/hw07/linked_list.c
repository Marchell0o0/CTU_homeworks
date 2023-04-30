#include <stdlib.h>
#include <stdbool.h>

#include "linked_list.h"

typedef struct Node
{
    int data;
    struct Node *next;
} Node;

Node *head = NULL;
Node *tail = NULL;
int size_of_queue = 0;

_Bool push(int entry)
{
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL)
        return false;

    newNode->data = entry;
    newNode->next = NULL;

    if (size_of_queue == 0)
    { // make the new node the head of the queue
        head = newNode;
        tail = newNode;
    }

    else
    { // add after the tail node
        tail->next = newNode;
        tail = newNode;
    }

    size_of_queue++;

    return true;
}

int pop(void)
{
    if (size_of_queue == 0)
        return -1;

    // return the head and remove from queue
    Node *temp = head;
    int data = temp->data;
    head = temp->next;
    size_of_queue--;

    free(temp);
    return data;
}

_Bool insert(int entry)
{
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL)
        return false;

    newNode->data = entry;
    newNode->next = NULL;

    Node *current = head;
    Node *prev = NULL;

    // while the queue hasnt ended and the entry is bigger than the current element
    // move through the queue
    int idx = 0;
    while (current != NULL && (entry < current->data))
    {
        prev = current;
        current = current->next;
        idx++;
    }

    if (prev == NULL)
    { // at the head
        newNode->next = head;
        head = newNode;
        if (current == NULL)
        { // empty queue
            tail = newNode;
        }
    }

    else
    { // in the middle
        newNode->next = current;
        prev->next = newNode;

        if (current == NULL)
        { // at the end
            tail = newNode;
        }
    }

    size_of_queue++;
    return true;
}

_Bool erase(int entry)
{
    Node *current = head;
    Node *prev = NULL;
    _Bool removed = false;

    // going through the whole queue
    while (current != NULL)
    {

        if (entry == current->data)
        { // if entry and an element are the same
            Node *toRemove = current;
            if (prev == NULL)
            { // moving the head node
                head = current->next;
            }
            else
            {
                prev->next = current->next;
            }

            if (tail == current)
            { // moving the tail node
                tail = prev;
            }

            current = current->next;
            free(toRemove);

            size_of_queue--;
            removed = true;
        }
        else
        {
            prev = current;
            current = current->next;
        }
    }

    return removed;
}

int getEntry(int idx)
{
    if (idx < 0 || idx >= size_of_queue)
        return EXIT_FAILURE;

    Node *current = head;

    int i;
    for (i = 0; i < idx; i++)
        current = current->next;

    return current->data;
}

int size(void)
{
    return size_of_queue;
}

void clear()
{
    Node *current = head;
    Node *next;

    while (current != NULL)
    {
        next = current->next;

        free(current);
        current = next;
    }

    head = NULL;
    size_of_queue = 0;
}
