# CFLAGS+= -Wall -Werror -std=gnu99 -g
# LDFLAGS=-pthread

# HW=prgsem
# BINARIES=prgsem-main

# CFLAGS+=$(shell sdl2-config --cflags)
# LDFLAGS+=$(shell sdl2-config --libs) -lSDL2_image


# all: $(BINARIES)

# OBJS=$(patsubst %.c,%.o,$(wildcard *.c))

# prgsem-main: $(OBJS)
# 	$(CC) $(OBJS) $(LDFLAGS) -o $@

# $(OBJS): %.o: %.c
# 	$(CC) -c $(CFLAGS) $< -o $@

# clean:
# 	rm -f $(BINARIES) $(OBJS)


CFLAGS+= -Wall -Werror -std=gnu99 -g
LDFLAGS=-pthread

# Set the names of the binary files to be generated
BINARIES=prgsem-main prgsem-comp_module

# Include flags for SDL2
CFLAGS+=$(shell sdl2-config --cflags)
LDFLAGS+=$(shell sdl2-config --libs) -lSDL2_image

# Default target: build all binaries
all: $(BINARIES)

# Rule for building prgsem-main: list its object file dependencies
prgsem-main: prgsem-main.o threads.o prg_io_nonblock.o xwin_sdl.o
	# Link the object files using the linker flags, and output the binary named prgsem-main
	$(CC) $^ $(LDFLAGS) -o $@

# Rule for building prgsem-comp_module: list its object file dependencies
prgsem-comp_module: prgsem-comp_module.o threads.o prg_io_nonblock.o
	# Link the object files using the linker flags, and output the binary named prgsem-comp_module
	$(CC) $^ $(LDFLAGS) -o $@

# General rule for compiling .c files into .o files
# Compile the .c file using the compiler flags, and output the corresponding .o file
%.o: %.c
	$(CC) -c $(CFLAGS) $< -o $@

# Rule for cleaning up the generated files
clean:
	# Remove the binary files and all .o files
	rm -f $(BINARIES) *.o
