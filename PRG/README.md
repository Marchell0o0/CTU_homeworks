# There is a readme file in every project folder!

# Testing

1. Create a directory for the homework.
2. Place your testing files provided by the courseware into some folder (in the Makefile by default: `testing_files`).
4. Download the Makefile from the folder of the homework you want to test! Or change the first variables for it to work with your setup.
3. Commands for Makefile:
   - `all` - compile main.c
   - `test_random` - test with random input from `generate_solutions.sh`
   - `test_data` - test with input from the premade data folder
   - `valgrind_data`, `valgrind_random` - check for errors and leaks with Valgrind for two different input data
   - `zip` - make a zip with the `main.c` file.

