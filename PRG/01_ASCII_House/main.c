#include <stdio.h>
#include <stdlib.h>

#define ERROR_INPUT 100
#define ERROR_RANGE 101
#define ERROR_EVEN_WIDTH 102
#define ERROR_FENCE_SIZE 103
#define MIN_VALUE 3
#define MAX_VALUE 69
#define WALL "X"
#define EMPTY_SPACE " "
#define FENCE_PART "|"
#define FENCE_BORDER "-"
#define HOUSE_INSIDE_1 "*"
#define HOUSE_INSIDE_2 "o"

#define MAX(X, Y) ((X) > (Y) ? (X) : (Y))

int read_input(int *widht, int *height, int *fence_size);

void print_error(int ret);

// print a straight line of symbols
void straight_line(int length, char symbol[]);

// print a triangle of walls
void roof(int width);

// print a square of walls with empty space inside
void box(int width, int height);

// print a square of walls with house_inside 1 and 2 inside and a fence to the
// right
void box_with_fence(int width, int height, int fence_size);

/* The main program */

int main(int argc, char *argv[]) {
    int width = 0;
    int height = 0;
    int fence_size = 0;

    int return_code = read_input(&width, &height, &fence_size);

    if (return_code != EXIT_SUCCESS)
        print_error(return_code);
    else {
        roof(width);
        if (fence_size == 0)
            box(width, height);
        else
            box_with_fence(width, height, fence_size);
    }
    return return_code;
}

void straight_line(int length, char symbol[]) {
    for (int i = 0; i < length; ++i) {
        printf("%s", symbol);
    }
}

void roof(int width) {
    for (int i = 0; i < width / 2; ++i) {
        straight_line(width / 2 - i, EMPTY_SPACE);
        if (i != 0) {
            printf(WALL);
            straight_line((i * 2) - 1, EMPTY_SPACE);
        }
        printf(WALL "\n");
    }
}

void box(int width, int height) {
    for (int i = 0; i < height; ++i) {
        printf(WALL);

        if (i == 0 || i == height - 1)
            straight_line(width - 2, WALL);

        else
            straight_line(width - 2, EMPTY_SPACE);

        printf(WALL "\n");
    }
}

void box_with_fence(int width, int height, int fence_size) {
    for (int i = 0; i < height; ++i) {
        if (i == 0 || i == height - 1)
            straight_line(width, WALL);

        else {
            printf(WALL);
            if (i % 2 == 1) {
                straight_line((width / 2) - 1, HOUSE_INSIDE_2 HOUSE_INSIDE_1);
                printf(HOUSE_INSIDE_2);
            } else {
                straight_line((width / 2) - 1, HOUSE_INSIDE_1 HOUSE_INSIDE_2);
                printf(HOUSE_INSIDE_1);
            }
            printf(WALL);
        }

        if (i == (height - fence_size) || i == height - 1) {
            if (fence_size % 2 == 1) printf(FENCE_PART);
            straight_line(fence_size / 2, FENCE_BORDER FENCE_PART);
        }

        else if (i > (height - fence_size)) {
            if (fence_size % 2 == 1) printf(FENCE_PART);
            straight_line(fence_size / 2, EMPTY_SPACE FENCE_PART);
        }
        printf("\n");
    }
}

int read_input(int *width, int *height, int *fence_size) {
    int correct_inputs = scanf("%d %d", width, height);

    // check errors for input
    if (correct_inputs != 2)
        return ERROR_INPUT;
    else if ((*width < MIN_VALUE || *width > MAX_VALUE) ||
             (*height < MIN_VALUE || *height > MAX_VALUE))
        return ERROR_RANGE;
    else if (*width % 2 != 1)
        return ERROR_EVEN_WIDTH;

    // read and check errors for fence value
    if (*height == *width) {
        correct_inputs += scanf("%d", fence_size);
        if (correct_inputs != 3) return ERROR_INPUT;
        if (*fence_size <= 0 || *fence_size >= *height) return ERROR_FENCE_SIZE;
    }
    return EXIT_SUCCESS;
}

void print_error(int return_code) {
    switch (return_code) {
        case ERROR_INPUT:
            fprintf(stderr, "Error: Chybny vstup!\n");
            break;
        case ERROR_RANGE:
            fprintf(stderr, "Error: Vstup mimo interval!\n");
            break;
        case ERROR_EVEN_WIDTH:
            fprintf(stderr, "Error: Sirka neni liche cislo!\n");
            break;
        case ERROR_FENCE_SIZE:
            fprintf(stderr, "Error: Neplatna velikost plotu!\n");
            break;
    }
}
