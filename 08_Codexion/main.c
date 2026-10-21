#include "coders.h"

int main (int ac, char av)
{
    if (av == 5 || av == 6)
    {
        // correct input
        // 1) errors checking, filling 
        parse_input(&workspace, av);

        // 2) creating the actual thing
        data_init(&workspace);
        
        // 3)
        work_start(&workspace);

        // 4) No leaks || coder burnout
        clan(&workspace);
    }
    else
    {
        // incorrect input
        error_exit("Wrong input:\n"
                G"Correct is ./coder 5 800 200 200 [5]"RST);
    }
}