#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>
#include <string.h>

// Define error codes
#define ERROR_INPUT 100
#define ERROR_INPUT_LENGTH 101

// Define the initial length of the input buffer
#define INITIAL_LENGTH_OF_INPUT 10

// Input functions
char *read_word(void);
int read_input(char *coded, char *rumor);
void print_error(int error_code);

// Decoding
char rotate(char original, int offset);
void shift(char *string, int offset);
char *decode(char *coded, char *rumor);
int wagner_fischer(char *string1, char *string2);
int min(int x, int y, int z);

/* The main program */
int main(int argc, char *argv[])
{
    // Read the coded and rumor strings
    char *coded = read_word();
    char *rumor = read_word();

    // Check the input for errors
    int error_code = read_input(coded, rumor);
    if (error_code != EXIT_SUCCESS)
    {
        // Print an error message and exit
        print_error(error_code);
        free(coded);
        free(rumor);
        return error_code;
    }

    // Decode the coded string and print the rumor
    printf("%s\n", decode(coded, rumor));

    // Free memory and exit
    free(coded);
    free(rumor);
    return error_code;
}

int min(int x, int y, int z)
{
    if (x <= y && x <= z)
        return x;
    if (y <= x && y <= z)
        return y;
    return z;
}

int wagner_fischer(char *string1, char *string2)
{
    int len1 = strlen(string1);
    int len2 = strlen(string2);
    int **dist = (int **)malloc((len1 + 1) * sizeof(int *));

    for (int i = 0; i <= len1; i++)
        dist[i] = (int *)malloc((len2 + 1) * sizeof(int));

    for (int i = 0; i <= len1; i++)
        dist[i][0] = i;
    for (int j = 0; j <= len2; j++)
        dist[0][j] = j;

    for (int j = 1; j <= len2; j++)
    {
        for (int i = 1; i <= len1; i++)
        {
            if (string1[i - 1] == string2[j - 1])
                dist[i][j] = dist[i - 1][j - 1];
            else
                dist[i][j] = min(dist[i - 1][j] + 1,      // deletion
                                 dist[i][j - 1] + 1,      // insertion
                                 dist[i - 1][j - 1] + 1); // substitution
        }
    }

    int result = dist[len1][len2];

    for (int i = 0; i <= len1; i++)
        free(dist[i]);
    free(dist);

    return result;
}

// Decode the coded string using the rumor as a key
char *decode(char *coded, char *rumor)
{
    // Initialize variables
    int best_offset = 0;
    int best_score = strlen(coded);
    int score;
    char *temp_string = (char *)malloc((strlen(coded) + 1) * sizeof(char));

    // Try all possible offsets and find the best match
    for (int i = 0; i <= 52; i++)
    {
        strcpy(temp_string, coded);
        shift(temp_string, i);
        // printf("%s\n", temp_string);
        score = wagner_fischer(temp_string, rumor);
        if (score < best_score)
        {
            best_score = score;
            best_offset = i;
        }
    }

    // Free memory and return the decoded string
    free(temp_string);
    shift(coded, best_offset);
    return coded;
}

// Rotate a character by the given offset
char rotate(char original, int offset)
{
    int index;
    if (isupper(original))
    {
        index = original - 'A' + offset;
        if ((index / 26) % 2 == 1)
            return (index % 26 + 'a');
        else
            return (index % 26 + 'A');
    }
    else
    {
        index = original - 'a' + offset;
        if ((index / 26) % 2 == 1)
            return (index % 26 + 'A');
        else
            return (index % 26 + 'a');
    }
}

// Shift a string by the given offset
void shift(char *string, int offset)
{
    for (int i = 0; i < strlen(string); i++)
        string[i] = rotate(string[i], offset);
}

int read_input(char *coded, char *rumor)
{
    // Return error if a character isnt a letter
    for (int i = 0; i < strlen(coded); i++)
        if (!isalpha(coded[i]))
            return ERROR_INPUT;
    for (int i = 0; i < strlen(rumor); i++)
        if (!isalpha(rumor[i]))
            return ERROR_INPUT;

    return EXIT_SUCCESS;
}

// Read one word from input
char *read_word(void)
{
    int capacity = INITIAL_LENGTH_OF_INPUT;
    int length = 0;
    char *word = malloc(INITIAL_LENGTH_OF_INPUT * sizeof(char));

    int c;
    while ((c = getchar()) != '\n')
    {
        // Reallocate more memory if needed
        if (length + 1 >= capacity)
        {
            capacity += 2;
            char *new_str = realloc(word, capacity * sizeof(char));
            word = new_str;
        }

        word[length++] = c;
    }
    // Terminate the string
    word[length] = '\0';
    return word;
}

// Print errors
void print_error(int return_code)
{
    switch (return_code)
    {
    case ERROR_INPUT:
        fprintf(stderr, "Error: Chybny vstup!\n");
        break;
    }
}
