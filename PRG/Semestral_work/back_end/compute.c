

#include <stdlib.h>
#include "utils.h"
#include "messages.h"

#include "compute.h"

static struct {
    int cid;               // Chunk id
    double re;             // Start of real coordinates of the chunk
    double im;             // Start of imaginary coordinates of the chunk
    uint8_t n_re;          // Width of one chunk
    uint8_t n_im;          // Height of one chunk
    double c_re;           // Real part of the constant c
    double c_im;           // Imaginary part of the constant c
    double d_re;           // Width of one dot in numerical representation
    double d_im;           // Height of one dot in numerical representation
    int n;                 // Number of iterations
} chunk = { .cid = 0 };

static int r = 0;
static int c = 0;

bool compute_chunk(message *compute_data) {
    if (r < chunk.n_re && c < chunk.n_im) {
        compute_data->data.compute_data.cid = chunk.cid;
        compute_data->data.compute_data.i_re = r;
        compute_data->data.compute_data.i_im = c;
        compute_data->data.compute_data.iter = compute(r, c);
        c++;
        if (c == chunk.n_im) {
            c = 0;
            r++;
        }
        return true;
    } else {
        r = 0;
        c = 0;
        return false;
    }
}

uint8_t compute(int r, int c){
    double new_real, new_imag;
    double real, imag;

    real = chunk.re + (r * chunk.d_re);
    imag = chunk.im + (c * chunk.d_im);

    uint8_t k;
    for (k = 0; k < chunk.n; ++k){
        new_real = real * real - imag * imag + chunk.c_re;
        new_imag = 2.0 * real * imag + chunk.c_im;
        real = new_real;
        imag = new_imag;

        if(real * real + imag * imag > 4.0) {
            return k;
        }
    }
    return k;
}

void compute_chunk_burst(message *msg){
    msg->type = MSG_COMPUTE_DATA_BURST;
    msg->data.compute_data_burst.cid = chunk.cid;
    msg->data.compute_data_burst.length = chunk.n_re * chunk.n_im;
    msg->data.compute_data_burst.iters = my_malloc(sizeof(uint8_t) * chunk.n_re * chunk.n_im);

    for (int r = 0; r < chunk.n_re; ++r){
        for (int c = 0; c < chunk.n_im; ++c){
        msg->data.compute_data_burst.iters[r + (c * chunk.n_re)] = compute(r, c);
        }
    }
}

void set_compute(const message *msg){
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);
    chunk.c_re = msg->data.set_compute.c_re;
    chunk.c_im = msg->data.set_compute.c_im;
    chunk.d_re = msg->data.set_compute.d_re;
    chunk.d_im = msg->data.set_compute.d_im;
    chunk.n = msg->data.set_compute.n;
}

void set_chunk(const message *msg){
    my_assert(msg != NULL, __func__, __LINE__, __FILE__);

    chunk.cid = msg->data.compute.cid;
    chunk.re = msg->data.compute.re; // starting real coordinates
    chunk.im = msg->data.compute.im; // starting imaginary coordinates
    chunk.n_re = msg->data.compute.n_re; // width of one chunk
    chunk.n_im = msg->data.compute.n_im; // height of one chunk
}


