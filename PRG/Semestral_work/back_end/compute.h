#ifndef __COMPUTE_H__
#define __COMPUTE_H__

#include <stdbool.h>

#include "messages.h"

void set_compute(const message *msg);
void set_chunk(const message *msg);
void chunk_reset(void);
uint8_t compute(int r, int c);

bool compute_chunk(message *compute_data);

void compute_chunk_burst(message *msg);


#endif