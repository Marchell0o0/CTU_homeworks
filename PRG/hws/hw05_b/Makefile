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
		# valgrind --leak-check=full --log-file=valgrind.out ./test < $$in_file > $$out_file 2> $$err_file ; \
		# grep -q "no leaks are possible" valgrind.out && \
		./test < $$in_file > $$out_file 2> $$err_file ; \
		diff -q $$out_file files/$$(basename $${in_file%.in}).out && \
		diff -q $$err_file files/$$(basename $${in_file%.in}).err ; \
	done

clear:
	rm -f test files/* my_files/*  valgrind.out

