#include <stdio.h>
#include <stdlib.h>

#define WEEK_DAYS 7
// static const char *texts_en[] = {
//     ""
//     ""
//     ""
//     ""
// };
// enum {
//     str_promt,
//     str_error_input,
//     str_error_range,
//     str_num
// };

static char *day_of_week[] = {"Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"};
// static char *name_of_month[] = {
// 	"January",
// 	"February",
// 	"March",
// 	"April",
// 	"May",
// 	"June",
// 	"July",
// 	"August",
// 	"September",
// 	"October",
// 	"November",
// 	"December"};
static int days_in_month[] = {31, 29, 31, 30, 31, 30,
							  31, 31, 30, 31, 30, 31};
// static int first_day_in_september = 2; // 1. 3. 2023 is Wednesday
static int first_day_in_year = 6; // 1. 1. 2023 is Sunday
 
void prt_days_header();
void prt_day_table(int, int );
void prt_month(int);
int get_first_day_in_month(int);
void prt_months(int, int);

int main(int argc, char const *argv[])
{
    prt_days_header();
    printf("%d\n", get_first_day_in_month(2));
    return 0;
}


void prt_days_header(){
    for (int i = 0; i < WEEK_DAYS; ++i)
        printf(" %s", day_of_week[i]);
    printf("\n");
}
void prt_days_table(int a, int b){

}

void prt_month(int month){
    int first_day = get_first_day_in_month(month);
    for (int i = 0; i < first_day; ++i)
        printf("    ");
    for (int i = 0; i < days_in_month[month]; i++){
        printf("%3d", i + 1);
        if ((first_day + i + 1) % WEEK_DAYS == 0)
            printf("\n");
    }
}

int get_first_day_in_month(int month){
    int first_day = first_day_in_year;
    for (int i = 0; i < month; ++i)
        first_day += days_in_month[i];
    return first_day % WEEK_DAYS;
}

void prt_months(int a, int b){

}


