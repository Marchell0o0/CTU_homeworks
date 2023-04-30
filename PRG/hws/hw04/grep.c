#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>

int string_in_string(char *string1, char *string2);
int string_in_array(char *array[], char *element, int array_length);
int *find_string(char *string, const char *word, int *count);
int *find_string_old(char *string, char *word, int *count);
int match_pattern(const char *string, const char *pattern);

void print_colored(char *line, int *indexes, char *word, int length_of_indexes);
int string_length(char *string);

/* The main program */
int main(int argc, char *argv[])
{
    FILE *ptr;

    char *line = NULL;
    size_t length = 0;
    ssize_t read;

    char *word;
    int return_code = EXIT_FAILURE;

    if (argc <= 1)
    {
        return 100;
    }

    // check if there is a file argument, if not redirect to stdin
    ptr = fopen(argv[argc - 1], "r");
    if (ptr == NULL)
    {
        word = argv[argc - 1];
        ptr = stdin;
    }
    else
        word = argv[argc - 2];

    int colors = string_in_array(argv, "--color=always", argc);
    int special_symbols = string_in_array(argv, "-E", argc);

    int *occurrences;
    while ((read = getline(&line, &length, ptr)) != EOF)
    {
        int count = 0;
        if (special_symbols)
            occurrences = find_string(line, word, &count);
        else
            occurrences = find_string_old(line, word, &count);

        if (occurrences != NULL)
        {
            if (colors)
                print_colored(line, occurrences, word, count);

            else
                printf("%s", line);
            free(occurrences);
            occurrences = NULL;

            return_code = EXIT_SUCCESS;
        }
    }

    fclose(ptr);

    if (occurrences != NULL)
        free(occurrences);

    if (line)
        free(line);
    return return_code;
}

void print_colored(char *line, int *indexes, char *word, int length_of_indexes)
{
    int i, j = -1;
    // int k = 0;
    int length_of_word;
    int finished = 1;

    for (i = 0; line[i] != '\0'; i++)
    {
        if ((length_of_word = match_pattern(line + i, word)) && finished)
        {
            printf("\033[01;31m\033[K");
            finished = 0;
            j = i + length_of_word;
        }
        if (i == j)
        {
            printf("\033[m\033[K");
            finished = 1;
        }

        printf("%c", line[i]);
    }
}

int string_in_string(char *string1, char *string2)
{
    int i, j;

    for (i = 0; string2[i] != '\0'; i++)
    {
        if (string2[i] == string1[0])
        {
            for (j = 1; string1[j] != '\0'; j++)
            {
                if (string2[i + j] != string1[j])
                    break;
            }
            if (string1[j] == '\0')
                return 1;
        }
    }
    return 0;
}

int *find_string_old(char *string, char *word, int *count)
{
    int i, j;
    int idx;
    int *indexes = NULL;
    for (i = 0; string[i] != '\0'; i++)
    {
        if (string[i] == word[0])
        {
            idx = i;
            for (j = 1; word[j] != '\0'; j++)
            {
                if (string[i + j] != word[j])
                {
                    idx = -1;
                    break;
                }
            }
            if (idx != -1)
            {

                int *new_indexes = realloc(indexes, (*count + 1) * sizeof(int));

                indexes = new_indexes;

                indexes[*count] = idx;
                *count = *count + 1;
            }
        }
    }
    return indexes;
}

int match_pattern(const char *string, const char *pattern)
{
    int length = 0;
    while (*pattern)
    {

        if (*string != *pattern)
        {
            if (*pattern == '?')
                ++pattern;

            else if (*pattern == '*')
            {
                --pattern;
                while (*string == *pattern)
                {
                    ++string;
                    ++length;
                }
            }
            else if (*pattern == '+')
            {
                --pattern;
                while (*string == *pattern)
                {
                    ++string;
                    ++length;
                }

                ++pattern;
                ++pattern;
            }

            else
            {
                ++pattern;
                if (*pattern == '?' || *pattern == '*')
                    ++pattern;

                else
                    return 0;
            }
        }
        else
        {
            ++pattern;
            ++string;
            ++length;
        }
    }
    return length;
}

int *find_string(char *string, const char *word, int *count)
{
    int *indexes = NULL;
    int i;

    for (i = 0; string[i] != '\0'; i++)
    {
        // printf("calling the function\n");
        if (match_pattern(string + i, word))
        {
            int *new_indexes = realloc(indexes, (*count + 1) * sizeof(int));

            indexes = new_indexes;
            indexes[*count] = i;
            *count = *count + 1;
        }
    }
    return indexes;
}

int string_in_array(char *array[], char *element, int array_length)
{
    int string_in_array = 0;
    for (int i = 0; i < array_length; i++)
    {
        if (string_in_string(array[i], element))
        {
            string_in_array = 1;
        }
    }
    return string_in_array;
}
int int_in_array(int *array, int element, int array_length)
{
    int int_in_array = 0;
    for (int i = 0; i < array_length; i++)
    {
        if (array[i] == element)
            int_in_array = 1;
    }
    return int_in_array;
}

int string_length(char *string)
{
    int length = 0;

    while (string[length] != '\0')
        length++;

    return length;
}
