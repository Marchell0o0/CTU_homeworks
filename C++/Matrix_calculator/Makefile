TARGET = main
TEST_DIR = testing_files
TEST_MODE = opt

CC = g++
CFLAGS = -pedantic -Wall -Werror  -g

DATA_DIR = $(TEST_DIR)/data_o/$(TEST_MODE)
# DATA_DIR = $(TEST_DIR)/data_b
MY_OUTPUTS_DIR = $(TEST_DIR)/my_outputs
DIFFS_DIR = $(TEST_DIR)/diffs

.PHONY: all  test_data clean

all: $(TARGET)

$(TARGET): $(TARGET).cpp
	$(CC) $(CFLAGS) -o $@ $<

test_data: $(TARGET) 
	mkdir -p $(MY_OUTPUTS_DIR)
	mkdir -p $(DIFFS_DIR)
	
	for input in $(DATA_DIR)/*.in; do \
		filename=$$(basename "$$input" .in); \
		./$(TARGET) < "$$input" \
		> "$(MY_OUTPUTS_DIR)/$$filename.out" 2> "$(MY_OUTPUTS_DIR)/$$filename.err"; \
		if ! diff -u "$(DATA_DIR)/$$filename.out" \
		 "$(MY_OUTPUTS_DIR)/$$filename.out" > "$(DIFFS_DIR)/$$filename.out.diff"; then \
			echo "Differences found in $$filename.out"; \
		else \
			rm "$(DIFFS_DIR)/$$filename.out.diff"; \
		fi; \
		if ! diff -u "$(DATA_DIR)/$$filename.err" \
		"$(MY_OUTPUTS_DIR)/$$filename.err" > "$(DIFFS_DIR)/$$filename.err.diff"; then \
			echo "Differences found in $$filename.err"; \
		else \
			rm "$(DIFFS_DIR)/$$filename.err.diff"; \
		fi; \
	done

clean:
	rm -rf $(TARGET) $(DIFFS_DIR) $(MY_OUTPUTS_DIR)