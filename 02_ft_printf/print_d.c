/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_d.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/07 23:17:20 by codespace         #+#    #+#             */
/*   Updated: 2026/06/08 01:11:42 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "ft_printf.h"

int print_d(int number)
{   
    int i;
    unsigned int n;

    i = 0;
    if(number < 0)
    {
        write(1, "-", 1);
        i++;
        n = print_d(-number);
    }
    else
    {
        n = (unsigned int)number;
        if(n >= DECIMAL_BASE)
        i += print_d(n / DECIMAL_BASE);
        i += print_char((n % DECIMAL_BASE) + '0');
    }
    return(i);
}
