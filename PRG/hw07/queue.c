#include <stdlib.h>
#include <stdbool.h>

#include "queue.h"

typedef struct Node
{
    void *data;
    struct Node *next;
} Node;

typedef struct Queue
{
    Node *head; // first node of the queue for pop
    Node *tail; // last node of the queue for push
    int size;
    int (*compare)(const void *, const void *); // function for comparing two elements of the queue
    void (*clear)(void *);                      // function to free all the data in an element of a queue
} Queue;

void *create()
{
    Queue *queue = (Queue *)malloc(sizeof(Queue));
    if (queue == NULL)
        return NULL;

    queue->head = NULL;
    queue->tail = NULL;
    queue->size = 0;
    queue->compare = NULL;
    queue->clear = NULL;

    return queue;
}

void clear(void *queuePtr)
{
    Queue *queue = (Queue *)queuePtr;
    Node *current = queue->head;
    Node *next;

    while (current != NULL)
    {
        next = current->next;

        if (queue->clear != NULL)
        { // call clear function if present
            queue->clear(current->data);
        }

        else
        { // just free
            free(current->data);
        }
        free(current);
        current = next;
    }

    queue->head = NULL;
    queue->tail = NULL;
    queue->size = 0;
}

_Bool push(void *queuePtr, void *entry)
{
    if (entry == NULL)
        return false;

    Queue *queue = (Queue *)queuePtr;
    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL)
        return false;

    newNode->data = entry;
    newNode->next = NULL;

    if (queue->size == 0)
    { // make the new node the head of the queue
        queue->head = newNode;
        queue->tail = newNode;
    }

    else
    { // add after the tail node
        queue->tail->next = newNode;
        queue->tail = newNode;
    }

    queue->size++;

    return true;
}

void *pop(void *queuePtr)
{
    Queue *queue = (Queue *)queuePtr;
    if (queue->size == 0)
        return NULL;

    // return the head and remove from queue
    Node *temp = queue->head;
    void *data = temp->data;
    queue->head = temp->next;
    queue->size--;

    free(temp);
    return data;
}

_Bool insert(void *queuePtr, void *entry)
{
    if (entry == NULL || queuePtr == NULL)
        return false;

    Queue *queue = (Queue *)queuePtr;
    if (queue->compare == NULL)
        return false;

    Node *newNode = (Node *)malloc(sizeof(Node));
    if (newNode == NULL)
        return false;

    newNode->data = entry;
    newNode->next = NULL;

    Node *current = queue->head;
    Node *prev = NULL;

    // while the queue hasnt ended and the entry is bigger than the current element
    // move through the queue
    while (current != NULL && queue->compare(entry, current->data) < 0)
    {
        prev = current;
        current = current->next;
    }

    if (prev == NULL)
    { // at the head
        newNode->next = queue->head;
        queue->head = newNode;
        if (current == NULL)
        { // empty queue
            queue->tail = newNode;
        }
    }

    else
    { // in the middle
        newNode->next = current;
        prev->next = newNode;

        if (current == NULL)
        { // at the end
            queue->tail = newNode;
        }
    }

    queue->size++;
    return true;
}

_Bool erase(void *queuePtr, void *entry)
{
    if (queuePtr == NULL || entry == NULL)
        return false;

    Queue *queue = (Queue *)queuePtr;
    if (queue->compare == NULL)
        return false;

    Node *current = queue->head;
    Node *prev = NULL;
    _Bool removed = false;

    // going through the whole queue
    while (current != NULL)
    {

        if (queue->compare(entry, current->data) == 0)
        { // if entry and an element are the same
            Node *toRemove = current;
            if (prev == NULL)
            { // moving the head node
                queue->head = current->next;
            }
            else
            {
                prev->next = current->next;
            }

            if (queue->tail == current)
            { // moving the tail node
                queue->tail = prev;
            }

            current = current->next;
            if (queue->clear != NULL)
            { // call clear function if present
                queue->clear(toRemove->data);
            }
            else
            { // just free
                free(toRemove->data);
            }
            free(toRemove);
            queue->size--;
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

void *getEntry(const void *queuePtr, int idx)
{
    const Queue *queue = (const Queue *)queuePtr;
    if (idx < 0 || idx >= queue->size)
        return NULL;

    Node *current = queue->head;

    int i;
    for (i = 0; i < idx; i++)
        current = current->next;

    return current->data;
}

int size(const void *queuePtr)
{
    const Queue *queue = (const Queue *)queuePtr;

    if (queue == NULL)
        return 0;

    return queue->size;
}

void setCompare(void *queuePtr, int (*compare)(const void *, const void *))
{
    Queue *queue = (Queue *)queuePtr;
    queue->compare = compare;
}

void setClear(void *queuePtr, void (*clear)(void *))
{
    Queue *queue = (Queue *)queuePtr;
    queue->clear = clear;
}
