#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define ERROR_INPUT 100
#define SIZE_OF_PRIMES_LIST 1000000 // how many primes to check

// check for errors in an input
int read_input(long long *number);

// print out errors
void print_error(int return_code);

// main function
void print_prime_factors(long long number, int *primes);

// creates an array prime[index] == 1 means index is prime and if == 0 index is
// a non-prime
void eratosthenes_sieve(int *primes);

/* The main program */
int main(int argc, char *argv[])
{
    // intialize the variables
    int return_code;
    int *primes = malloc(sizeof(int) * SIZE_OF_PRIMES_LIST);
    long long number;

    // create an array of primes
    eratosthenes_sieve(primes);

    for (;;)
    {
        // assign a value and check if its correct
        return_code = read_input(&number);

        // check if the input is 0
        if (number == 0)
            break;

        else
        {
            if (return_code == EXIT_SUCCESS)
            {

                // special case for 1
                if (number == 1)
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

void print_prime_factors(long long number, int *primes)
{

    printf("Prvociselny rozklad cisla %lld je:\n", number);

    for (int i = 2; i <= SIZE_OF_PRIMES_LIST; i++)
    {
        // go through possible factors
        if (primes[i] == 1)
        {
            int amount = 0;

            // if the remainder is 0 divide by that number
            while (number % i == 0)
            {
                number /= i;
                amount += 1;
            }

            if (amount >= 1)
                printf("%d", i);

            if (amount > 1)
                printf("^%d", amount);

            // in the end dont print " x "
            if (number == 1)
                break;

            else if (amount != 0)
                printf(" x ");
        }
    }
    printf("\n");
}

int read_input(long long *number)
{
    int correct_inputs = scanf("%lld", number);

    if (correct_inputs != 1 || *number < 0)
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
