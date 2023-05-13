#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define INITIAL_CAPACITY 10
#define FIRST_MATRIX_CAPACITY 100
#define SECOND_MATRIX_CAPACITY 400
#define THIRD_MATRIX_CAPACITY 1700
#define NUM_LETTERS 26

enum ErrorCode
{
    ERROR_INPUT = 100,
    ERROR_OUT_OF_MEMORY = 101,
};

struct Matrix
{
    int **data;
    int rows;
    int cols;
    int too_big;
};

struct MatrixArray
{
    struct Matrix *equation;
    struct Matrix *matrices;
    char *operations;
    int size;
    int capacity;
    int max_rows;
    int max_cols;
    enum ErrorCode error_code;
};

// input and miscellaneous
void print_error(int return_code);
void print_matrix(struct Matrix matrix);
void check_input_errors(struct MatrixArray *matrix_array);
void getline(char **lineptr, size_t *n, FILE *stream);
char *strtok_r(char *str, const char *delim, char **saveptr);

void copy_matrix(struct Matrix dist, int **src);

// creation of the main array of equation
struct MatrixArray read_equation(void);

// main computation
void multiply(struct MatrixArray matrix_array, int first_multiplier, struct Matrix *answer, int c2);
void matrix_add_sub(struct Matrix matrix1, int **matrix2, char opp);

int find_end_of_mult_sequence(struct MatrixArray matrix_array, int start_index);

// memory handling
void free_matrix(struct Matrix matrix);
void free_matrix_array(struct MatrixArray matrix_array);

/* The main program */
int main(int argc, char *argv[])
{
    struct MatrixArray matrix_array = read_equation();

    // if (matrix_array.error_code != EXIT_SUCCESS)
    // {
    //     print_error(matrix_array.error_code);
    //     free_matrix_array(matrix_array);
    //     return matrix_array.error_code;
    // }

    check_input_errors(&matrix_array);
    if (matrix_array.error_code != EXIT_SUCCESS)
    {
        print_error(matrix_array.error_code);
        free_matrix_array(matrix_array);
        return matrix_array.error_code;
    }

    int max_rows = matrix_array.max_rows;
    int max_cols = matrix_array.max_cols;

    int current_idx = 0;
    int end_of_mult_sequence = find_end_of_mult_sequence(matrix_array, current_idx);

    // create and allocate memory for main answer matrix
    struct Matrix answer;
    answer.rows = matrix_array.equation[end_of_mult_sequence].rows;
    answer.cols = matrix_array.equation[end_of_mult_sequence].cols;

    answer.data = malloc(max_rows * sizeof(int *));
    if (!answer.data)
        matrix_array.error_code = ERROR_OUT_OF_MEMORY;

    for (int i = 0; i < max_rows; i++)
    {
        answer.data[i] = malloc(max_cols * sizeof(int));
        if (!answer.data[i])
            matrix_array.error_code = ERROR_OUT_OF_MEMORY;
    }

    int temp_idx;

    copy_matrix(answer, matrix_array.equation[end_of_mult_sequence].data);
    if (end_of_mult_sequence != 0)
    {
        temp_idx = end_of_mult_sequence;
        while (temp_idx != current_idx)
        {
            temp_idx--;
            multiply(matrix_array, temp_idx, &answer, answer.cols);
        }
    }
    // move current index
    current_idx = end_of_mult_sequence;

    // if something else left
    if (current_idx != matrix_array.size)
    {
        struct Matrix next_matrix;

        next_matrix.data = malloc(max_rows * sizeof(int *));
        if (!next_matrix.data)
            matrix_array.error_code = ERROR_OUT_OF_MEMORY;

        for (int i = 0; i < max_rows; i++)
        {
            next_matrix.data[i] = malloc(max_cols * sizeof(int));
            if (!next_matrix.data[i])
                matrix_array.error_code = ERROR_OUT_OF_MEMORY;
        }

        char current_operation;
        while (current_idx < matrix_array.size)
        {
            current_idx++;
            end_of_mult_sequence = find_end_of_mult_sequence(matrix_array, current_idx);

            next_matrix.rows = matrix_array.equation[end_of_mult_sequence].rows;
            next_matrix.cols = matrix_array.equation[end_of_mult_sequence].cols;

            copy_matrix(next_matrix, matrix_array.equation[end_of_mult_sequence].data);
            temp_idx = end_of_mult_sequence;
            while (temp_idx != current_idx)
            {
                temp_idx--;
                multiply(matrix_array, temp_idx, &next_matrix, next_matrix.cols);
            }

            current_operation = matrix_array.operations[current_idx - 1];
            matrix_add_sub(answer, next_matrix.data, current_operation);

            current_idx = end_of_mult_sequence;
        }
        for (int i = 0; i < max_rows; i++)
            free(next_matrix.data[i]);
        free(next_matrix.data);
    }
    print_matrix(answer);

    for (int i = 0; i < max_rows; i++)
        free(answer.data[i]);
    free(answer.data);

    free_matrix_array(matrix_array);

    return EXIT_SUCCESS;
}

