#include <stdio.h>


int main()
{
int m, dvacet = 0, deset = 0, pet = 0, dva = 0, jedna = 0;
scanf("%d", &m);
printf("%i\n", m);
while (m >= 20) {
    m = m - 20;
    ++dvacet;
}
while (m >= 10) {
    m = m - 10;
    ++deset;
}
while (m >= 5) {
    m = m - 5;
    ++pet;
}
while (m >= 2) {
    m = m - 2;
    ++dva;
}
if (m == 1) {
    ++jedna;
}
if (dvacet != 0) {
    printf("Dvacet ");
    printf("%i\n", dvacet);
}
if (deset != 0) {
    printf("Deset ");
    printf("%i\n", deset);
}
if (pet != 0) {
    printf("Pet ");
    printf("%i\n", pet);
}
if (dva != 0) {
    printf("Dva ");
    printf("%i\n", dva);
}
if (jedna != 0) {
    printf("Jedna ");
    printf("%i\n", jedna);
}

}
