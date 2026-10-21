#include "coders.h"



// ./coder 5    800     200     200 [5]
//        av[1] av[2]   av[3] ...
//1) actual numbers
//2)not > INT_MAX
//3) TIMESTAMPS > 60ms

void parse_input(t_workspace *workspace, char **av)
{
    workspace->number_of_coders = ft(atoi(av[1]));
}