void matrix_add_sub(struct Matrix matrix1, int **matrix2, char opp)
{
    int mult;
    if (opp == '-')
        mult = -1;
    else
        mult = 1;

    for (int i = 0; i < matrix1.rows; i++)
    {
        for (int j = 0; j < matrix1.cols; j++)
            matrix1.data[i][j] += mult * matrix2[i][j];
    }
}

void multiply(struct MatrixArray matrix_array, int first_multiplier, struct Matrix *answer, int c2)
{
    int r1 = matrix_array.equation[first_multiplier].rows;
    int c1 = matrix_array.equation[first_multiplier].cols;

    int **temp_answer = (int **)malloc(sizeof(int *) * r1);
    for (int i = 0; i < r1; i++)
        temp_answer[i] = (int *)malloc(sizeof(int) * c2);

    for (int i = 0; i < r1; i++)
    {
        for (int j = 0; j < c2; j++)
        {
            temp_answer[i][j] = 0;
            for (int k = 0; k < c1; k++)
                temp_answer[i][j] += matrix_array.equation[first_multiplier].data[i][k] * answer->data[k][j];
        }
    }
    answer->rows = r1;
    copy_matrix(*answer, temp_answer);
    for (int i = 0; i < r1; i++)
        free(temp_answer[i]);
    free(temp_answer);
}

int find_end_of_mult_sequence(struct MatrixArray matrix_array, int start_index)
{
    int end_idx = start_index;
    while (end_idx < matrix_array.size && matrix_array.operations[end_idx] == '*')
    {
        end_idx++;
    }
    return end_idx;
}

void copy_matrix(struct Matrix dist, int **src)
{
    for (int i = 0; i < dist.rows; i++)
    {
        for (int j = 0; j < dist.cols; j++)
            dist.data[i][j] = src[i][j];
    }
}

void print_matrix(struct Matrix matrix)
{
    int r = matrix.rows;
    int c = matrix.cols;
    printf("[");

    for (int i = 0; i < r; i++)
    {
        for (int j = 0; j < c; j++)
        {
            printf("%d", matrix.data[i][j]);
            if (j != c - 1)
                printf(" ");
        }
        if (i != r - 1)
            printf("; ");
    }
    printf("]\n");
}

void print_error(int return_code)
{
    switch (return_code)
    {
    case ERROR_INPUT:
        fprintf(stderr, "Error: Chybny vstup!\n");
        break;
    }
}

void free_matrix(struct Matrix matrix)
{
    for (int i = 0; i < matrix.rows; i++)
    {
        free(matrix.data[i]);
    }
    free(matrix.data);
}

void free_matrix_array(struct MatrixArray matrix_array)
{
    for (int i = 0; i <= matrix_array.size; i++)
    {
        free_matrix(matrix_array.equation[i]);
    }

    for (int i = 0; i < 26; i++)
    {
        if (matrix_array.matrices[i].rows)
        {
            if (matrix_array.matrices[i].too_big == 0)
            {
                for (int j = 0; j < FIRST_MATRIX_CAPACITY; j++)
                {
                    free(matrix_array.matrices[i].data[j]);
                }
                free(matrix_array.matrices[i].data);
            }
            else if (matrix_array.matrices[i].too_big == 1)
            {
                for (int j = 0; j < SECOND_MATRIX_CAPACITY; j++)
                {
                    free(matrix_array.matrices[i].data[j]);
                }
                free(matrix_array.matrices[i].data);
            }
            else if (matrix_array.matrices[i].too_big == 2)
            {
                for (int j = 0; j < THIRD_MATRIX_CAPACITY; j++)
                {
                    free(matrix_array.matrices[i].data[j]);
                }
                free(matrix_array.matrices[i].data);
            }
        }
    }

    free(matrix_array.matrices);
    free(matrix_array.equation);
    free(matrix_array.operations);
}

struct MatrixArray read_equation(void)
{
    struct MatrixArray matrix_array;

