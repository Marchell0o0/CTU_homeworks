#include <stdio.h>
#include <unistd.h>
#include <pthread.h>
#include "messages.h"
#include "threads.h"
#include "prg_io_nonblock.h"

#define INPUT_PIPE "/tmp/computational_module.in"
#define OUTPUT_PIPE "/tmp/computational_module.out"

int fd_out;

int main() {
    int fd_in;
    init_threads(INPUT_PIPE, OUTPUT_PIPE, &fd_in, &fd_out);

    // Set the terminal to non-blocking mode
    set_nonblock(STDIN_FILENO);

    printf("Press 'q' to quit, 'g' to get version\n");

    char input;
    message msg;
    while (1) {
        input = getchar();
        if (input != -1) {
            switch (input) {
                case 'q':
                    msg.type = MSG_QUIT;
                    write(fd_out, &msg, sizeof(msg));
                    break;
                case 'g':
                    msg.type = MSG_GET_VERSION;
                    write(fd_out, &msg, sizeof(msg));
                    break;
                default:
                    printf("Unknown command\n");
                    break;
            }

            if (input == 'q') {
                break;
            }
        }
        usleep(100000); // sleep for 100 ms to avoid high CPU usage
    }

    // Cleanup and exit
    cleanup_threads();
    return 0;
}
