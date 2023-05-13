# CC:=ccache $(CC)
CFLAGS+= -Wall -Werror -std=gnu99 -g -I.
LDFLAGS=-pthread

BINARIES= front_end/prgsem back_end/prgsem-comp_module

CFLAGS+=$(shell sdl2-config --cflags)
LDFLAGS+=$(shell sdl2-config --libs) -lSDL2_image

COMMON_OBJS = $(patsubst %.c,%.o,$(wildcard *.c))
FRONT_END_OBJS = $(patsubst %.c,%.o,$(wildcard front_end/*.c)) $(COMMON_OBJS)
BACK_END_OBJS = $(patsubst %.c,%.o,$(wildcard back_end/*.c)) $(COMMON_OBJS)

all: $(BINARIES)

front_end/prgsem: $(FRONT_END_OBJS)
	$(CC) $(FRONT_END_OBJS) $(LDFLAGS) -o $@

back_end/prgsem-comp_module: $(BACK_END_OBJS)
	$(CC) $(BACK_END_OBJS) $(LDFLAGS) -o $@

%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

clean:
	rm -f $(BINARIES) *.o front_end/*.o back_end/*.o


# BINARIES=prgsem prgsem-comp_module

# CFLAGS+=$(shell sdl2-config --cflags)
# LDFLAGS+=$(shell sdl2-config --libs) -lSDL2_image


# all: $(BINARIES)

# COMMON_OBJS= compute_control.o compute.o event_queue.o gui.o keyboard.o main.o messages.o prg_io_nonblock.o utils.o xwin_sdl.o

# prgsem_OBJS = prgsem.o $(COMMON_OBJS)
# prgsem-comp_module_OBJS = prgsem-comp_module.o $(COMMON_OBJS)


# prgsem: $(prgsem_OBJS)
# 	$(CC) $(prgsem_OBJS) $(LDFLAGS) -o $@

# prgsem-comp_module: $(prgsem-comp_module_OBJS)
# 	$(CC) $(prgsem-comp_module_OBJS) $(LDFLAGS) -o $@

# %.o: %.c
# 	$(CC) -c $(CFLAGS) $< -o $@

# clean:
# 	rm -f $(BINARIES) *.o


# OBJS=$(patsubst %.c,%.o,$(wildcard *.c))

# prgsem: $(OBJS)
# 	$(CC) $(OBJS) $(LDFLAGS) -o $@

# $(OBJS): %.o: %.c
# 	$(CC) -c $(CFLAGS) $< -o $@

# clean:
# 	rm -f $(BINARIES) $(OBJS)

