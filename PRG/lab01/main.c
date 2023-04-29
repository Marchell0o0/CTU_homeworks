#include <stdio.h>

#define MINUS1(i) i % 2 ? 1 : -1
#define MINUS2(cis) cis * (-1)
#define MINUS3(cis) cis == 1 ? -1 : 1
#define MINUS4(cis) ~cis | 0x01

int main() {
    for (int i = 1; i< 10; ++i){
        for (int j = 1; j<=10; ++j){
            if (i == j)
                printf("%d ", i*j);
            else 
            printf("    ");
        }
        printf("\n");
        
    }
    printf("\n");
    return 0;
}
