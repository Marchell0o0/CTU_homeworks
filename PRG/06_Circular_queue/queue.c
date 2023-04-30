#include "queue.h"

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>

queue_t *create_queue(int capacity)
{
    // Allocate memory for the queue structure and initialize its fields
    queue_t *queue = (queue_t *)malloc(sizeof(queue_t));
    queue->array = (void **)malloc(capacity * sizeof(void *));
    queue->capacity = capacity;
    queue->front = -1;
    queue->rear = -1;
    queue->size = 0;

    return queue;
}

void delete_queue(queue_t *queue)
{
    if (queue)
    {
        if (queue->array)
            free(queue->array);
        free(queue);
    }
}

void resize_and_rearrange(queue_t *queue, int new_capacity)
{
    // Allocate memory for the new array with the new capacity
    void **new_array = (void **)malloc(new_capacity * sizeof(void *));

    int index = 0;
    if (queue->front > queue->rear)
    // Transfer from front then from start to rear
    {
        for (int i = queue->front; i < queue->capacity; ++i, ++index)
            new_array[index] = queue->array[i];

        for (int i = 0; i <= queue->rear; ++i, ++index)
            new_array[index] = queue->array[i];
    }
    // Transfer values one for one
    else
    {
        for (int i = queue->front; i <= queue->rear; ++i, ++index)
            new_array[index] = queue->array[i];
    }

    free(queue->array);
    queue->array = new_array;
    queue->capacity = new_capacity;
    queue->front = 0;
    queue->rear = index - 1;

    return;
}

bool push_to_queue(queue_t *queue, void *data)
{
    // Resize the queue if it is full
    if (queue->size == queue->capacity)
    {
        int new_capacity = queue->capacity * 2;
        resize_and_rearrange(queue, new_capacity);
    }

    // Update front index if it is the first element
    if (queue->front == -1)
        queue->front = 0;

    // Update rear index, size and add the element to the queue
    queue->rear = (queue->rear + 1) % queue->capacity;
    queue->array[queue->rear] = data;
    queue->size++;

    return true;
}

void *pop_from_queue(queue_t *queue)
{
    // Return NULL if the queue is empty
    if (queue->size == 0)
    {
        return NULL;
    }

    // Get the first element and update the front index and size
    void *data = queue->array[queue->front];
    queue->front = (queue->front + 1) % queue->capacity;
    queue->size--;

    // Reset front and rear indices if the queue is empty
    if (queue->size == 0)
    {
        queue->front = -1;
        queue->rear = -1;
    }

    // Shrink the array if necessary
    else if (queue->size <= queue->capacity / 2)
    {
        int new_capacity = queue->capacity / 2 + 1;
        resize_and_rearrange(queue, new_capacity);
    }
    return data;
}

void *get_from_queue(queue_t *queue, int idx)
{
    if (idx < 0 || idx >= queue->size)
        return NULL;

    int index = (queue->front + idx) % queue->capacity;
    return queue->array[index];
}

int get_queue_size(queue_t *queue)
{
    return queue->size;
}
