#include "coders.h"
#include <stdio.h>
#include <stdlib.h>

void    error_exit(const char *error)
{
    printf("%s\n", error);
    exit(EXIT_FAILURE);
}

