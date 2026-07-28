#include <stdlib.h>

int absolute_value(int num) 
{ 
    if (num < 0) 
        num = -num;
    return (num);
}

int *ft_range(int start, int end)
{
    int width;
    int *var_int;
    width = absolute_value(end - start) + 1;
    var_int = malloc(sizeof(int) * width);
    if(!var_int)
        return NULL;
    int i = 0;
    int j = start;
    while(i < width)
    {
        if(start <= end)
        {
            var_int[i] = j;
            j++;
        }
        else if(start > end)
        {
            var_int[i] = j;
            j--;
        }
        i++;
    }
    return(var_int);
}
