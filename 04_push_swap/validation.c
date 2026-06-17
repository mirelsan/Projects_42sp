/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   validation.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/16 23:59:37 by codespace         #+#    #+#             */
/*   Updated: 2026/06/17 01:37:01 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//1. verify if int is valid
//2. verify if int is in the range
//3. verify duplicates

#include "push_swap.h"

int ft_int_validated(char *str)
{
    if(*str == '\0')
        return(0);
    
    while(*str)
    {
        if (*str < '0' || *str > '9')
        {
            return (0);
        }
            str++;
    }
    return (1);
}

int ft_int_range(char *str)
{
    if(*str >= '-2147483648' && *str <= '2147483647')
        return(1);
    else
        return(0);    
}

int ft_int_duplicate(char *str)
{
    
}