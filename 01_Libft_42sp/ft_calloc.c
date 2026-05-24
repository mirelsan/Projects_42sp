/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mirelapitt <mirelapitt@student.42.fr>      +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/24 12:04:06 by mirelapitt        #+#    #+#             */
/*   Updated: 2026/05/24 12:11:02 by mirelapitt       ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */



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