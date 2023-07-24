
#include <stdlib.h>
#include <stdio.h>
#include <pthread.h>
#include <unistd.h>

#include "utils.h"
#include "prg_io_nonblock.h"
#include "event_queue.h"
#include "messages.h"
#include "compute_thread.h"

#ifndef IO_READ_TIMEOUT_MS
#define IO_READ_TIMEOUT_MS 100
#endif

void* pipe_rear_thread(void* d);

int main(int argc, char* argv[]){
    int ret = EXIT_SUCCESS;

    const char *fname_pipe_in = argc > 1 ? argv[1] : "/tmp/computational_module.in";
    const char *fname_pipe_out = argc > 2 ? argv[2] : "/tmp/computational_module.out";

    int pipe_in = io_open_read(fname_pipe_in);
    int pipe_out = io_open_write(fname_pipe_out);

    my_assert(pipe_in != -1 && pipe_out != -1, __func__, __LINE__, __FILE__);

    enum { PIPE_REAR_THRD, COMPUTE_THRD, NUM_THREADS };

    const char *thrd_names[NUM_THREADS] = { "Pipe rear", "Compute"};

    void* (*thrd_functions[])(void*) = {pipe_rear_thread, compute_thread};

    pthread_t threads[NUM_THREADS];

    void* thrd_data[NUM_THREADS] = {};
    thrd_data[PIPE_REAR_THRD] = &pipe_in;
    thrd_data[COMPUTE_THRD] = &pipe_out;

    for (int i = 0; i < NUM_THREADS; ++i){
        int r = pthread_create(&threads[i], NULL, thrd_functions[i], thrd_data[i]);
        fprintf(stderr, "DEBUG: Create thread '%s' %s\r\n", thrd_names[i], (r == 0 ? "OK" : "FAIL"));
    }
    int *ex;
    for (int i = 0; i < NUM_THREADS; ++i){
        fprintf(stderr, "DEBUG: Call join to the thread %s\r\n", thrd_names[i]);
        int r = pthread_join(threads[i], (void*)&ex);
        fprintf(stderr, "DEBUG: Joining the thread %s has been %s\r\n", thrd_names[i], (r == 0 ? "OK" : "FAIL"));
    }

    io_close(pipe_in);
    io_close(pipe_out);

    return ret;
}

void* pipe_rear_thread(void* d)
{
    my_assert(d != NULL, __func__, __LINE__, __FILE__);
    int pipe_in = *(int*)d;
    bool end = false;

    uint8_t msg_buf[sizeof(message)];
    int i = 0;
    int len = 0;

    unsigned char c;

    while (io_getc_timeout(pipe_in, IO_READ_TIMEOUT_MS, &c) > 0) {}; // discard garbage

    while (!end){
        int r = io_getc_timeout(pipe_in, IO_READ_TIMEOUT_MS, &c);
        if (r > 0){ // char has been read
            if (i == 0){
                len = 0;
                if (get_message_size(c, &len)){
                    msg_buf[i++] = c;
                } else {
                    fprintf(stderr, "ERROR: Unknown message type %d\n", c); 
                }
            } else { // read remaining bytes of the message
                msg_buf[i++] = c;
            }
            if (len > 0 && i == len){
                message *msg = my_malloc(sizeof(message));
                if (parse_message_buf(msg_buf, len, msg)){
                    event ev = { .type = EV_PIPE_IN_MESSAGE};
                    ev.data.msg = msg;
                    queue_push(ev);
                } else {
                    fprintf(stderr, "ERROR: cannot parse message type %d\n", msg_buf[0]);
                    free(msg);
                }
                i = len = 0;
            }
        } 
        else if (r == 0) { } //timeout 
        else { 
            fprintf(stderr, "ERROR: reading from pipe\n");
            set_quit();
            event ev = { .type = EV_QUIT};
            queue_push(ev);
        }
        end = is_quit();
    } 

    return NULL;
}
