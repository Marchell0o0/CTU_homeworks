#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

#include "keyboard.h"

#include "event_queue.h"
#include "utils.h"
#include "compute_control.h"


void* keyboard_thread(void* d)
{
    call_termios(0);
    int c;
    event ev;

    while ((c = getchar()) != 'q'){
        ev.type = EV_TYPE_NUM;
        switch(c){
            case 'g':
                ev.type = EV_GET_VERSION;
                info("Requesting version");
                break;
            case 'a':
                if (is_computing())
                { 
                    ev.type = EV_ABORT;
                    info("Aborting computation"); 
                } else { 
                    warn("Abort requested but it is not computing"); 
                }
                break;
            case 's':
                if (!is_computing()) 
                { 
                    ev.type = EV_SET_COMPUTE;
                } else {
                    warn("New computation parameters requested but it is discarded due to on ongoing computation"); 
                }
                break;
            case 'c':
                if (!is_computing()) 
                { 
                    ev.type = EV_COMPUTE; 
                } else { 
                    warn("New computation requested but it is discarded due on ongoing computation"); 
                }
                break;
            case 'b':
                if (!is_computing()) 
                { 
                    ev.type = EV_COMPUTE_BURST; 
                } else { 
                    warn("New computation requested but it is discarded due on ongoing computation"); 
                }
                break;
            default:
                break;
        }
        if (ev.type != EV_TYPE_NUM){
            queue_push(ev);
        }
    }
    // set_quit();
    ev.type = EV_QUIT;
    queue_push(ev);


    call_termios(1);
    return NULL;
}
