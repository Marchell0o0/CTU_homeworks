/*
 * Filename: prg-lec09-main.c
 * Date:     2019/12/25 21:38
 * Author:   Jan Faigl
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
 
#include <termios.h> 
#include <unistd.h>  // for STDIN_FILENO

#include "messages.h" 
#include "messages.c" 
#include "prg_io_nonblock.h"
 
typedef struct {
   bool quit;
   int fdIn, fdOut; // file descriptor
} data_t;
 
void call_termios(int reset);

/// - main ---------------------------------------------------------------------
int main(int argc, char *argv[])
{
   data_t data = { .quit = false, .fdIn = -1, .fdOut = -1 };
   int c;
   const char *out = argc > 1 ? argv[1] : "/tmp/computational_module.out";
   const char *in = argc > 1 ? argv[1] : "/tmp/computational_module.in";

   data.fdOut = io_open_write(out);
   if (data.fdOut == -1) {
      fprintf(stderr, "Cannot open named pipe port %s\n", out);
      exit(100);
   }
   data.fdIn = io_open_read(in);
   if (data.fdIn == -1) {
      fprintf(stderr, "Cannot open named pipe port %s\n", in);
      exit(100);
   }
   //--------------------------how to read one message (11 bytes)--------------------
   uint8_t buf[sizeof(message)];
   int buf_len = 0;
   int idx = 0;
   unsigned char cc;
   while(!data.quit) {
      int r = io_getc_timeout(data.fdIn, 0, &cc);
      if (r == 1) {
         if (idx == 0)
            if (get_message_size(cc, &buf_len)) {
               buf[idx++] = cc;
            } else {} //handle an error (maybe)
         else
            buf[idx++] = cc;
         // printf("Tisk: %c\n", cc);
      } else if (r == 0) { //timeout
      } else {} // handle error
      if (buf_len > 0 && idx == buf_len) {
         message *msg = malloc(sizeof(message));
         if (parse_message_buf(buf, buf_len, msg)) {
            switch (msg->type) {
            case MSG_STARTUP:
               printf("Received message: ");
               for (int i = 0; i < STARTUP_MSG_LEN; i++) {
                  printf("%c", msg->data.startup.message[i]);
               }
               printf("\n");
               break;
            case MSG_VERSION:
               printf("MSG_VERSION WAS ACCEPTED...\n");
               printf("INFO: Module firmware ver. %d.%d-p%d\n",
                msg->data.version.major,
                 msg->data.version.minor,
                  msg->data.version.patch);
            default:
               break;
            }
         }
         idx = 0; // Reset the index to read the next message
      }
      break; // to test quit
   }
   //---------------------------------------------------------------------
   call_termios(0); 

   while (!data.quit && (c = getchar()) != EOF) {
      switch(c) {
	 case 's':
	 case 'e':
	 case '1':
	 case '2':
	 case '3':
	 case '4':
	 case '5':
	 case 'b':
	 case 'h':
	    if (io_putc(data.fdOut, c) != 1) {
	       fprintf(stderr, "ERROR: Cannot send command to module, exit program\n");
	       data.quit = true;
	    }
	    fsync(data.fdOut);
	    fprintf(stderr, "Send command '%c'\n", c);
	    break;
	 case 'q':
	    fprintf(stderr, "quit\n");
	    fprintf(stdout, "quit\n");
	    data.quit = true;
	    break;
    case 'g':
    // MSG_GET_VERSION
       if (io_putc(data.fdOut, c) != 1) {
          fprintf(stderr, "ERROR: Cannot send command to module, exit program\n");
          data.quit = true;
       }
       fsync(data.fdOut);
       fprintf(stderr, "Send command '%c'\n", c);
       break;
	 default: // discard all other keys
	    break;
      } //end switch
   } // end 
   fprintf(stderr, "quit\n");
   io_close(data.fdOut);
   io_close(data.fdIn);
   call_termios(1); // restore terminal settings
   return EXIT_SUCCESS;
}

// - function -----------------------------------------------------------------
void call_termios(int reset)
{
   static struct termios tio, tioOld;
   tcgetattr(STDIN_FILENO, &tio);
   if (reset) {
      tcsetattr(STDIN_FILENO, TCSANOW, &tioOld);
   } else {
      tioOld = tio; //backup 
      cfmakeraw(&tio);
      tio.c_oflag |= OPOST;
      tcsetattr(STDIN_FILENO, TCSANOW, &tio);
   }
}

/* end of prg-lec09-main.c */
