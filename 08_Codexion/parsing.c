#include "coders.h"

static inline bool is_digit(char c)
{
    return (c >= '0' && c <= '9');
}

static inline bool is_space(char c)
{
    return ((c >= 9 && c <= 13) || 32 == c);
}

//1) check for negative
//2) check if the number is legit
//3) check for INT_MAX
// 2_147_483_674 -> 9_999_999
// why return ptr

static const char *valid_input(const char *str)
{
    int len ;
    const char *number;

    len = 0;
    // 1) skip spaces
    while (is_space(*str))
        ++str;
    if (*str == '+')
        ++str;
    else if (*str == '-')
        error_exit("Feed me only positive values u suck!");
    if (!is_digit(*str))
        error_exit("The input is not a correct digit");
    number = str;
    while (is_digit(*str++))
        ++len;
    if (len > 10)
        error_exit("The value is too big, INT_MAX is the limit");
    return (number);
}

static long ft_atoi(const char *str)
{
    long    num;
    num = 0;
    str = valid_input(str);
    while (is_digit(*str))
    {
        num = (num * 10) + (*str - '0');
        str++;
    }
    while (is_space(*str))
        str++;
    if (*str != '\0')
        error_exit("Input contains invalid non-digit characters!");
    
    if (num > INT_MAX)
        error_exit("The value is too big, INT_MAX is the limit");
    return (num);
}

// ./coder 5    800     200     200 [5]
//        av[1] av[2]   av[3] ...
//1) actual numbers
//2)not > INT_MAX
//3) TIMESTAMPS > 60ms

static long parse_scheduler(const char *str)
{
    if (strcmp(str, "fifo") == 0)
        return (SCHEDULER_FIFO);
    if (strcmp(str, "edf") == 0)
        return (SCHEDULER_EDF);
    error_exit("Invalid scheduler! Choose 'fifo' or 'edf'.");
    return (-1);
}

void parse_input(t_workspace *workspace, char **av)
{
    workspace->number_of_coders = ft_atoi(av[1]);
    if (workspace->number_of_coders <= 0)
        error_exit("Number of coders must be greater than 0");
    
    // Converting milis to microsecs (* 1000)
    workspace->time_to_burnout = ft_atoi(av[2]);
    workspace->time_to_compile = ft_atoi(av[3]);
    workspace->time_to_debug = ft_atoi(av[4]);
    workspace->time_to_refactor = ft_atoi(av[5]);
    workspace->dongle_cooldown = ft_atoi(av[7]);

    workspace->number_of_compiles_required = ft_atoi(av[6]);
    if (workspace->number_of_compiles_required <= 0)
        error_exit("Number of compiles required must be greater than 0");
    
    workspace->scheduler = parse_scheduler(av[8]);

}