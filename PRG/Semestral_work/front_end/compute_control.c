#include <stdlib.h>
#include <stdio.h>
#include <math.h>

#include "compute_control.h"
#include "utils.h"

static struct{
    double c_re; // c constant
    double c_im;
    int n;

    double range_re_min;
    double range_re_max;
    double range_im_min;
    double range_im_max;

    int grid_w;
    int grid_h;

    int cur_x;
    int cur_y;

    double d_re;
    double d_im;

    int nbr_chunks;
    int cid;
    double chunk_re; // chunk real start
    double chunk_im; // chunk imaginary start

    uint8_t chunk_n_re; // width of one chunk
    uint8_t chunk_n_im; // height of one chunk

    uint8_t *grid;
    bool computing;
    bool done;
} comp = {
    .c_re = -0.72, 
    .c_im = -0.28,

    .n = 97,
    .range_re_min = -1.6,
    .range_re_max = 1.6,
    .range_im_min = -1.1,
    .range_im_max = 1.1,

    .grid = NULL,
    .grid_w = 1500,
    .grid_h = 1000,

    .chunk_n_re = 25, 
    .chunk_n_im = 25,

    .computing = false,
    .done = false
};
asdfasdf
void computation_init(void)
{
    comp.grid = my_malloc(comp.grid_w * comp.grid_h);
    comp.d_re = (comp.range_re_max - comp.range_re_min) / (1. * comp.grid_w);
    comp.d_im = -(comp.range_im_max - comp.range_im_min) / (1. * comp.grid_h);
    comp.nbr_chunks = (comp.grid_w * comp.grid_h) / (comp.chunk_n_re * comp.chunk_n_im);
}
void computation_cleanup(void)
{
    if (comp.grid){
    free(comp.grid);
    }
    comp.grid = NULL;
}

bool is_computing(void){ return comp.computing; }
bool is_done(void){ return comp.done; }
void abort_comp(void){ comp.computing = false; comp.done = false; }

void get_grid_size(int *w, int *h)
{
    *w = comp.grid_w;
    *h = comp.grid_h;
}




bool set_compute(message *msg)
{
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);

    bool ret  = !is_computing();
    if (ret){
        msg->type = MSG_SET_COMPUTE;
        msg->data.set_compute.c_re = comp.c_re;
        msg->data.set_compute.c_im = comp.c_im;
        msg->data.set_compute.d_re = comp.d_re;
        msg->data.set_compute.d_im = comp.d_im;
        msg->data.set_compute.n = comp.n;
        comp.done = false;
        fprintf(stderr, "INFO: Setting compute, resolution %dx%d\n", comp.grid_w, comp.grid_h);

    }
    return ret;
}
bool compute(message *msg){
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);

    if (!is_computing()){ // first chunk
        comp.cid = 0;
        comp.computing = true;
        comp.done = false;
        comp.cur_x = comp.cur_y = 0; // start computation of the whole image
        comp.chunk_re = comp.range_re_min; // upper-"left" corner
        comp.chunk_im = comp.range_im_max; // "upper"-left corner
        msg->type = MSG_COMPUTE;
    } else { // next chunk
        comp.cid += 1;
        if (comp.cid < comp.nbr_chunks) {
            comp.cur_x += comp.chunk_n_re;
            comp.chunk_re += comp.chunk_n_re * comp.d_re;
            if (comp.cur_x >= comp.grid_w) {
                comp.chunk_re = comp.range_re_min;
                comp.chunk_im += comp.chunk_n_im * comp.d_im;
                comp.cur_x = 0;
                comp.cur_y += comp.chunk_n_im;
            }
            msg->type = MSG_COMPUTE;
        } else { // everything has been computed
        }
    }

    fprintf(stderr, "INFO: Sending a new chunk of data cid: %d\n", comp.cid);

    if (comp.computing && msg->type == MSG_COMPUTE){
        msg->data.compute.cid = comp.cid;
        msg->data.compute.re = comp.chunk_re;
        msg->data.compute.im = comp.chunk_im;
        msg->data.compute.n_re = comp.chunk_n_re;
        msg->data.compute.n_im = comp.chunk_n_im;
    }
    return is_computing();
}

