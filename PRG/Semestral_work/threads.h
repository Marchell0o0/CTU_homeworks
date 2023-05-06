#ifndef __THREADS_H__
#define __THREADS_H__

void init_threads(const char *input_pipe, const char *output_pipe, int *fd_in, int *fd_out);
void cleanup_threads(void);

#endif