    matrix_array.equation = malloc(INITIAL_CAPACITY * sizeof(struct Matrix));
    matrix_array.operations = malloc(INITIAL_CAPACITY * sizeof(char));
    matrix_array.matrices = malloc(NUM_LETTERS * sizeof(struct Matrix));
    matrix_array.size = 0;
    matrix_array.max_rows = 0;
    matrix_array.max_cols = 0;
    matrix_array.capacity = INITIAL_CAPACITY;
    matrix_array.error_code = EXIT_SUCCESS;
    // initialize rows to later free only initialized matrices
    for (int i = 0; i < 26; i++)
        matrix_array.matrices[i].rows = 0;

    char c;
    char *line = NULL;
    size_t len = 0;
    char matrix_idx;

    while (isalpha(c = getchar()))
    {

        int current_cols = 0;
        int current_rows = 0;
        struct Matrix matrix;
        matrix.too_big = 0;

        // create matrix and allocate memory for it
        matrix.data = malloc(FIRST_MATRIX_CAPACITY * sizeof(int *));
        if (!matrix.data)
        {
            matrix_array.error_code = ERROR_OUT_OF_MEMORY;
            break;
        }
        for (int i = 0; i < FIRST_MATRIX_CAPACITY; i++)
        {
            matrix.data[i] = malloc(FIRST_MATRIX_CAPACITY * sizeof(int));
            // printf("allocating row for matrix %c\n", c);
            if (!matrix.data[i])
            {
                matrix_array.error_code = ERROR_OUT_OF_MEMORY;
                break;
            }
        }

        // read the line and remove everything not needed from it
        getline(&line, &len, stdin);
        matrix_idx = c;
        strtok(line, "[");
        char *matrix_string = strtok(NULL, "[");
        matrix_string[strlen(matrix_string) - 2] = '\0';

        // split it in rows by ;
        char *row_saveptr, *col_saveptr;
        char *row = strtok_r(matrix_string, ";", &row_saveptr);

        int i = 0;
        while (row != NULL)
        {
            int j = 0;

            // split in numbers by spaces
            char *col = strtok_r(row, " ", &col_saveptr);
            while (col != NULL)
            {
                matrix.data[i][j++] = atoi(col);
                col = strtok_r(NULL, " ", &col_saveptr);
                if (j == (FIRST_MATRIX_CAPACITY - 50) && matrix.too_big == 0)
                {
                    matrix.too_big = 1;
                    matrix.data = realloc(matrix.data, sizeof(int *) * SECOND_MATRIX_CAPACITY);
                    int k;
                    for (k = 0; k < FIRST_MATRIX_CAPACITY; k++)
                    {
                        matrix.data[k] = realloc(matrix.data[k], sizeof(int) * SECOND_MATRIX_CAPACITY);
                    }
                    while (k < SECOND_MATRIX_CAPACITY - 1)
                    {
                        k++;
                        matrix.data[k] = malloc(sizeof(int) * SECOND_MATRIX_CAPACITY);
                    }
                }
                if (j == (SECOND_MATRIX_CAPACITY - 50) && matrix.too_big == 1)
                {
                    matrix.too_big = 2;
                    matrix.data = realloc(matrix.data, sizeof(int *) * THIRD_MATRIX_CAPACITY);
                    int k;
                    for (k = 0; k < FIRST_MATRIX_CAPACITY; k++)
                    {
                        matrix.data[k] = realloc(matrix.data[k], sizeof(int) * THIRD_MATRIX_CAPACITY);
                    }
                    while (k < THIRD_MATRIX_CAPACITY - 1)
                    {
                        k++;
                        matrix.data[k] = malloc(sizeof(int) * THIRD_MATRIX_CAPACITY);
                    }
                }
            }

            // check the number of columns or check if its correct
            if (!current_cols)
                current_cols = j;
            else if (current_cols != j)
                matrix_array.error_code = ERROR_INPUT;

            // go to another row
            i++;
            row = strtok_r(NULL, ";", &row_saveptr);
        }

        // update the information of the matrix
        current_rows = i;
        matrix.rows = current_rows;
        matrix.cols = current_cols;

        if (current_rows > matrix_array.max_rows)
            matrix_array.max_rows = current_rows;

        if (current_cols > matrix_array.max_cols)
            matrix_array.max_cols = current_cols;

        matrix_array.matrices[matrix_idx - 'A'] = matrix;

        if (matrix_array.error_code != EXIT_SUCCESS)
            return matrix_array;
    }

    free(line);

