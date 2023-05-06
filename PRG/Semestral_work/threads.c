#include <fcntl.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <unistd.h>
#include "threads.h"

static int fd_in;
static int fd_out;
static const char *g_input_pipe;
static const char *g_output_pipe;

void init_threads(const char *input_pipe, const char *output_pipe, int *p_fd_in, int *p_fd_out) {
    g_input_pipe = input_pipe;
    g_output_pipe = output_pipe;

    // Open input pipe
    *p_fd_in = open(input_pipe, O_RDONLY | O_NONBLOCK);
    if (*p_fd_in < 0) {
        perror("Error opening input pipe");
        unlink(input_pipe);
        unlink(output_pipe);
        exit(EXIT_FAILURE);
    }
    fd_in = *p_fd_in;

    // Open output pipe
    *p_fd_out = open(output_pipe, O_WRONLY);
    if (*p_fd_out < 0) {
        perror("Error opening output pipe");
        close(fd_in);
        unlink(input_pipe);
        unlink(output_pipe);
        exit(EXIT_FAILURE);
    }
    fd_out = *p_fd_out;
}

void cleanup_threads(void) {
    // Close input and output pipes
    close(fd_in);
    close(fd_out);

    // Remove the input and output pipe files
    unlink(g_input_pipe);
    unlink(g_output_pipe);
}