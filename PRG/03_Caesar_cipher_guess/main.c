
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
int compare(char *string1, char *string2);
char *decode(char *coded, char *rumor);

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

// Decode the coded string using the rumor as a key
char *decode(char *coded, char *rumor)
{
    // Initialize variables
    int best_offset = 0;
    int best_score = 0;
    int score;
    char *temp_string = (char *)malloc(strlen(coded) + 1);

    // Try all possible offsets and find the best match
    for (int i = 0; i <= 52; i++)
    {
        strcpy(temp_string, coded);
        shift(temp_string, i);
        score = compare(temp_string, rumor);
        if (score > best_score)
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

// Compare two strings and return the number of matching characters
int compare(char *string1, char *string2)
{
    int same = 0;
    for (int i = 0; i < strlen(string1); i++)
        if (string1[i] == string2[i])
            same++;
    return same;
}

int read_input(char *coded, char *rumor)
{
    // Return error if a character isnt a letter
    for (int i = 0; i < strlen(coded); i++)
        if (!isalpha(coded[i]) || !isalpha(rumor[i]))
            return ERROR_INPUT;

    // Or if the lengths are different
    if (strlen(coded) != strlen(rumor))
        return ERROR_INPUT_LENGTH;
    else
        return EXIT_SUCCESS;
}

// Read one word from input
char *read_word(void)
{
    int capacity = INITIAL_LENGTH_OF_INPUT;
    int length = 0;
    char *word = malloc(INITIAL_LENGTH_OF_INPUT);

    int c;
    while ((c = getchar()) != '\n')
    {
        // Reallocate more memory if needed
        if (length + 1 >= capacity)
        {
            capacity += 10;
            char *new_str = realloc(word, capacity);
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
    case ERROR_INPUT_LENGTH:
        fprintf(stderr, "Error: Chybna delka vstupu!\n");
        break;
    }
}