    while ((c = getchar()) != EOF)
    {
        if (!isalpha(c) && (c != '*' && c != '+' && c != '-'))
            continue;

        else if (isalpha(c))
        {
            if (matrix_array.size == matrix_array.capacity - 2)
            {
                matrix_array.capacity *= 2;
                matrix_array.equation = realloc(matrix_array.equation, matrix_array.capacity * sizeof(struct Matrix));
                matrix_array.operations = realloc(matrix_array.operations, matrix_array.capacity * sizeof(char));
                if (!matrix_array.equation || !matrix_array.operations)
                {
                    matrix_array.error_code = ERROR_OUT_OF_MEMORY;
                    break;
                }
            }
            int index_of_matrix = c - 'A';
            int matrix_rows = matrix_array.matrices[index_of_matrix].rows;
            int matrix_cols = matrix_array.matrices[index_of_matrix].cols;

            matrix_array.equation[matrix_array.size].rows = matrix_rows;
            matrix_array.equation[matrix_array.size].cols = matrix_cols;

            matrix_array.equation[matrix_array.size].data = malloc(matrix_rows * sizeof(int *));
            for (int i = 0; i < matrix_rows; i++)
                matrix_array.equation[matrix_array.size].data[i] = malloc(matrix_cols * sizeof(int));

            copy_matrix(matrix_array.equation[matrix_array.size], matrix_array.matrices[index_of_matrix].data);

            matrix_array.size++;
        }
        else
        {
            matrix_array.operations[matrix_array.size - 1] = c;
        }
    }

    matrix_array.size--;
    return matrix_array;
}

void check_input_errors(struct MatrixArray *matrix_array)
{
    int end_of_mult_sequence;
    int sequence_rows = 0;

    for (int i = 0; i < matrix_array->size; i++)
    {
        int current_rows = matrix_array->equation[i].rows;
        int current_cols = matrix_array->equation[i].cols;
        int next_rows = matrix_array->equation[i + 1].rows;
        int next_cols = matrix_array->equation[i + 1].cols;
        char operation = matrix_array->operations[i];

        if (operation == '*')
        {
            if (current_cols != next_rows)
            {
                matrix_array->error_code = ERROR_INPUT;
                return;
            }
            if (!sequence_rows)
                sequence_rows = current_rows;
        }
        else
        {
            if (sequence_rows)
            {
                if (i != matrix_array->size - 1 && matrix_array->operations[i + 1] != '*')
                {

                    if (sequence_rows != next_rows || current_cols != next_cols)
                    {
                        matrix_array->error_code = ERROR_INPUT;
                        return;
                    }
                }
                else
                {
                    end_of_mult_sequence = find_end_of_mult_sequence(*matrix_array, i + 1);
                    if (sequence_rows != next_rows || current_cols != matrix_array->equation[end_of_mult_sequence].cols)
                    {
                        matrix_array->error_code = ERROR_INPUT;
                        return;
                    }
                }
            }
            else
            {
                if (i != matrix_array->size - 1 && matrix_array->operations[i + 1] != '*')
                {
                    if (current_rows != next_rows || current_cols != next_cols)
                    {
                        matrix_array->error_code = ERROR_INPUT;
                        return;
                    }
                }
                else
                {
                    end_of_mult_sequence = find_end_of_mult_sequence(*matrix_array, i + 1);
                    if (current_rows != next_rows || current_cols != matrix_array->equation[end_of_mult_sequence].cols)
                    {
                        matrix_array->error_code = ERROR_INPUT;
                        return;
                    }
                }
            }
        }
    }
}

void getline(char **lineptr, size_t *n, FILE *stream)
{
    if (!lineptr || !n || !stream)
        return;

    const size_t chunk_size = 64;
    size_t buffer_size = *n;
    if (!*lineptr)
    {
        buffer_size = chunk_size;
        *lineptr = malloc(buffer_size);
        if (!*lineptr)
            return;
    }

    char *ptr = *lineptr;
    size_t read_chars = 0;

    while (1)
    {
        int c = fgetc(stream);
        if (c == EOF)
        {
            if (read_chars == 0)
                return;
            break;
        }

        if (read_chars + 1 >= buffer_size)
        {
            buffer_size += chunk_size;
            char *new_ptr = realloc(ptr, buffer_size);
            if (!new_ptr)
                return;
            *lineptr = new_ptr;
            ptr = new_ptr;
        }

        ptr[read_chars++] = (char)c;

        if (c == '\n')
            break;
    }

    ptr[read_chars] = '\0';
    *n = buffer_size;
}

char *strtok_r(char *str, const char *delim, char **saveptr)
{
    if (!delim || !saveptr)
        return NULL;

    char *token_start = (str != NULL) ? str : *saveptr;
    token_start += strspn(token_start, delim);

    if (*token_start == '\0')
    {
        *saveptr = token_start;
        return NULL;
    }

    char *token_end = token_start + strcspn(token_start, delim);

    if (*token_end == '\0')
    {
        *saveptr = token_end;
    }
    else
    {
        *token_end = '\0';
        *saveptr = token_end + 1;
    }

    return token_start;
}
