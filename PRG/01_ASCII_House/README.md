# ASCII House

This program reads input to create an ASCII representation of a house with an optional fence.

## Usage

### Input format

The input consists of two or three integers:

1. Width (W) of the house (must be an odd integer between 3 and 69).
2. Height (H) of the house (must be an integer between 3 and 69).
3. (Optional) Size of the fence (F) (must be a positive integer smaller than H).

If the height and width are equal, the program will expect a third integer for the size of the fence.

### Example

Input:
7 7 3

Output:
```
   X
  X X
 X   X
XXXXXXX
Xo*o*oX
X*o*o*X
Xo*o*oX
X*o*o*X|-|
Xo*o*oX| |
XXXXXXX|-|
```

Input:
9 4

Output:
```

    X
   X X
  X   X
 X     X
XXXXXXXXX
X       X
X       X
XXXXXXXXX
```


## Testing

1. Create a directory for the homework.
2. Place your testing files provided by the courseware into some folder (in the Makefile by default: `testing_files`).
3. Commands for Makefile:
   - `all` - compile main.c
   - `test_random` - test with random input from `generate_solutions.sh`
   - `test_data` - test with input from the premade data folder
   - `valgrind_data`, `valgrind_random` - check for errors and leaks with Valgrind for two different input data
   - `zip` - make a zip with the `main.c` file.
