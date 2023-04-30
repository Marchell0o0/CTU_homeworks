#include <stdio.h>

#define ERROR_INPUT 100
#define ERROR_RANGE 101


int main() {
    int n;
    printf("Enter a number of lines in range 1 to 10: ");
    int r = scanf("%d", &n);
    if (r != 1){
        fprintf(stderr, "ERROR: Cannot read integer value from the standard input\n");
        return ERROR_INPUT;
    }
    else if (n < 1 || n > 10){
        fprintf(stderr, "ERROR: Given value %d is not within range [1, 10]\n", n);
        return ERROR_RANGE;
    }
    putchar('\n');
    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n - i; ++j){
            putchar('*');
        }
        putchar('\n');
    }
    return 0;
}

