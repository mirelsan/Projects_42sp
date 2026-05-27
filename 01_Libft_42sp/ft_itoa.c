/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/05/26 23:49:44 by codespace         #+#    #+#             */
/*   Updated: 2026/05/27 02:03:44 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t ft_is_negative(int n)
{
    if(n < 0)
        return(1);
    else
        return(0);    
}

size_t ft_count_digits(size_t n)
{
    unsigned int i;

    if(n == 0)
        return(1);

    i = 0;

    if(n > 0 )
    {
        n / 10;
        i++;
    } 
    return(i);       
}

char	*ft_itoa(int n)
{
    char *str;
    unsigned int i;
    long int number;
    unsigned int count_digits;

    str = ft_is_negative(n);
    number = n;
    
    if(str == 1)
    number *= -1;
    
    count_digits = ft_count_digits(n);
    str =(malloc(count_digits + i + 1));

    if(!str)
        return(NULL);
        
    if(i == 1)
    str[0] = '-';   
    str[count_digits + i] = '\0';

    while(count_digits > 0)
    {
        str[(count_digits - 1) + i] = (number % 10) + '\0';
        number /= 10;
        count_digits--;
    }
    return(str);
}