bool compute_burst(message *msg){
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);

    if (!is_computing()){ // first chunk
        comp.cid = 0;
        comp.computing = true;
        comp.done = false;
        comp.cur_x = comp.cur_y = 0; // start computation of the whole image
        comp.chunk_re = comp.range_re_min; // upper-"left" corner
        comp.chunk_im = comp.range_im_max; // "upper"-left corner
        msg->type = MSG_COMPUTE_BURST;
    } else { // next chunk
        comp.cid += 1;
        if (comp.cid < comp.nbr_chunks) {
            comp.cur_x += comp.chunk_n_re;
            comp.chunk_re += comp.chunk_n_re * comp.d_re;
            if (comp.cur_x >= comp.grid_w) {
                comp.chunk_re = comp.range_re_min;
                comp.chunk_im += comp.chunk_n_im * comp.d_im;
                comp.cur_x = 0;
                comp.cur_y += comp.chunk_n_im;
            }
            msg->type = MSG_COMPUTE_BURST;
        } else { // everything has been computed
        }
    }

    fprintf(stderr, "INFO: Sending a new chunk of data cid: %d\n", comp.cid);

    if (comp.computing && msg->type == MSG_COMPUTE_BURST){
        msg->data.compute.cid = comp.cid;
        msg->data.compute.re = comp.chunk_re;
        msg->data.compute.im = comp.chunk_im;
        msg->data.compute.n_re = comp.chunk_n_re;
        msg->data.compute.n_im = comp.chunk_n_im;
    }
    return is_computing();
}

void update_image(int w, int h, unsigned char *img)
{
    my_assert(img && comp.grid && w == comp.grid_w && h == comp.grid_h, __func__, __LINE__,__FILE__);
    for (int i = 0; i < w*h; ++i) {
        const double t = 1. * comp.grid[i] / (comp.n + 1.0);
        // inverted colors
        // *(img++) = 255 - 9 * (1-t)*t*t*t * 255;
        // *(img++) = 255 - 15 * (1-t)*(1-t)*t*t * 255;
        // *(img++) = 255 - 8.5 * (1-t)*(1-t)*(1-t)*t * 255;

        // original
        *(img++) = 9 * (1-t)*t*t*t * 255;
        *(img++) = 15 * (1-t)*(1-t)*t*t * 255;
        *(img++) = 8.5 * (1-t)*(1-t)*(1-t)*t * 255;

        //yellow to purple
        // *(img++) = 128 * (1-t) + t * 255;
        // *(img++) = 0 * (1-t) + t * 255;
        // *(img++) = 128 * (1-t) + t * 0;

        // *(img++) = 255 - t * 255;
        // *(img++) = 255 - t * 255;
        // *(img++) = 255 - t * 255;

    }
}


void update_data(const msg_compute_data *compute_data)
{
    my_assert(compute_data != NULL, __func__, __LINE__, __FILE__);

    if (compute_data->cid == comp.cid) {
        const int idx = (comp.cur_x + compute_data->i_re) + (comp.cur_y + compute_data->i_im) * comp.grid_w;
        if (idx >= 0 && idx < (comp.grid_w * comp.grid_h)) {
            comp.grid[idx] = compute_data->iter;
        }
        if ((comp.cid + 1) >= comp.nbr_chunks && (compute_data->i_re + 1) == comp.chunk_n_re && (compute_data->i_im + 1) == comp.chunk_n_im){
            comp.done = true;
            comp.computing = false;
        }
    } else {
        fprintf(stderr, "Received chunk with unexpected id %d\n", compute_data->cid);
    }
}

void update_data_burst(const msg_compute_data_burst *compute_data)
{
    my_assert(compute_data != NULL, __func__, __LINE__, __FILE__);

    if (compute_data->cid == comp.cid) {
        for (int i = 0; i <= compute_data->length; ++i){
            const int idx = comp.cur_x  + comp.cur_y * comp.grid_w + (i % comp.chunk_n_re) + (i / comp.chunk_n_im) * comp.chunk_n_im;
            if (idx >= 0 && idx < (comp.grid_w * comp.grid_h)) {
                comp.grid[idx] = compute_data->iters[i];
            }
        }
        if ((comp.cid + 1) >= comp.nbr_chunks){
            comp.done = true;
            comp.computing = false;
        }
        // free(compute_data->iters);
    } else {
        fprintf(stderr, "Received chunk with unexpected id %d\n", compute_data->cid);
    }
}
