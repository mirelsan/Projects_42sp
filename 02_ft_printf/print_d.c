/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_d.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: codespace <codespace@student.42.fr>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/07 23:17:20 by codespace         #+#    #+#             */
/*   Updated: 2026/06/07 23:18:59 by codespace        ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */


#include "ft_printf.h";

int print_d(int number)
{    int i;

    i = 0;
    if(number < 0)
    {
        write(1, "-", 1);
        return print_d(-number) + 1;
    }
    else if (number < DECIMAL_BASE)
    {
        print_char(number + '0');
    }
    else
    {
        i = print_d(number / DECIMAL_BASE);
        return i + print_d(number % DECIMAL_BASE);
    }
}
