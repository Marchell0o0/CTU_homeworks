# ASCII House

This program reads input to create an ASCII representation of a house with an optional fence.

## Usage

### Input format

The input consists of two or three integers:

1. Width (W) of the house (must be an odd integer between 3 and 69).
2. Height (H) of the house (must be an integer between 3 and 69).
3. (Optional) Size of the fence (F) (must be a positive integer smaller than H).

If the height and width are equal, the program will expect a third integer for the size of the fence.

### Example output

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


