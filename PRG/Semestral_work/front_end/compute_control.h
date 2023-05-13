#ifndef __COMPUTE_CONTROL_H__
#define __COMPUTE_CONTROL_H__

#include <stdbool.h>

#include "messages.h"

void computation_init(void);
void computation_cleanup(void);

void get_grid_size(int *w, int *h);

bool is_computing(void);
bool is_done(void);

void abort_comp(void);

bool set_compute(message *msg);
bool compute(message *msg);
bool compute_burst(message *msg);

void update_image(int w, int h, unsigned char *img);
void update_data(const msg_compute_data *compute_data);
void update_data_burst(const msg_compute_data_burst *compute_data);


#endif