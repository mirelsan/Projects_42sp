#include "libft.h"

void        *ft_calloc(size_t nmemb, size_t size)
{
    size_t sum;
    void *p;
    
    sum = (nmemb * size);
    p = malloc(sum);
    if(!p)
        return(NULL);
    ft_memset(p, 0, sum);
        return(p);    
}