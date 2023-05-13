#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <ctype.h>

#define ERROR_INPUT 100
#define MAX_DIGITS 100              // max digits for input
#define SIZE_OF_PRIMES_LIST 1000000 // how many primes to check

// checks if a big number is a one
int is_one(char *number);

// checks if there are any letters in a number
int letters_in_number(char *number);

// check for errors in an input
int read_input(char *number);

// print out errors
void print_error(int return_code);

// main function
void print_prime_factors(char number[], int *primes);

// creates an array prime[index] == 1 means index is prime and if == 0 index is a non-prime
void eratosthenes_sieve(int *primes);

// divides a big number and returns a remainder
int divide(char *num, int divisor);

// copies a big number into an empty array
void copy(char number[], char number_copy[]);

/* The main program */
int main(int argc, char *argv[])
{
    // intialize the variables
    int return_code;
    int *primes = malloc(sizeof(int) * SIZE_OF_PRIMES_LIST);
    char number[MAX_DIGITS];

    // create an array of primes
    eratosthenes_sieve(primes);

    for (;;)
    {
        // assign a value and check if its correct
        return_code = read_input(number);

        // check if the input is 0
        int len = strlen(number);
        if (len == 1 && number[0] == '0')
            break;

        else
        {
            if (return_code == EXIT_SUCCESS)
            {

                // special case for 1
                if (is_one(number) == 1)
                    printf("Prvociselny rozklad cisla 1 je:\n1\n");

                // main function
                else
                    print_prime_factors(number, primes);
            }

            else
            {
                free(primes);
                print_error(return_code);
                return return_code;
            }
        }
    }
    free(primes);
    return return_code;
}

void eratosthenes_sieve(int *primes)
{
    // fill up the array with 1s
    for (int i = 0; i < SIZE_OF_PRIMES_LIST; i += 1)
    {
        primes[i] = 1;
    }

    // change every multiple of a prime to 0
    for (int p = 2; p < sqrt(SIZE_OF_PRIMES_LIST) - 1; p++)
    {
        if (primes[p] == 1)
        {
            for (int k = p * p; k < SIZE_OF_PRIMES_LIST; k += p)
            {
                primes[k] = 0;
            }
        }
    }
}

void print_prime_factors(char number[], int *primes)
{

    printf("Prvociselny rozklad cisla %s je:\n", number);

    for (int i = 2; i <= SIZE_OF_PRIMES_LIST; i++)
    {
        // go through possible factors
        if (primes[i] == 1)
        {
            // copy a number so that when it checks for remainder it doesnt change
            char number_copy[strlen(number) + 1];
            copy(number, number_copy);

            int amount = 0;
            int remainder = divide(number_copy, i);

            // if the remainder is 0 divide by that number
            while (remainder == 0)
            {
                divide(number, i);
                amount += 1;
                copy(number, number_copy);
                remainder = divide(number_copy, i);
            }

            if (amount >= 1)
                printf("%d", i);

            if (amount > 1)
                printf("^%d", amount);

            // in the end dont print " x "
            if (is_one(number) == 1)
                break;

            else if (amount != 0)
                printf(" x ");
        }
    }
    printf("\n");
}

void copy(char number[], char number_copy[])
{
    // transfers every digit to the copy and adds \0 in the end
    for (int i = 0; i < strlen(number); i++)
    {
        number_copy[i] = number[i];
    }
    number_copy[strlen(number)] = '\0';
}

int is_one(char *number)
{
    int len = strlen(number);

    // check if the last digit is 1
    int value = number[len - 1] - '0';
    if (value != 1)
        return 0;

    // check if all other digits are 0
    for (int i = len - 2; i >= 0; i--)
    {
        value = number[i] - '0';
        if (value != 0)
            return 0;
    }

    // else return true
    return 1;
}

int divide(char *number, int divisor)
{
    int len = strlen(number);
    int remainder = 0;

    for (int i = 0; i < len; i++)
    {
        int digit = number[i] - '0';
        int quotient = (remainder * 10 + digit) / divisor;
        remainder = (remainder * 10 + digit) % divisor;
        number[i] = quotient + '0';
    }
    return remainder;
}

int letters_in_number(char *number)
{
    int len = strlen(number);

    for (int i = 0; i < len; i++)
    {
        if (isalpha(number[i]))
            return 1;
    }
    return 0;
}

int read_input(char *number)
{
    int correct_inputs = scanf("%s", number);

    if (correct_inputs != 1 || number[0] == '-' || letters_in_number(number))
        return ERROR_INPUT;
    else
        return EXIT_SUCCESS;
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
