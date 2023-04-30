CC = clang
CFLAGS = -Wall -Werror -std=c99 -g
PROGRAM = hw07-test
TESTER = b3b36prg-hw07-test
DATA = data/man
MY_FILES = my_files
FILES = files
INPUTS = $(wildcard $(DATA)/*.txt)
MY_OUTPUTS = $(patsubst $(DATA)/%.txt,$(MY_FILES)/%.out,$(INPUTS))
TESTER_OUTPUTS = $(patsubst $(DATA)/%.txt,$(FILES)/%.out,$(INPUTS))

all: $(PROGRAM)

$(PROGRAM): hw07-test.c
	$(CC) $(CFLAGS) -o $@ $<

my_outputs: $(PROGRAM)
	@mkdir -p $(MY_FILES)
	@for input in $(INPUTS); do \
		output=$(MY_FILES)/$$(basename $$input .txt).out; \
		echo "Running $(PROGRAM) on $$input"; \
		./$(PROGRAM) <$$input > $$output; \
	done

tester_outputs: $(TESTER)
	@mkdir -p $(FILES)
	@for input in $(INPUTS); do \
		output=$(FILES)/$$(basename $$input .txt).out; \
		echo "Running $(TESTER) on $$input"; \
		./$(TESTER) <$$input > $$output; \
	done

compare: my_outputs tester_outputs
	@for my_file in $(MY_OUTPUTS); do \
		tester_file=$(FILES)/$$(basename $$my_file); \
		echo "Comparing $$my_file and $$tester_file"; \
		diff -q $$my_file $$tester_file || echo "Difference found in $$(basename $$my_file)"; \
	done

valgrind_check: $(PROGRAM) $(INPUTS)
	@for input in $(INPUTS); do \
		echo "Valgrind check for $$input"; \
		valgrind --tool=memcheck --leak-check=full --quiet --error-exitcode=1 --read-var-info=no ./$(PROGRAM) < $$input 2>&1 > /dev/null | \
		grep -v "unhandled" | \
		grep -v "get_Form_contents" || \
		echo "Valgrind error for $$input"; \
	done

.PHONY: all my_outputs tester_outputs compare valgrind_check clean

clean:
	rm -f $(PROGRAM)
	rm -rf $(MY_FILES) $(FILES)
