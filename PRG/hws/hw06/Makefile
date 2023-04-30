# CFLAGS+=  -pedantic -Wall -std=c99 -O3
# HW=hw06-b3b36prg
# ZIP=zip

# all: $(HW) lib

# $(HW): main.c queue.o
# 	$(CC) $(CFLAGS) main.c queue.o -o $(HW)

# queue.o: queue.c queue.h
# 	$(CC) $(CFLAGS) -c queue.c -o queue.o

# libqueue.so: queue.c queue.h
# 	$(CC) $(CFLAGS) -fPIC -shared queue.c -o libqueue.so
# 	$(STRIP) $(lib)

# lib: libqueue.so

# zip:
# 	$(ZIP) $(HW)-brute.zip queue.h queue.c

# clean:
# 	$(RM) *.o
# 	$(RM) $(HW) libqueue.so
# 	$(RM) $(HW)-brute.zip

# .PHONY: clean zip valgrind --leak-check=full --log-file=valgrind.out grep -q "no leaks are possible" valgrind.out && \

CC = clang
CFLAGS = -pedantic -Wall -std=c99 -O3
SRC = main.c
EXEC = test

.PHONY: clear test

test:
	$(CC) $(CFLAGS) main.c -o test
	sh generate_solutions.sh
	for in_file in files/*.in ; do\
		out_file=my_files/$$(basename $${in_file%.in}).out ; \
		err_file=my_files/$$(basename $${in_file%.in}).err ; \
		./test < $$in_file > $$out_file 2> $$err_file ; \
		diff -q $$out_file files/$$(basename $${in_file%.in}).out && \
		diff -q $$err_file files/$$(basename $${in_file%.in}).err ; \
	done

clear:
	rm -f test  files/* my_files/* valgrind.out

