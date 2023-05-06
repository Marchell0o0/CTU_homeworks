// comp_module.c
#include <stdio.h>
#include <unistd.h>
#include "messages.h"
#include "threads.h"

#define INPUT_PIPE "/tmp/computational_module.out"
#define OUTPUT_PIPE "/tmp/computational_module.in"

const uint8_t VERSION_MAJOR = 1;
const uint8_t VERSION_MINOR = 0;
const uint8_t VERSION_PATCH = 0;

int fd_in;

int main() {
    int fd_out;
    init_threads(INPUT_PIPE, OUTPUT_PIPE, &fd_in, &fd_out);
    message msg;
    while (1) {
        if (read(fd_in, &msg, sizeof(msg)) > 0) {
            switch (msg.type) {
                case MSG_QUIT:
                    printf("Received quit message, exiting...\n");
                    cleanup_threads();
                    return 0;
                case MSG_GET_VERSION:
                    printf("Received get version message, sending version...\n");
                    message version_msg;
                    version_msg.type = MSG_VERSION;
                    version_msg.data.version.major = VERSION_MAJOR;
                    version_msg.data.version.minor = VERSION_MINOR;
                    version_msg.data.version.patch = VERSION_PATCH;
                    write(fd_out, &version_msg, sizeof(version_msg));
                    break;
                default:
                    printf("Unknown message type: %d\n", msg.type);
                    break;
            }
        }
        usleep(100000); // sleep for 100 ms to avoid high CPU usage
    }

    // Cleanup and exit
    cleanup_threads();
    return 0;
}
