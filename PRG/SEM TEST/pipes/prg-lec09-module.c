/*
 * Filename: prg-lec09-module.c
 * Date:     2019/12/25 21:37
 * Author:   Jan Faigl
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include <unistd.h>  // for usleep

#ifndef SLEEP_MS
#define SLEEP_MS 10
#endif 

#include "messages.h"
#include "messages.c"
#include "prg_io_nonblock.h"

typedef struct {
   bool quit;
   // int fd; // file descriptor
   int fdOut, fdIn; // file descriptor
   int period;
   bool enabled;
} data_t;

void draw_computing(void);

/// - main ---------------------------------------------------------------------
int main(int argc, char *argv[])
{
   data_t data = { .quit = false, .fdOut = -1, .fdIn = -1, .enabled = false, .period = SLEEP_MS };
   int tiks = 0;
   unsigned char c;
   const char *out = argc > 1 ? argv[1] : "/tmp/computational_module.out";
   const char *in = argc > 1 ? argv[1] : "/tmp/computational_module.in";

   data.fdOut = io_open_read(out);
   if (data.fdOut == -1) {
      fprintf(stderr, "Cannot open named pipe port %s\n", out);
      exit(100);
   }
   data.fdIn = io_open_write(in);
   if (data.fdIn == -1) {
      fprintf(stderr, "Cannot open named pipe port %s\n", in);
      exit(100);
   }
   //--------------------------how to send one message--------------------
   // it sends 1 + 9 + 1 = 11 bytes
   message msg = { .data.startup.message = {'B', 'O', 'R', 'Y', 'S', 'O', 'L', 'E'}};
   // syncronize for good flow in pipe (dont get why)
   fsync(data.fdIn);
   if (io_putc(data.fdIn, MSG_STARTUP)  != 1) {
      fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
      data.quit = true;
   }
   int csum = MSG_STARTUP;
   for (int i = 0; i < STARTUP_MSG_LEN; ++i) {
      fsync(data.fdIn);
      if (io_putc(data.fdIn, msg.data.startup.message[i])  != 1) {
         fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
         data.quit = true;
      }
      csum += msg.data.startup.message[i];
   }
   csum = 255 - csum;
   fsync(data.fdIn);
   if (io_putc(data.fdIn, csum)  != 1) {
      fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
      data.quit = true;
   }
   //---------------------------------------------------------------------
   int periods_ms[] = { 50, 100, 200, 500, 1000 };

   while(!data.quit) {
      message msg1;             
      int r = io_getc_timeout(data.fdOut, 0, &c);
      if (r == 1) {
	 switch(c) {
	    case 's':
	       data.enabled = false;
	       fprintf(stdout, "stop-s\n");
	       break;
	    case 'e':
	       data.enabled = false;
	       fprintf(stdout, "stop-e\n");
	       break;
	    case 'h':
	       fprintf(stdout, "hello\n");
	       break;
	    case 'b':
	       fprintf(stdout, "bye\n");
	       data.quit = true;
	       break;
     case 'g':
   // Create a new message with type MSG_VERSION
    printf("received g\n");
   msg1.type = MSG_VERSION;
   msg1.data.version.major = 1; // Major version number
   msg1.data.version.minor = 0; // Minor version number
   msg1.data.version.patch = 0; // Patch version number


   // Calculate checksum for the version message
   csum = MSG_VERSION + msg1.data.version.major + msg1.data.version.minor + msg1.data.version.patch;
   csum = 255 - csum;

   // Send the message type to the main file
   fsync(data.fdIn);
   if (io_putc(data.fdIn, MSG_VERSION)  != 1) {
      fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
      data.quit = true;
   }

   // Send the message data to the main file
   fsync(data.fdIn);
   if (io_putc(data.fdIn, msg1.data.version.major)  != 1 ||
       io_putc(data.fdIn, msg1.data.version.minor)  != 1 ||
       io_putc(data.fdIn, msg1.data.version.patch)  != 1) {
      fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
      data.quit = true;
   }

   // Send the message checksum to the main file
   fsync(data.fdIn);
   if (io_putc(data.fdIn, csum)  != 1) {
      fprintf(stderr, "ERROR: CANNOT SEND COMMAND TO MODLULE\n");
      data.quit = true;
   }
   break;

	    default:
	       if (c >= '1' && c <= '5') { // (re)attach 
		  data.period = periods_ms[ c - '1' ]; 
		  data.enabled = true;
	       }
	       break;
	 } //end switch
      } // end char read
      usleep(SLEEP_MS * 1000); // smallest period
      tiks += SLEEP_MS;
      if (tiks >= data.period) {
	 tiks = 0;
	 if (data.enabled) {
	    draw_computing();
	 }
      }
   } // end while(!data.quit)
   fprintf(stderr, "quit\n");
   io_close(data.fdOut);
   io_close(data.fdIn);
   return EXIT_SUCCESS;
}

// - function -----------------------------------------------------------------
void draw_computing(void)
{
   static char a[] = { '|', '/', '-', '\\', };
   static unsigned char i = 0;
   fprintf(stdout, "\r%c", a[i++]);
   fflush(stdout);
   i %= 4;
}

/* end of prg-lec09-module.c */
